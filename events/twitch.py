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


class TwitchBitsEvent(TwitchEvent):
    def _validate(self):
        super()._validate()
        required_fields = ["user", "bits_used", "channel"]
        for field in required_fields:
            if field not in self.data:
                raise ValueError(f"Missing {field} in bits event data")

    def _handle(self):
        return {
            "type": "twitch_bits",
            "user": self.data["user"],
            "bits_used": self.data["bits_used"],
            "channel": self.data["channel"],
            "message": self.data.get("message", ""),
            "timestamp": self.data.get("timestamp")
        }


class TwitchSubscriptionEvent(TwitchEvent):
    def _validate(self):
        super()._validate()
        required_fields = ["user", "channel", "sub_plan"]
        for field in required_fields:
            if field not in self.data:
                raise ValueError(f"Missing {field} in subscription event data")

    def _handle(self):
        return {
            "type": "twitch_subscription",
            "user": self.data["user"],
            "channel": self.data["channel"],
            "sub_plan": self.data["sub_plan"],
            "message": self.data.get("message", ""),
            "is_gift": self.data.get("is_gift", False),
            "months": self.data.get("months", 1),
            "timestamp": self.data.get("timestamp")
        }


class TwitchSubscriptionGiftEvent(TwitchEvent):
    def _validate(self):
        super()._validate()
        required_fields = ["gifter", "channel", "count", "sub_plan"]
        for field in required_fields:
            if field not in self.data:
                raise ValueError(
                    f"Missing {field} in subscription gift event data")

    def _handle(self):
        return {
            "type": "twitch_subscription_gift",
            "gifter": self.data["gifter"],
            "channel": self.data["channel"],
            "count": self.data["count"],
            "sub_plan": self.data["sub_plan"],
            "recipients": self.data.get("recipients", []),
            "timestamp": self.data.get("timestamp")
        }


class TwitchFollowEvent(TwitchEvent):
    def _validate(self):
        super()._validate()
        required_fields = ["user", "channel"]
        for field in required_fields:
            if field not in self.data:
                raise ValueError(f"Missing {field} in follow event data")

    def _handle(self):
        return {
            "type": "twitch_follow",
            "user": self.data["user"],
            "channel": self.data["channel"],
            "timestamp": self.data.get("timestamp")
        }


class TwitchRaidEvent(TwitchEvent):
    def _validate(self):
        super()._validate()
        required_fields = ["raider", "channel", "viewer_count"]
        for field in required_fields:
            if field not in self.data:
                raise ValueError(f"Missing {field} in raid event data")

    def _handle(self):
        return {
            "type": "twitch_raid",
            "raider": self.data["raider"],
            "channel": self.data["channel"],
            "viewer_count": self.data["viewer_count"],
            "timestamp": self.data.get("timestamp")
        }


class TwitchChannelPointRedemptionEvent(TwitchEvent):
    def _validate(self):
        super()._validate()
        required_fields = ["user", "channel", "reward"]
        for field in required_fields:
            if field not in self.data:
                raise ValueError(
                    f"Missing {field} in channel point redemption event data")

    def _handle(self):
        return {
            "type": "twitch_channel_point_redemption",
            "user": self.data["user"],
            "channel": self.data["channel"],
            "reward": self.data["reward"],
            "input": self.data.get("input", ""),
            "status": self.data.get("status", "fulfilled"),
            "timestamp": self.data.get("timestamp")
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
