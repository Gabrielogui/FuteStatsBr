from typing import List, Optional
from uuid import UUID

from src.models.match_model import Match
from src.models.team_model import Team
from src.schemas.team_schemas import TeamSimpleResponse
from src.schemas.stadium_schemas import StadiumSimpleResponse
from src.schemas.h2h_schemas import (
    H2HSummaryResponse,
    H2HMatchItemResponse,
    H2HBiggestWinResponse
)

class H2HCalculator:
    """
    Engine coeso que processa a lista de partidas entre duas equipes e gera
    estatísticas detalhadas do confronto direto.
    """

    def __init__(self, team1: Team, team2: Team):
        self.team1 = team1
        self.team2 = team2

    def calculate(self, matches: List[Match]) -> H2HSummaryResponse:
        t1_id = self.team1.id
        t2_id = self.team2.id

        t1_wins = 0
        t2_wins = 0
        draws = 0
        t1_goals = 0
        t2_goals = 0

        biggest_diff_t1 = -1
        biggest_diff_t2 = -1
        biggest_match_t1: Optional[Match] = None
        biggest_match_t2: Optional[Match] = None

        match_items: List[H2HMatchItemResponse] = []

        for m in matches:
            is_t1_home = (m.home_team_id == t1_id)
            
            # Gols da partida
            t1_score = m.home_score if is_t1_home else m.away_score
            t2_score = m.away_score if is_t1_home else m.home_score

            t1_goals += t1_score
            t2_goals += t2_score

            # Vitória / Empate / Derrota
            if t1_score > t2_score:
                t1_wins += 1
                diff = t1_score - t2_score
                if diff > biggest_diff_t1:
                    biggest_diff_t1 = diff
                    biggest_match_t1 = m
            elif t2_score > t1_score:
                t2_wins += 1
                diff = t2_score - t1_score
                if diff > biggest_diff_t2:
                    biggest_diff_t2 = diff
                    biggest_match_t2 = m
            else:
                draws += 1

            # DTO da Partida
            match_items.append(
                H2HMatchItemResponse(
                    match_id=m.id,
                    date=m.date,
                    edition_name=m.edition.name if m.edition else "",
                    phase_name=m.phase.name if m.phase else None,
                    round_number=m.round.number if m.round else None,
                    home_team=TeamSimpleResponse.model_validate(m.home_team),
                    away_team=TeamSimpleResponse.model_validate(m.away_team),
                    stadium=StadiumSimpleResponse.model_validate(m.stadium) if m.stadium else None,
                    home_score=m.home_score,
                    away_score=m.away_score,
                    home_penalty_score=m.home_penalty_score,
                    away_penalty_score=m.away_penalty_score,
                    status=m.status
                )
            )

        total = len(matches)
        t1_win_rate = round((t1_wins / total * 100), 1) if total > 0 else 0.0
        t2_win_rate = round((t2_wins / total * 100), 1) if total > 0 else 0.0

        return H2HSummaryResponse(
            team1=TeamSimpleResponse.model_validate(self.team1),
            team2=TeamSimpleResponse.model_validate(self.team2),
            total_matches=total,
            team1_wins=t1_wins,
            team2_wins=t2_wins,
            draws=draws,
            team1_goals=t1_goals,
            team2_goals=t2_goals,
            goal_difference=t1_goals - t2_goals,
            team1_win_rate=t1_win_rate,
            team2_win_rate=t2_win_rate,
            biggest_win_team1=self._build_biggest_win_dto(biggest_match_t1, biggest_diff_t1),
            biggest_win_team2=self._build_biggest_win_dto(biggest_match_t2, biggest_diff_t2),
            matches=match_items
        )

    def _build_biggest_win_dto(self, match: Optional[Match], diff: int) -> Optional[H2HBiggestWinResponse]:
        if not match or diff <= 0:
            return None

        return H2HBiggestWinResponse(
            match_id=match.id,
            date=match.date,
            edition_name=match.edition.name if match.edition else "",
            home_team=TeamSimpleResponse.model_validate(match.home_team),
            away_team=TeamSimpleResponse.model_validate(match.away_team),
            home_score=match.home_score,
            away_score=match.away_score,
            score_difference=diff
        )
    