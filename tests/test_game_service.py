"""
Tests for game_service.py — round lifecycle management.
"""

import pytest
from app.services.game_service import create_round, get_round, reveal_answer, add_strike, reveal_board, get_client_board


SAMPLE_BOARD = {
    "id": "test_01",
    "prompt": "Name something students do before an exam",
    "answers": [
        {"text": "study", "score": 42},
        {"text": "panic", "score": 20},
        {"text": "drink coffee", "score": 15},
    ],
    "source_type": "real",
    "category": "student_life",
}


class TestCreateRound:
    def test_creates_round(self):
        state = create_round(SAMPLE_BOARD)
        assert "round_id" in state
        assert state["prompt"] == SAMPLE_BOARD["prompt"]
        assert len(state["answers"]) == 3
        assert state["score"] == 0
        assert state["strikes"] == 0
        assert state["round_over"] is False

    def test_answers_not_revealed(self):
        state = create_round(SAMPLE_BOARD)
        for ans in state["answers"]:
            assert ans["revealed"] is False


class TestGetRound:
    def test_get_existing(self):
        state = create_round(SAMPLE_BOARD)
        fetched = get_round(state["round_id"])
        assert fetched is not None
        assert fetched["round_id"] == state["round_id"]

    def test_get_nonexistent(self):
        assert get_round("nonexistent-id") is None


class TestRevealAnswer:
    def test_reveals_and_scores(self):
        state = create_round(SAMPLE_BOARD)
        rid = state["round_id"]
        updated = reveal_answer(rid, 0, "study")
        assert updated["answers"][0]["revealed"] is True
        assert updated["score"] == 42
        assert "study" in updated["guesses"]

    def test_round_over_when_all_revealed(self):
        state = create_round(SAMPLE_BOARD)
        rid = state["round_id"]
        reveal_answer(rid, 0, "study")
        reveal_answer(rid, 1, "panic")
        updated = reveal_answer(rid, 2, "coffee")
        assert updated["round_over"] is True


class TestAddStrike:
    def test_adds_strike(self):
        state = create_round(SAMPLE_BOARD)
        rid = state["round_id"]
        updated = add_strike(rid, "wrong")
        assert updated["strikes"] == 1
        assert updated["round_over"] is False

    def test_round_over_on_max_strikes(self):
        state = create_round(SAMPLE_BOARD)
        rid = state["round_id"]
        add_strike(rid, "wrong1")
        add_strike(rid, "wrong2")
        updated = add_strike(rid, "wrong3")
        assert updated["strikes"] == 3
        assert updated["round_over"] is True


class TestRevealBoard:
    def test_reveals_all(self):
        state = create_round(SAMPLE_BOARD)
        rid = state["round_id"]
        updated = reveal_board(rid)
        assert all(a["revealed"] for a in updated["answers"])
        assert updated["round_over"] is True


class TestGetClientBoard:
    def test_hides_unrevealed(self):
        state = create_round(SAMPLE_BOARD)
        board = get_client_board(state)
        assert len(board) == 3
        for slot in board:
            assert slot.text is None
            assert slot.score is None
            assert slot.revealed is False

    def test_shows_revealed(self):
        state = create_round(SAMPLE_BOARD)
        rid = state["round_id"]
        reveal_answer(rid, 0, "study")
        board = get_client_board(state)
        assert board[0].text == "study"
        assert board[0].score == 42
        assert board[0].revealed is True
        assert board[1].text is None  # Still hidden
