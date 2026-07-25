from typing import List, Dict
from uuid import UUID

from src.models.edition_model import Edition
from src.models.match_model import Match
from src.models.enums import StandingsZoneEnum
from src.schemas.round_schemas import TeamSimpleResponse
from src.schemas.standings_schemas import TeamStatsAccumulator, TeamStandingResponse

# TODO: COMENTAR CADA UM DOS MÉTODOS
class StandingsCalculator:
    """
    Motor desacoplado responsável por processar os jogos e gerar a classificação.
    Suporta regras configuráveis de pontuação (ex: 3 ou 2 pts por vitória) e zonas flexíveis.
    """

    def __init__(self, edition: Edition):
        self.edition = edition
        self.rules   = edition.rules_config or {}
        
        # Pontuação por vitória configurável (Default: 3 pts. Para edições antigas: 2 pts)
        self.points_per_win : int = self.rules.get("points_per_win", 3)
        self.points_per_draw: int = self.rules.get("points_per_draw", 1)

    def calculate(self, matches: List[Match]) -> List[TeamStandingResponse]:
        accumulators = self._initialize_accumulators()

        self._process_matches(accumulators, matches)
        self._calculate_derived_metrics(accumulators)

        sorted_stats = self._sort_standings(accumulators)
        return self._apply_zones_and_positions(sorted_stats)

    def _initialize_accumulators(self) -> Dict[UUID, TeamStatsAccumulator]:
        accumulators = {}
        for team in self.edition.teams:
            accumulators[team.id] = TeamStatsAccumulator(
                team=TeamSimpleResponse.model_validate(team)
            )
        return accumulators


    def _process_matches(self, accumulators: Dict[UUID, TeamStatsAccumulator], matches: List[Match]) -> None:
        for match in matches:
            home = accumulators.get(match.home_team_id)
            away = accumulators.get(match.away_team_id)

            if not home or not away:
                continue

            home.played += 1
            away.played += 1

            home.goals_for     += match.home_score
            home.goals_against += match.away_score
            away.goals_for     += match.away_score
            away.goals_against += match.home_score

            if match.home_score > match.away_score:
                home.points += self.points_per_win
                home.wins   += 1
                away.losses += 1
            elif match.away_score > match.home_score:
                away.points += self.points_per_win
                away.wins   += 1
                home.losses += 1
            else:
                home.points += self.points_per_draw
                away.points += self.points_per_draw
                home.draws  += 1
                away.draws  += 1

    def _calculate_derived_metrics(self, accumulators: Dict[UUID, TeamStatsAccumulator]) -> None:
        for stats in accumulators.values():
            stats.goal_difference = stats.goals_for - stats.goals_against

            max_points_possible = stats.played * self.points_per_win
            if max_points_possible > 0:
                stats.win_rate = round((stats.points / max_points_possible) * 100, 1)

    def _sort_standings(self, accumulators: Dict[UUID, TeamStatsAccumulator]) -> List[TeamStatsAccumulator]:
        # Critério de desempate padrão: Pontos > Vitórias > Saldo de Gols > Gols Pró
        return sorted(
            accumulators.values(),
            key=lambda x: (x.points, x.wins, x.goal_difference, x.goals_for),
            reverse=True
        )

    # TODO: [FUTURO] : DEIXAR A FUNÇÃO MAIS GENÉRICA PARA QUALQUER LIGA
    def _apply_zones_and_positions(self, stats_list: List[TeamStatsAccumulator]) -> List[TeamStandingResponse]:
        total_teams     = len(stats_list)
        relegated_count = self.edition.relegated_count or 0
        
        # Mapeamento dinâmico lido do regulamento da edição
        promotion_count = self.rules.get("promotion_count", 0)         # Ex: Série B (4 sobem)
        g_direct        = self.rules.get("g4_direct_libertadores", 0)  # Ex: Série A
        g_pre           = self.rules.get("pre_libertadores", 0)
        sula_count      = self.rules.get("sulamericana_count", 0)
        qualified_count = self.rules.get("qualified_next_stage", 0)    # Ex: Estaduais

        result = []
        for idx, item in enumerate(stats_list, start=1):
            zone = StandingsZoneEnum.NEUTRAL

            # Regras dinâmicas por posição
            if idx == 1:
                zone = StandingsZoneEnum.CHAMPION if item.played > 0 else StandingsZoneEnum.NEUTRAL
            elif g_direct > 0 and idx <= g_direct:
                zone = StandingsZoneEnum.LIBERTADORES_DIRECT
            elif g_pre > 0 and idx <= (g_direct + g_pre):
                zone = StandingsZoneEnum.LIBERTADORES_PRE
            elif promotion_count > 0 and idx <= promotion_count:
                zone = StandingsZoneEnum.PROMOTION
            elif qualified_count > 0 and idx <= qualified_count:
                zone = StandingsZoneEnum.QUALIFIED
            elif sula_count > 0 and idx <= (g_direct + g_pre + sula_count):
                zone = StandingsZoneEnum.SUDAMERICANA
            elif relegated_count > 0 and total_teams > 0 and idx > (total_teams - relegated_count):
                zone = StandingsZoneEnum.RELEGATION

            result.append(
                TeamStandingResponse(
                    position=idx,
                    team=item.team,
                    points=item.points,
                    played=item.played,
                    wins=item.wins,
                    draws=item.draws,
                    losses=item.losses,
                    goals_for=item.goals_for,
                    goals_against=item.goals_against,
                    goal_difference=item.goal_difference,
                    win_rate=item.win_rate,
                    zone=zone
                )
            )

        return result