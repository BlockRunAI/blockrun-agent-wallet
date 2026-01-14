"""
BlockRun Spending Tracker.

Persistent spending tracking with budget enforcement.
Stores spending data in ~/.blockrun/spending.json.
"""

import json
import os
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple


class SpendingTracker:
    """Persistent spending tracker with budget enforcement."""

    MAX_HISTORY = 100

    def __init__(self):
        self.dir = Path.home() / ".blockrun"
        self.file = self.dir / "spending.json"
        self.data = self._load()

    def _today(self) -> str:
        """Get today's date string."""
        return datetime.now().strftime("%Y-%m-%d")

    def _now(self) -> str:
        """Get current timestamp."""
        return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    def _new_session(self) -> dict:
        """Create a fresh session."""
        return {
            "session_id": self._today(),
            "budget_limit": None,
            "spending": {
                "total_usd": 0.0,
                "calls": 0
            },
            "history": []
        }

    def _load(self) -> dict:
        """Load or create fresh session (resets daily)."""
        # Ensure directory exists
        self.dir.mkdir(parents=True, exist_ok=True)

        if self.file.exists():
            try:
                data = json.loads(self.file.read_text())
                # Reset if new day
                if data.get("session_id", "")[:10] != self._today():
                    # Preserve budget limit across days
                    new_data = self._new_session()
                    new_data["budget_limit"] = data.get("budget_limit")
                    return new_data
                return data
            except (json.JSONDecodeError, KeyError):
                # Corrupted file - start fresh
                return self._new_session()

        return self._new_session()

    def _save(self):
        """Atomic save to prevent corruption."""
        self.dir.mkdir(parents=True, exist_ok=True)

        # Write to temp file first
        fd, temp_path = tempfile.mkstemp(dir=self.dir, suffix=".json")
        try:
            with os.fdopen(fd, 'w') as f:
                json.dump(self.data, f, indent=2)
            # Atomic rename
            os.replace(temp_path, self.file)
        except Exception:
            # Clean up temp file on error
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            raise

    def record(self, model: str, cost: float):
        """Record a call and save."""
        self.data["spending"]["total_usd"] += cost
        self.data["spending"]["calls"] += 1

        # Add to history
        self.data["history"].append({
            "timestamp": self._now(),
            "model": model,
            "cost": cost
        })

        # Cap history size
        if len(self.data["history"]) > self.MAX_HISTORY:
            self.data["history"] = self.data["history"][-self.MAX_HISTORY:]

        self._save()

    def check_budget(self) -> Tuple[bool, float]:
        """
        Check if within budget.

        Returns:
            Tuple of (within_budget, remaining).
            If no budget set, returns (True, float('inf')).
        """
        limit = self.data.get("budget_limit")
        if limit is None:
            return True, float('inf')

        spent = self.data["spending"]["total_usd"]
        remaining = limit - spent

        # Use tolerance for floating-point comparison (0.0001 = 0.01 cent)
        EPSILON = 0.0001
        within_budget = remaining > -EPSILON

        return within_budget, max(0, remaining)

    def set_budget(self, amount: float):
        """Set daily budget limit."""
        self.data["budget_limit"] = amount
        self._save()

    def clear_budget(self):
        """Remove budget limit."""
        self.data["budget_limit"] = None
        self._save()

    def get_total(self) -> float:
        """Get total spent this session."""
        return self.data["spending"]["total_usd"]

    def get_calls(self) -> int:
        """Get number of calls this session."""
        return self.data["spending"]["calls"]

    def get_limit(self) -> Optional[float]:
        """Get current budget limit (None if no limit)."""
        return self.data.get("budget_limit")

    def get_history(self, limit: int = 10) -> list:
        """Get recent call history."""
        return self.data["history"][-limit:]

    def get_session_id(self) -> str:
        """Get current session ID (date)."""
        return self.data.get("session_id", self._today())
