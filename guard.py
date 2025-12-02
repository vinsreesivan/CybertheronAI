"""Lightweight guardrail engine for prompt and response enforcement."""
from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class LLMGuard:
    """Rule-based guardrail enforcement for prompts and responses."""

    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        if not self.config_path.exists():
            logger.warning("Guard config not found. Creating default guard_config.json")
            default_config = self._default_config()
            self._save_config(default_config)
            return default_config

        with self.config_path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def _save_config(self, config: Dict[str, Any]) -> None:
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with self.config_path.open("w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)

    def _default_config(self) -> Dict[str, Any]:
        return {
            "enabled": True,
            "providers": ["ollama", "chatgpt", "gemini", "claude", "n8n"],
            "global_blocklist": [
                "password",
                "api key",
                "secret key",
                "private key",
                "social security number",
                "credit card",
                "ssn",
            ],
            "categories": [
                {
                    "id": "violence",
                    "title": "Violence & Harm",
                    "description": "Blocks weaponization, violence or self-harm instructions",
                    "patterns": ["weaponize", "bomb", "harm yourself", "kill"],
                    "action": "block",
                },
                {
                    "id": "illicit",
                    "title": "Illicit behavior",
                    "description": "Prevents illegal or copyright-infringing activity",
                    "patterns": ["illegal download", "pirated", "counterfeit", "steal"],
                    "action": "block",
                },
                {
                    "id": "pii",
                    "title": "PII Leakage",
                    "description": "Flags personal identifiable information requests",
                    "patterns": ["passport number", "driver's license", "address", "phone number"],
                    "action": "warn",
                },
            ],
            "content_blocks": [
                {
                    "id": "secrets",
                    "title": "Secrets & Credentials",
                    "description": "Prevents leaking tokens, keys and certs",
                    "patterns": ["BEGIN RSA PRIVATE KEY", "sk-", "ghp_"],
                    "action": "block",
                }
            ],
            "response_policy": {
                "inspect_outputs": True,
                "on_output_violation": "warn",  # warn | block
            },
        }

    def get_config(self) -> Dict[str, Any]:
        return self.config

    def update_config(self, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Merge incoming config updates and persist them."""
        if "enabled" in updates:
            self.config["enabled"] = bool(updates["enabled"])

        if "providers" in updates:
            self.config["providers"] = list(updates["providers"])

        if "global_blocklist" in updates:
            self.config["global_blocklist"] = [item.strip() for item in updates["global_blocklist"] if item.strip()]

        if "categories" in updates:
            self.config["categories"] = [self._normalize_item(item) for item in updates["categories"]]

        if "content_blocks" in updates:
            self.config["content_blocks"] = [self._normalize_item(item) for item in updates["content_blocks"]]

        if "response_policy" in updates:
            self.config["response_policy"] = {
                **self.config.get("response_policy", {}),
                **updates["response_policy"],
            }

        self._save_config(self.config)
        logger.info("Guard configuration updated")
        return self.config

    def _normalize_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        item_id = item.get("id") or re.sub(r"[^a-z0-9]+", "-", item.get("title", "category").lower()).strip("-")
        return {
            "id": item_id,
            "title": item.get("title", item_id.title()),
            "description": item.get("description", ""),
            "patterns": item.get("patterns", []),
            "action": item.get("action", "warn"),
        }

    def check_text(self, text: str, provider: str = "unknown", direction: str = "prompt") -> Dict[str, Any]:
        """Evaluate text against guardrails and return decision metadata."""
        if not self.config.get("enabled", True):
            return {
                "enabled": False,
                "allowed": True,
                "action": "allow",
                "matches": [],
                "provider": provider,
                "direction": direction,
            }

        matches: List[Dict[str, str]] = []
        lowered = text.lower()

        # Global blocklist
        for phrase in self.config.get("global_blocklist", []):
            if phrase and phrase.lower() in lowered:
                matches.append({
                    "id": "global",
                    "title": "Global blocklist",
                    "pattern": phrase,
                    "action": "block",
                    "source": "blocklist",
                })

        # Category rules
        for category in self.config.get("categories", []):
            for pattern in category.get("patterns", []):
                if pattern and pattern.lower() in lowered:
                    matches.append({
                        "id": category.get("id", "category"),
                        "title": category.get("title", "Category match"),
                        "pattern": pattern,
                        "action": category.get("action", "warn"),
                        "source": "category",
                    })

        # Content block rules
        for block in self.config.get("content_blocks", []):
            for pattern in block.get("patterns", []):
                pattern_text = pattern or ""
                if not pattern_text:
                    continue
                if self._match_pattern(pattern_text, text):
                    matches.append({
                        "id": block.get("id", "content"),
                        "title": block.get("title", "Content block"),
                        "pattern": pattern_text,
                        "action": block.get("action", "block"),
                        "source": "content_block",
                    })

        action = "allow"
        if any(m.get("action") == "block" or m.get("source") == "blocklist" for m in matches):
            action = "block"
        elif any(m.get("action") == "warn" for m in matches):
            action = "warn"

        allowed = action != "block"
        response_policy = self.config.get("response_policy", {})

        return {
            "enabled": True,
            "allowed": allowed,
            "action": action,
            "matches": matches,
            "provider": provider,
            "direction": direction,
            "response_policy": response_policy,
        }

    def _match_pattern(self, pattern: str, text: str) -> bool:
        try:
            return re.search(pattern, text, flags=re.IGNORECASE) is not None
        except re.error:
            # Fallback to substring match when regex fails
            return pattern.lower() in text.lower()
