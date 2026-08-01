from typing import List, Optional, Dict, Any
from collections import Counter
from uuid import UUID

from src.models.match_model import Match
from src.models.team_model import Team
from src.schemas.team_schemas import TeamSimpleResponse
from src.schemas.stadium_schemas import StadiumSimpleResponse
from src.schemas.h2h_schemas import (
    H2HSummaryResponse,
    H2HMatchItemResponse,
    H2HBiggestWinResponse,
    EntityMatchCountResponse,
    FrequentScoreResponse
)

class H2HCalculator:
    """
    Engine coeso responsável por processar o retrospecto entre duas equipes,
    gerando agregados de gols, vitórias, goleadas, métricas temporais e listas.
    """

    def __init__(self, team1: Team, team2: Team):
        self.team1 = team1
        self.team2 = team2

    def calculate(self, matches: List[Match]) -> H2HSummaryResponse:
        """Método principal orquestrador do cálculo do retrospecto."""
        if not matches:
            return self._build_empty_response()

        # 1. Processa partidas e consolida acumulados
        accumulated_stats = self._process_matches_loop(matches)

        # 2. Constrói o DTO final estruturado
        return self._build_summary_response(accumulated_stats, matches)

    def _process_matches_loop(self, matches: List[Match]) -> Dict[str, Any]:
        """Percorre a lista de partidas acumulando métricas e identificando goleadas."""
        t1_id = self.team1.id

        t1_wins = 0
        t2_wins = 0
        draws = 0
        t1_goals = 0
        t2_goals = 0

        biggest_diff_t1, biggest_match_t1 = -1, None
        biggest_diff_t2, biggest_match_t2 = -1, None
        biggest_diff_home_t1, biggest_match_home_t1 = -1, None
        biggest_diff_away_t1, biggest_match_away_t1 = -1, None
        most_goals_count, match_most_goals = -1, None

        scores_counter = Counter()
        years_counter = Counter()

        stadiums_counter: Dict[UUID, Dict[str, Any]] = {}
        competitions_counter: Dict[UUID, Dict[str, Any]] = {}
        match_items: List[H2HMatchItemResponse] = []

        for m in matches:
            is_t1_home = (m.home_team_id == t1_id)
            t1_score = m.home_score if is_t1_home else m.away_score
            t2_score = m.away_score if is_t1_home else m.home_score

            t1_goals += t1_score
            t2_goals += t2_score

            # Partida com mais gols
            total_match_goals = m.home_score + m.away_score
            if total_match_goals > most_goals_count:
                most_goals_count, match_most_goals = total_match_goals, m

            # Contadores de frequência
            scores_counter[f"{t1_score} x {t2_score}"] += 1

            # Contagem de Estádios (Corrigido: incremento na chave 'count')
            if m.stadium:
                st_id = m.stadium.id
                if st_id not in stadiums_counter:
                    stadiums_counter[st_id] = {
                        "id": st_id, 
                        "name": m.stadium.nickname or m.stadium.name, 
                        "count": 0
                    }
                stadiums_counter[st_id]["count"] += 1

            # Contagem de Competições
            if m.edition and m.edition.competition:
                comp = m.edition.competition
                if comp.id not in competitions_counter:
                    competitions_counter[comp.id] = {
                        "id": comp.id, 
                        "name": comp.name, 
                        "count": 0
                    }
                competitions_counter[comp.id]["count"] += 1

            if m.date:
                years_counter[m.date.year] += 1

            # Avaliação de resultado e goleadas
            if t1_score > t2_score:
                t1_wins += 1
                diff = t1_score - t2_score
                if diff > biggest_diff_t1:
                    biggest_diff_t1, biggest_match_t1 = diff, m
                if is_t1_home and diff > biggest_diff_home_t1:
                    biggest_diff_home_t1, biggest_match_home_t1 = diff, m
                elif not is_t1_home and diff > biggest_diff_away_t1:
                    biggest_diff_away_t1, biggest_match_away_t1 = diff, m
            elif t2_score > t1_score:
                t2_wins += 1
                diff = t2_score - t1_score
                if diff > biggest_diff_t2:
                    biggest_diff_t2, biggest_match_t2 = diff, m
            else:
                draws += 1

            match_items.append(self._build_match_item_dto(m))

        return {
            "t1_wins": t1_wins,
            "t2_wins": t2_wins,
            "draws": draws,
            "t1_goals": t1_goals,
            "t2_goals": t2_goals,
            "biggest_diff_t1": biggest_diff_t1,
            "biggest_match_t1": biggest_match_t1,
            "biggest_diff_t2": biggest_diff_t2,
            "biggest_match_t2": biggest_match_t2,
            "biggest_diff_home_t1": biggest_diff_home_t1,
            "biggest_match_home_t1": biggest_match_home_t1,
            "biggest_diff_away_t1": biggest_diff_away_t1,
            "biggest_match_away_t1": biggest_match_away_t1,
            "most_goals_count": most_goals_count,
            "match_most_goals": match_most_goals,
            "scores_counter": scores_counter,
            "stadiums_counter": stadiums_counter,
            "competitions_counter": competitions_counter,
            "years_counter": years_counter,
            "match_items": match_items
        }

    def _build_summary_response(self, stats: Dict[str, Any], matches: List[Match]) -> H2HSummaryResponse:
        """Monta e formata a resposta final do retrospecto."""
        total = len(matches)
        t1_goals, t2_goals = stats["t1_goals"], stats["t2_goals"]
        t1_wins, t2_wins = stats["t1_wins"], stats["t2_wins"]

        avg_goals = round((t1_goals + t2_goals) / total, 2) if total > 0 else 0.0
        t1_win_rate = round((t1_wins / total * 100), 1) if total > 0 else 0.0
        t2_win_rate = round((t2_wins / total * 100), 1) if total > 0 else 0.0

        # Processa placar mais frequente
        most_frequent_score_dto = None
        if stats["scores_counter"]:
            top_score, top_count = stats["scores_counter"].most_common(1)[0]
            most_frequent_score_dto = FrequentScoreResponse(score=top_score, count=top_count)

        # Processa métricas temporais
        years_counter = stats["years_counter"]
        top_year = years_counter.most_common(1)[0][0] if years_counter else None
        total_years = len(years_counter)
        avg_matches_per_year = round(total / total_years, 1) if total_years > 0 else 0.0

        # Corrigido: Acessando via dicionário stats
        stadiums_list = [
            EntityMatchCountResponse(**data) 
            for data in sorted(stats["stadiums_counter"].values(), key=lambda x: x["count"], reverse=True)
        ]

        competitions_list = [
            EntityMatchCountResponse(**data) 
            for data in sorted(stats["competitions_counter"].values(), key=lambda x: x["count"], reverse=True)
        ]

        return H2HSummaryResponse(
            team1=TeamSimpleResponse.model_validate(self.team1),
            team2=TeamSimpleResponse.model_validate(self.team2),
            total_matches=total,
            team1_wins=t1_wins,
            team2_wins=t2_wins,
            draws=stats["draws"],
            team1_goals=t1_goals,
            team2_goals=t2_goals,
            goal_difference=t1_goals - t2_goals,
            average_goals_per_match=avg_goals,
            team1_win_rate=t1_win_rate,
            team2_win_rate=t2_win_rate,
            most_frequent_score=most_frequent_score_dto,
            match_with_most_goals=self._build_biggest_win_dto(stats["match_most_goals"], stats["most_goals_count"]),
            biggest_win_team1=self._build_biggest_win_dto(stats["biggest_match_t1"], stats["biggest_diff_t1"]),
            biggest_win_team2=self._build_biggest_win_dto(stats["biggest_match_t2"], stats["biggest_diff_t2"]),
            biggest_home_win_team1=self._build_biggest_win_dto(stats["biggest_match_home_t1"], stats["biggest_diff_home_t1"]),
            biggest_away_win_team1=self._build_biggest_win_dto(stats["biggest_match_away_t1"], stats["biggest_diff_away_t1"]),
            year_with_most_matches=top_year,
            average_matches_per_year=avg_matches_per_year,
            stadiums_played=stadiums_list,
            competitions_played=competitions_list,
            matches=stats["match_items"]
        )

    def _build_match_item_dto(self, match: Match) -> H2HMatchItemResponse:
        """Converte uma entidade Match para o DTO de item do histórico."""
        return H2HMatchItemResponse(
            match_id=match.id,
            date=match.date,
            edition_name=match.edition.name if match.edition else "",
            phase_name=match.phase.name if match.phase else None,
            round_number=match.round.number if match.round else None,
            home_team=TeamSimpleResponse.model_validate(match.home_team),
            away_team=TeamSimpleResponse.model_validate(match.away_team),
            stadium=StadiumSimpleResponse.model_validate(match.stadium) if match.stadium else None,
            home_score=match.home_score,
            away_score=match.away_score,
            home_penalty_score=match.home_penalty_score,
            away_penalty_score=match.away_penalty_score,
            status=match.status
        )

    def _build_biggest_win_dto(self, match: Optional[Match], diff: int) -> Optional[H2HBiggestWinResponse]:
        """Converte uma partida de goleada para DTO com o estádio preenchido."""
        if not match or diff <= 0:
            return None

        return H2HBiggestWinResponse(
            match_id=match.id,
            date=match.date,
            edition_name=match.edition.name if match.edition else "",
            home_team=TeamSimpleResponse.model_validate(match.home_team),
            away_team=TeamSimpleResponse.model_validate(match.away_team),
            stadium=StadiumSimpleResponse.model_validate(match.stadium) if match.stadium else None,
            home_score=match.home_score,
            away_score=match.away_score,
            score_difference=diff
        )

    def _build_empty_response(self) -> H2HSummaryResponse:
        """Retorna uma estrutura zerada caso os times nunca tenham se enfrentado."""
        return H2HSummaryResponse(
            team1=TeamSimpleResponse.model_validate(self.team1),
            team2=TeamSimpleResponse.model_validate(self.team2),
            total_matches=0,
            team1_wins=0,
            team2_wins=0,
            draws=0,
            team1_goals=0,
            team2_goals=0,
            goal_difference=0,
            average_goals_per_match=0.0,
            team1_win_rate=0.0,
            team2_win_rate=0.0,
            matches=[]
        )