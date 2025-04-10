from typing import Dict, Any, Optional

from events.base import BaseEvent


class TwitchEvent(BaseEvent):
    def __init__(self, data: Dict[str, Any]):
        super().__init__(data)
        self.platform = "twitch"

    def _validate(self):
        if not self.data:
            raise ValueError("Event data cannot be empty")

    def _handle(self):
        pass


class TwitchReadyEvent(TwitchEvent):
    def _validate(self):
        super()._validate()
        if "bot_user" not in self.data:
            raise ValueError("Missing bot_user in ready event data")

    def _handle(self):
        return {
            "type": "twitch_ready",
            "bot_user": self.data["bot_user"]
        }


class TwitchMessageEvent(TwitchEvent):
    def _validate(self):
        super()._validate()
        required_fields = ["author", "content", "channel"]
        for field in required_fields:
            if field not in self.data:
                raise ValueError(f"Missing {field} in message event data")

    def _handle(self):
        return {
            "type": "twitch_message",
            "author": self.data["author"],
            "content": self.data["content"],
            "channel": self.data["channel"],
            "id": self.data.get("id"),
            "timestamp": self.data.get("timestamp")
        }


class TwitchJoinEvent(TwitchEvent):
    def _validate(self):
        super()._validate()
        if "channel" not in self.data or "user" not in self.data:
            raise ValueError("Missing channel or user in join event data")

    def _handle(self):
        return {
            "type": "twitch_join",
            "channel": self.data["channel"],
            "user": self.data["user"]
        }


class TwitchPartEvent(TwitchEvent):
    def _validate(self):
        super()._validate()
        if "channel" not in self.data or "user" not in self.data:
            raise ValueError("Missing channel or user in part event data")

    def _handle(self):
        return {
            "type": "twitch_part",
            "channel": self.data["channel"],
            "user": self.data["user"]
        }


class TwitchSubscriptionEvent(TwitchEvent):
    def _validate(self):
        super()._validate()

    def _handle(self):
        return {
            "type": "twitch_subscription",
            "data": self.data
        }


class SendTwitchMessageEvent(TwitchEvent):
    def _validate(self):
        super()._validate()
        if "content" not in self.data:
            raise ValueError("Missing content in send message event data")
        if "channel" not in self.data:
            self.data["channel"] = None  # Will use default channel

    def _handle(self):
        return {
            "type": "send_twitch_message",
            "channel": self.data["channel"],
            "content": self.data["content"]
        }
