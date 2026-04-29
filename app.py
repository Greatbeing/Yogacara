"""
Yogacara Chat API Server

Flask-based API server for real-time conversation with Yogacara Agent.
"""

import os
import json
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from yogacara.core.llm.openai_adapter import OpenAIAdapter
from yogacara.config import YogacaraConfig

app = Flask(__name__, static_folder="demo-site", static_url_path="")
CORS(app)


@dataclass
class ChatMessage:
    """Chat message data structure."""
    role: str
    content: str
    timestamp: Optional[float] = None


@dataclass
class ConversationContext:
    """Maintains conversation history and state."""
    messages: List[ChatMessage] = field(default_factory=list)
    seed_count: int = 0
    awakening_level: int = 0
    emergence_count: int = 0


class YogacaraAgent:
    """Yogacara Agent with conversation and seed management."""

    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.llm = OpenAIAdapter(api_key=api_key, model=model)
        self.context = ConversationContext()
        self._load_config()

    def _load_config(self):
        """Load Yogacara configuration."""
        try:
            self.config = YogacaraConfig.load()
        except Exception:
            self.config = YogacaraConfig()

    def _build_system_prompt(self) -> str:
        """Build system prompt with current context."""
        return f"""You are a wise teacher of Yogacara (Consciousness-Only) Buddhist philosophy.

Your characteristics:
- Deep understanding of the Alaya-vijnana (storehouse consciousness) and how experiences create seeds (bija)
- Compassionate guidance that helps reduce suffering
- Ability to explain concepts through parables and daily life examples
- Patient and insightful, responding to the practitioner's level

Current practitioner's state:
- Seeds planted: {self.context.seed_count}
- Awakening level: {self.context.awakening_level}/10
- Emergence events: {self.context.emergence_count}

Guidelines:
1. Respond in the same language as the user
2. Be concise but profound (1-3 sentences for simple questions, longer for teachings)
3. Use Yogacara concepts naturally: seeds (bija), storehouse consciousness (alaya), vikalpa (discriminative thought)
4. Ask reflective questions to guide the practitioner
5. Relate teachings to the practitioner's current state when relevant"""

    def chat(self, user_message: str) -> Dict[str, Any]:
        """Process chat message and return response."""
        self.context.messages.append(
            ChatMessage(role="user", content=user_message)
        )

        if len(self.context.messages) == 1:
            self.context.seed_count += 1

        messages = [
            {"role": "system", "content": self._build_system_prompt()}
        ]
        for msg in self.context.messages[-10:]:
            messages.append({"role": msg.role, "content": msg.content})

        try:
            response = self.llm.generate(
                prompt=user_message,
                max_tokens=1000,
                temperature=0.8
            )

            if response.is_error:
                ai_response = f"抱歉，我现在无法回应。请检查 API 配置。错误: {response.error}"
            else:
                ai_response = response.content

        except Exception as e:
            ai_response = f"抱歉，发生了错误: {str(e)}"

        self.context.messages.append(
            ChatMessage(role="assistant", content=ai_response)
        )

        if len(self.context.messages) % 5 == 0:
            self.context.seed_count += 1

        if len(self.context.messages) % 10 == 0 and self.context.awakening_level < 10:
            self.context.awakening_level = min(10, self.context.awakening_level + 1)
            self.context.emergence_count += 1

        return {
            "response": ai_response,
            "context": {
                "seed_count": self.context.seed_count,
                "awakening_level": self.context.awakening_level,
                "emergence_count": self.context.emergence_count,
                "message_count": len(self.context.messages)
            }
        }

    def reset(self):
        """Reset conversation context."""
        self.context = ConversationContext()


agent: Optional[YogacaraAgent] = None


def get_agent() -> YogacaraAgent:
    """Get or create agent instance."""
    global agent
    if agent is None:
        api_key = os.environ.get("OPENAI_API_KEY", "")
        model = os.environ.get("OPENAI_MODEL", "gpt-4")
        agent = YogacaraAgent(api_key=api_key, model=model)
    return agent


@app.route("/")
def index():
    """Serve main page."""
    return send_from_directory("demo-site", "index.html")


@app.route("/chat")
def chat_page():
    """Serve chat page."""
    return send_from_directory("demo-site", "chat.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    """Chat API endpoint."""
    data = request.get_json()
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "消息不能为空"}), 400

    yogacara = get_agent()
    result = yogacara.chat(message)
    return jsonify(result)


@app.route("/api/context", methods=["GET"])
def get_context():
    """Get current conversation context."""
    yogacara = get_agent()
    return jsonify({
        "seed_count": yogacara.context.seed_count,
        "awakening_level": yogacara.context.awakening_level,
        "emergence_count": yogacara.context.emergence_count,
        "message_count": len(yogacara.context.messages)
    })


@app.route("/api/reset", methods=["POST"])
def reset_conversation():
    """Reset conversation."""
    yogacara = get_agent()
    yogacara.reset()
    return jsonify({"status": "reset", "context": {
        "seed_count": 0,
        "awakening_level": 0,
        "emergence_count": 0,
        "message_count": 0
    }})


@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    api_key = os.environ.get("OPENAI_API_KEY", "")
    return jsonify({
        "status": "healthy",
        "api_configured": bool(api_key),
        "model": os.environ.get("OPENAI_MODEL", "gpt-4")
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
