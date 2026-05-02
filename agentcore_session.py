from __future__ import annotations

import asyncio
import datetime as dt
from typing import Any, Optional

from agents.items import TResponseInputItem
from agents.memory.session import SessionABC
from bedrock_agentcore.memory import MemoryClient


class AgentCoreSession(SessionABC):
    def __init__(
        self,
        memory_id: str,
        session_id: str,
        actor_id: str,
        region: Optional[str] = None,
    ) -> None:
        self.memory_id = memory_id
        self.session_id = session_id
        self.actor_id = actor_id
        self.client = MemoryClient(region_name=region)

    async def get_items(self, limit: int | None = None) -> list[TResponseInputItem]:
        events = await asyncio.to_thread(
            self.client.list_events,
            memory_id=self.memory_id,
            actor_id=self.actor_id,
            session_id=self.session_id,
            max_results=limit or 100,
            include_payload=True,
        )

        items: list[TResponseInputItem] = []

        for event in events:
            for payload in event.get("payload", []):
                conv = payload.get("conversational")
                if not conv:
                    continue

                role = self._to_openai_role(conv.get("role"))
                text = (conv.get("content") or {}).get("text")

                if text:
                    items.append(
                        {
                            "role": role,
                            "content": [
                                {
                                    "type": self._content_type(role),
                                    "text": text,
                                }
                            ],
                        }
                    )

        return items[-limit:] if limit else items

    async def add_items(self, items: list[TResponseInputItem]) -> None:
        for item in items:
            text, role = self._extract_text_and_role(item)

            if not text:
                continue

            await asyncio.to_thread(
                self.client.create_event,
                memory_id=self.memory_id,
                actor_id=self.actor_id,
                session_id=self.session_id,
                messages=[(text, role)],
                event_timestamp=dt.datetime.utcnow(),
            )

    async def pop_item(self) -> TResponseInputItem | None:
        items = await self.get_items()
        return items[-1] if items else None

    async def clear_session(self) -> None:
        # AgentCore events are immutable.
        # For a real reset, use a new session_id.
        return None

    @staticmethod
    def _extract_text_and_role(item: TResponseInputItem) -> tuple[str, str]:
        role = item.get("role", "assistant") if isinstance(item, dict) else "assistant"
        content = item.get("content") if isinstance(item, dict) else None

        text = ""

        if isinstance(content, str):
            text = content
        elif isinstance(content, list):
            for part in content:
                if isinstance(part, dict) and isinstance(part.get("text"), str):
                    text = part["text"]
                    break

        agentcore_role = "USER" if role == "user" else "ASSISTANT"
        return text, agentcore_role

    @staticmethod
    def _to_openai_role(role: Optional[str]) -> str:
        return "user" if role == "USER" else "assistant"

    @staticmethod
    def _content_type(role: str) -> str:
        return "input_text" if role == "user" else "output_text"
