"""
ai_service.py — LLM Integration Layer (Google Gemini)

Handles:
- Board generation (fallback when real boards unavailable)
- Semantic guess matching (when exact/fuzzy fail)
- Optional commentary generation

This is the ONLY module that talks to the LLM.
All calls return parsed dicts or None on failure (graceful degradation).
"""

import json
import traceback
from typing import Optional

from google import genai
from google.genai import types
from app.config import settings


# ---------------------------------------------------------------------------
# Client Initialization
# ---------------------------------------------------------------------------
_client = None


def _get_client():
    """Lazy-init Gemini client."""
    global _client
    if _client is None:
        if not settings.GEMINI_API_KEY:
            print("[ai_service] WARNING: No GEMINI_API_KEY set, AI features disabled")
            return None
        _client = genai.Client(api_key=settings.GEMINI_API_KEY)
    return _client


# ---------------------------------------------------------------------------
# Board Generation
# ---------------------------------------------------------------------------
async def generate_board(category: str = None, topic: str = None) -> Optional[dict]:
    """
    Generate a Family Feud-style board using Gemini.
    
    Returns dict with: prompt, answers, category, source_type
    Returns None if LLM call fails.
    """
    client = _get_client()
    if not client:
        return None

    category_hint = f"Category: {category}" if category else "Category: general"
    topic_hint = f"Topic to incorporate: {topic}" if topic else ""

    user_prompt = f"""Generate a realistic Family Feud survey board as JSON.

Requirements:
- The prompt should be a survey-style question beginning with "Name..." or "Tell me..."
- Provide 5 to 8 ranked answers
- Scores must sum to exactly 100
- Answers must be distinct, concise (2-5 words max), and sound like likely crowd responses
- {category_hint}
- {topic_hint}
- Tone should feel modern, relevant, and fun
- Do NOT use any markdown formatting

Return ONLY valid JSON in this exact format, nothing else:
{{
  "prompt": "Name something ...",
  "answers": [
    {{"text": "answer text", "score": 34}},
    {{"text": "answer text", "score": 25}},
    {{"text": "answer text", "score": 18}},
    {{"text": "answer text", "score": 12}},
    {{"text": "answer text", "score": 11}}
  ],
  "category": "{category or 'general'}",
  "source_type": "{'hybrid' if topic else 'ai'}"
}}"""

    try:
        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=user_prompt,
            config=types.GenerateContentConfig(
                temperature=0.9,
                max_output_tokens=1024,
            ),
        )

        text = response.text.strip()
        # Clean up potential markdown code fences
        if text.startswith("```"):
            text = text.split("\n", 1)[1] if "\n" in text else text[3:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()

        board = json.loads(text)

        # Validate structure
        if "prompt" not in board or "answers" not in board:
            print(f"[ai_service] Invalid board structure: {list(board.keys())}")
            return None

        if len(board["answers"]) < 3:
            print(f"[ai_service] Too few answers: {len(board['answers'])}")
            return None

        # Ensure source_type
        board["source_type"] = "hybrid" if topic else "ai"
        board["category"] = board.get("category", category or "general")

        print(f"[ai_service] Generated board: '{board['prompt']}' ({len(board['answers'])} answers)")
        return board

    except Exception as e:
        print(f"[ai_service] Board generation failed: {e}")
        traceback.print_exc()
        return None


# ---------------------------------------------------------------------------
# Semantic Guess Matching
# ---------------------------------------------------------------------------
async def semantic_match(guess: str, answers: list[str]) -> Optional[dict]:
    """
    Use LLM to determine if a guess semantically matches any board answer.
    
    Args:
        guess: The player's free-text guess
        answers: List of unrevealed answer strings
    
    Returns:
        Dict with: is_match (bool), matched_answer (str), confidence (float)
        Returns None if LLM call fails.
    """
    client = _get_client()
    if not client:
        return None

    answers_formatted = "\n".join(f"{i+1}. {a}" for i, a in enumerate(answers))

    user_prompt = f"""You are a judge for a Family Feud survey game. Determine if the player's guess refers to the SAME concept or a closely related answer as one of the board answers.

Board answers:
{answers_formatted}

Player's guess: "{guess}"

Matching Rules:
- A match means the guess describes the SAME core concept, action, or closely related idea as an answer
- Allow: synonyms ("cell phone" = "phone"), shorthand ("coffee" = "grab coffee"), singular/plural
- Allow: rephrasing ("stand at the gate" = "stand by the gate early")
- Allow: closely related survey answers -- in a survey, a person giving the guess would ALSO give the board answer or vice versa
  - Example: "sleep" MATCHES "wake up earlier" (both about sleep/waking habits -- same survey concept)
  - Example: "working out" MATCHES "go to the gym" (same activity, different phrasing)
  - Example: "phone" MATCHES "check their phone" (same thing)
- REJECT: completely different actions that just happen in the same setting
  - Example: "standing in line" does NOT match "check the departure board" (different actions at same place)
  - Example: "eating food" does NOT match "buying a ticket" (unrelated actions)
- REJECT: overly generic guesses that are too broad
- When genuinely unsure, set confidence below 0.5

Return ONLY valid JSON, no markdown:
{{
  "is_match": true or false,
  "matched_answer": "the exact answer text from the list that matches, or null",
  "confidence": 0.0 to 1.0
}}"""

    try:
        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=user_prompt,
            config=types.GenerateContentConfig(
                temperature=0.1,
                max_output_tokens=256,
            ),
        )

        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1] if "\n" in text else text[3:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()

        result = json.loads(text)

        if result.get("is_match") and result.get("confidence", 0) >= settings.SEMANTIC_MATCH_CONFIDENCE:
            print(f"[ai_service] Semantic match: '{guess}' → '{result.get('matched_answer')}' (conf={result.get('confidence')})")
            return result
        else:
            print(f"[ai_service] No semantic match for '{guess}' (conf={result.get('confidence', 0)})")
            return result  # Return result even if not matched so caller can decide

    except Exception as e:
        print(f"[ai_service] Semantic match failed: {e}")
        return None


# ---------------------------------------------------------------------------
# Commentary Generation (Stretch)
# ---------------------------------------------------------------------------
async def generate_commentary(prompt: str, answers: list[dict], source_type: str) -> Optional[str]:
    """Generate a short end-of-round commentary."""
    client = _get_client()
    if not client:
        return None

    answers_text = ", ".join(a["text"] for a in answers[:3])

    user_prompt = f"""A Family Feud round just finished. The question was: "{prompt}"
The top answers were: {answers_text}
The board was sourced from: {source_type} data.

Write ONE short, fun sentence commenting on the results (max 20 words). Be witty and casual."""

    try:
        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=user_prompt,
            config=types.GenerateContentConfig(
                temperature=0.8,
                max_output_tokens=100,
            ),
        )
        text = response.text.strip().strip('"')
        return text if len(text) < 200 else text[:200]
    except Exception:
        return None
