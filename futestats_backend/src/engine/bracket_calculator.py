from typing import List, Dict, Tuple, Optional
from datetime import datetime
from uuid import UUID

from src.models.match_model import Match
from src.schemas.team_schemas import TeamSimpleResponse
from src.schemas.stadium_schemas import StadiumSimpleResponse
from src.schemas.bracket_schemas import (
    ConfrontoResponse,
    KnockoutMatchResponse,
    KnockoutPhaseResponse
)

class BracketCalculator:
    """
    Engine coeso responsável por processar os jogos de uma fase Mata-Mata,
    agrupando partidas por confronto, somando placares agregados,
    processando pênaltis e determinando o time classificado.
    """

    def calculate_phase_confrontos(
        self,
        phase_id: UUID,
        phase_name: str,
        order: int,
        matches: List[Match]
    ) -> KnockoutPhaseResponse:
        
        grouped_matches = self._group_matches_by_teams(matches)
        confrontos = [
            self._process_single_confronto(match_list)
            for match_list in grouped_matches.values()
            if match_list
        ]

        return KnockoutPhaseResponse(
            phase_id=phase_id,
            phase_name=phase_name,
            order=order,
            confrontos=confrontos
        )

    def _group_matches_by_teams(
        self, 
        matches: List[Match]
    ) -> Dict[Tuple[UUID, UUID], List[Match]]:
        """Agrupa os jogos pela dupla de times envolvida (independente de mandante/visitante)."""
        grouped: Dict[Tuple[UUID, UUID], List[Match]] = {}
        for match in matches:
            pair_key = tuple(sorted([match.home_team_id, match.away_team_id]))
            grouped.setdefault(pair_key, []).append(match)
        return grouped

    def _process_single_confronto(self, match_list: List[Match]) -> ConfrontoResponse:
        """Processa um confronto entre 2 clubes, suportando 1, 2 ou 3 jogos (jogo extra)."""
        # Ordena cronologicamente os jogos (Ida -> Volta -> Desempate)
        match_list.sort(key=lambda m: m.date or datetime.min)

        first_match = match_list[0]
        team_a = TeamSimpleResponse.model_validate(first_match.home_team)
        team_b = TeamSimpleResponse.model_validate(first_match.away_team)

        knockout_matches = [self._build_match_dto(m) for m in match_list]
        agg_a, agg_b = self._calculate_aggregate_score(team_a.id, match_list)
        pen_a, pen_b, decided_on_penalties = self._extract_penalties_score(team_a.id, match_list)

        winner_id = self._determine_winner(
            team_a_id=team_a.id,
            team_b_id=team_b.id,
            agg_a=agg_a,
            agg_b=agg_b,
            pen_a=pen_a,
            pen_b=pen_b,
            decided_on_penalties=decided_on_penalties
        )

        return ConfrontoResponse(
            confronto_id=f"{team_a.sigla}-x-{team_b.sigla}",
            team_a=team_a,
            team_b=team_b,
            matches=knockout_matches,
            aggregate_score_a=agg_a,
            aggregate_score_b=agg_b,
            penalties_score_a=pen_a,
            penalties_score_b=pen_b,
            winner_team_id=winner_id,
            is_decided_on_penalties=decided_on_penalties
        )

    def _build_match_dto(self, match: Match) -> KnockoutMatchResponse:
        """Converte o model SQLAlchemy Match para o DTO de resposta do FastAPI."""
        return KnockoutMatchResponse(
            id=match.id,
            round_number=match.round.number if match.round else 1,
            date=match.date,
            home_team=TeamSimpleResponse.model_validate(match.home_team),
            away_team=TeamSimpleResponse.model_validate(match.away_team),
            stadium=StadiumSimpleResponse.model_validate(match.stadium) if match.stadium else None,
            home_score=match.home_score,
            away_score=match.away_score,
            home_penalty_score=match.home_penalty_score,
            away_penalty_score=match.away_penalty_score,
            status=match.status
        )

    def _calculate_aggregate_score(
        self, 
        team_a_id: UUID, 
        matches: List[Match]
    ) -> Tuple[int, int]:
        """Soma o placar agregado acumulado em 1, 2 ou 3 jogos do confronto."""
        agg_a = 0
        agg_b = 0
        for m in matches:
            if m.home_team_id == team_a_id:
                agg_a += m.home_score
                agg_b += m.away_score
            else:
                agg_b += m.home_score
                agg_a += m.away_score
        return agg_a, agg_b

    def _extract_penalties_score(
        self, 
        team_a_id: UUID, 
        matches: List[Match]
    ) -> Tuple[Optional[int], Optional[int], bool]:
        """Localiza a partida onde ocorreu a disputa por pênaltis (se houver)."""
        for m in matches:
            if m.home_penalty_score is not None and m.away_penalty_score is not None:
                if m.home_team_id == team_a_id:
                    return m.home_penalty_score, m.away_penalty_score, True
                else:
                    return m.away_penalty_score, m.home_penalty_score, True
        return None, None, False

    def _determine_winner(
        self,
        team_a_id: UUID,
        team_b_id: UUID,
        agg_a: int,
        agg_b: int,
        pen_a: Optional[int],
        pen_b: Optional[int],
        decided_on_penalties: bool
    ) -> Optional[UUID]:
        """Determina qual clube avançou de fase (por placar agregado ou pênaltis)."""
        # 1. Desempate no Placar Agregado
        if agg_a > agg_b:
            return team_a_id
        elif agg_b > agg_a:
            return team_b_id

        # 2. Desempate por Pênaltis (se o agregado terminou empatado)
        if decided_on_penalties and pen_a is not None and pen_b is not None:
            if pen_a > pen_b:
                return team_a_id
            elif pen_b > pen_a:
                return team_b_id

        return None