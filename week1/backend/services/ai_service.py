import json
import logging
import boto3
from typing import Any

logger = logging.getLogger(__name__)

MODEL_ID = "us.anthropic.claude-haiku-4-5-20251001-v1:0"
REGION = "us-east-1"

_client = None


def _get_client() -> Any:
    global _client
    if _client is None:
        _client = boto3.client("bedrock-runtime", region_name=REGION)
    return _client


def _invoke(system: str, user: str) -> str:
    client = _get_client()
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1024,
        "system": system,
        "messages": [{"role": "user", "content": user}],
    })
    response = client.invoke_model(
        modelId=MODEL_ID,
        contentType="application/json",
        accept="application/json",
        body=body,
    )
    result = json.loads(response["body"].read())
    return result["content"][0]["text"]


def categorize_and_prioritize(
    title: str,
    description: str,
    existing_resolutions: list[dict[str, Any]],
) -> dict[str, Any]:
    existing_summary = ""
    if existing_resolutions:
        items = [f"- {r['title']} (category: {r.get('category', 'unset')}, priority: {r.get('priority', 'unset')})" for r in existing_resolutions]
        existing_summary = "Existing resolutions:\n" + "\n".join(items)

    system = (
        "You are an assistant that categorizes and prioritizes personal resolutions. "
        "Respond with ONLY a JSON object, no extra text. "
        "Categories: Health, Finance, Learning, Career, Personal. "
        "Priority is 1 (highest) to 5 (lowest). "
        "Consider existing resolutions when assigning priority to avoid duplicates."
    )
    user = (
        f"New resolution:\nTitle: {title}\nDescription: {description}\n\n"
        f"{existing_summary}\n\n"
        'Respond with: {"category": "...", "priority": N}'
    )

    try:
        raw = _invoke(system, user)
        parsed = json.loads(raw.strip())
        return {
            "category": parsed.get("category", "Personal"),
            "priority": int(parsed.get("priority", 3)),
        }
    except Exception:
        logger.exception("AI categorize failed, using defaults")
        return {"category": "Personal", "priority": 3}


def analyze_sentiment_and_feedback(
    note: str,
    resolution_title: str,
    resolution_description: str,
    past_check_ins: list[dict[str, Any]],
) -> dict[str, Any]:
    past_summary = ""
    if past_check_ins:
        items = [f"- [{c.get('created_at', '')}] {c['note']} (sentiment: {c.get('sentiment', 'unknown')})" for c in past_check_ins[-5:]]
        past_summary = "Recent check-ins:\n" + "\n".join(items)

    system = (
        "You are a supportive goal-tracking coach. Analyze the sentiment of a progress update "
        "and provide brief, encouraging feedback. "
        "Respond with ONLY a JSON object, no extra text. "
        'Format: {"sentiment": "positive|neutral|negative", "sentiment_score": 0.0-1.0, "ai_feedback": "..."} '
        "The sentiment_score is confidence in the sentiment label (1.0 = very confident). "
        "The ai_feedback should be 1-2 sentences of encouragement or constructive advice."
    )
    user = (
        f"Resolution: {resolution_title}\nGoal: {resolution_description}\n\n"
        f"{past_summary}\n\n"
        f"New check-in note: {note}\n\n"
        "Analyze the sentiment and provide feedback."
    )

    try:
        raw = _invoke(system, user)
        parsed = json.loads(raw.strip())
        return {
            "sentiment": parsed.get("sentiment", "neutral"),
            "sentiment_score": float(parsed.get("sentiment_score", 0.5)),
            "ai_feedback": parsed.get("ai_feedback", "Keep going!"),
        }
    except Exception:
        logger.exception("AI sentiment analysis failed, using defaults")
        return {
            "sentiment": "neutral",
            "sentiment_score": 0.5,
            "ai_feedback": "Keep going! Every step counts.",
        }
