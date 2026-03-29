"""
Tests for API endpoints via FastAPI TestClient.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


class TestLandingPage:
    def test_home_loads(self):
        res = client.get("/")
        assert res.status_code == 200
        assert "Family Feud" in res.text

    def test_play_page_loads(self):
        res = client.get("/play")
        assert res.status_code == 200
        assert "game-container" in res.text

    def test_play_page_with_category(self):
        res = client.get("/play?category=student_life")
        assert res.status_code == 200


class TestCategoriesEndpoint:
    def test_get_categories(self):
        res = client.get("/api/categories")
        assert res.status_code == 200
        data = res.json()
        assert "categories" in data
        assert len(data["categories"]) > 0


class TestNewRoundEndpoint:
    def test_new_round(self):
        res = client.post("/api/new-round", json={"prefer_real": True})
        assert res.status_code == 200
        data = res.json()
        assert "round_id" in data
        assert "prompt" in data
        assert "board" in data
        assert data["score"] == 0
        assert data["strikes"] == 0
        assert data["source_type"] in ["real", "ai", "hybrid"]

    def test_new_round_with_category(self):
        res = client.post("/api/new-round", json={"category": "daily_life", "prefer_real": True})
        assert res.status_code == 200
        data = res.json()
        # Category should match or fall back to another
        assert "category" in data

    def test_board_answers_hidden(self):
        res = client.post("/api/new-round", json={})
        assert res.status_code == 200
        data = res.json()
        for slot in data["board"]:
            assert slot["text"] is None
            assert slot["score"] is None
            assert slot["revealed"] is False


class TestGuessEndpoint:
    def _start_round(self):
        res = client.post("/api/new-round", json={"prefer_real": True})
        return res.json()

    def test_guess_flow(self):
        """Test that a guess submission returns proper structure."""
        round_data = self._start_round()
        res = client.post("/api/guess", json={
            "round_id": round_data["round_id"],
            "guess": "something random"
        })
        assert res.status_code == 200
        data = res.json()
        assert "correct" in data
        assert "board" in data
        assert "score" in data
        assert "strikes" in data
        assert "round_over" in data

    def test_invalid_round(self):
        res = client.post("/api/guess", json={
            "round_id": "fake-id",
            "guess": "test"
        })
        assert res.status_code == 404

    def test_empty_guess(self):
        round_data = self._start_round()
        res = client.post("/api/guess", json={
            "round_id": round_data["round_id"],
            "guess": "  "
        })
        assert res.status_code == 400


class TestRevealEndpoint:
    def test_reveal(self):
        res = client.post("/api/new-round", json={})
        assert res.status_code == 200
        round_data = res.json()

        res = client.post("/api/reveal", json={
            "round_id": round_data["round_id"]
        })
        assert res.status_code == 200
        data = res.json()
        assert all(slot["revealed"] for slot in data["board"])
        assert all(slot["text"] is not None for slot in data["board"])

    def test_reveal_invalid_round(self):
        res = client.post("/api/reveal", json={"round_id": "fake-id"})
        assert res.status_code == 404
