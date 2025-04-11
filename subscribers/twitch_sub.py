# subscribers/twitch_sub.py (updating to handle additional events)

from typing import Dict, Any

from event_bus.bus import event_bus
from core.logging import get_logger
from core.errors import handle_error, NetworkError
from core.config import config
from publishers.twitch_pub import twitch_pub

logger = get_logger("twitch_sub")


class TwitchEventHandler:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.channel = config.get('CHANNEL', '')
        self.enabled = config.get_boolean('TWITCH_ENABLED', True)

    def subscribe(self):
        if not self.enabled:
            logger.info("Twitch handler is disabled")
            return

        self.event_bus.subscribe("twitch_message", self._handle_message)
        self.event_bus.subscribe("twitch_ready", self._handle_ready)
        self.event_bus.subscribe("twitch_join", self._handle_join)
        self.event_bus.subscribe("twitch_part", self._handle_part)
        self.event_bus.subscribe(
            "twitch_subscription", self._handle_subscription)
        self.event_bus.subscribe(
            "twitch_subscription_gift", self._handle_subscription_gift)
        self.event_bus.subscribe("twitch_bits", self._handle_bits)
        self.event_bus.subscribe("twitch_follow", self._handle_follow)
        self.event_bus.subscribe("twitch_raid", self._handle_raid)
        self.event_bus.subscribe(
            "twitch_channel_point_redemption", self._handle_channel_point_redemption)
        self.event_bus.subscribe("send_twitch_message", self._send_message)

        logger.info("Twitch handler subscribed to events")

    def _handle_message(self, data: Dict[str, Any]):
        try:
            author = data.get("author", {})
            username = author.get("name", "unknown")
            content = data.get("content", "")
            logger.info(f"[{username}]: {content}")

            # Additional message processing logic can be added here
        except Exception as e:
            handle_error(e, {"event": "twitch_message", "data": data})

    def _handle_ready(self, data: Dict[str, Any]):
        try:
            bot_user = data.get("bot_user", "unknown")
            logger.info(f"Twitch bot ready: {bot_user}")

            # Optional: Send a startup message to channel
            # if self.channel:
            #     self._send_message(
            #         {"channel": self.channel, "content": f"I'm live, bitches!"})
        except Exception as e:
            handle_error(e, {"event": "twitch_ready", "data": data})

    def _handle_join(self, data: Dict[str, Any]):
        try:
            channel = data.get("channel", "unknown")
            user = data.get("user", "unknown")
            logger.debug(f"User joined: {user} in {channel}")
        except Exception as e:
            handle_error(e, {"event": "twitch_join", "data": data})

    def _handle_part(self, data: Dict[str, Any]):
        try:
            channel = data.get("channel", "unknown")
            user = data.get("user", "unknown")
            logger.debug(f"User left: {user} from {channel}")
        except Exception as e:
            handle_error(e, {"event": "twitch_part", "data": data})

    def _handle_subscription(self, data: Dict[str, Any]):
        try:
            user = data.get("user", {})
            username = user.get("name", "unknown")
            channel = data.get("channel", "unknown")
            sub_plan = data.get("sub_plan", "")
            message = data.get("message", "")
            is_gift = data.get("is_gift", False)
            months = data.get("months", 1)

            sub_plan_name = "Tier 1"
            if sub_plan == "2000":
                sub_plan_name = "Tier 2"
            elif sub_plan == "3000":
                sub_plan_name = "Tier 3"
            elif sub_plan == "Prime":
                sub_plan_name = "Prime"

            logger.info(
                f"Subscription: {username} subscribed to {channel} with {sub_plan_name}")

            if is_gift:
                logger.info(f"This was a gifted subscription")
            elif months > 1:
                logger.info(f"This is a resubscription for {months} months")

            if message:
                logger.info(f"Sub message: {message}")

            # Send a thank you message
            if self.channel and not is_gift:
                tier_text = f"{sub_plan_name} " if sub_plan_name != "Tier 1" else ""
                if months > 1:
                    self._send_message({
                        "channel": self.channel,
                        "content": f"Thanks for the {tier_text}resub for {months} months, @{username}!"
                    })
                else:
                    self._send_message({
                        "channel": self.channel,
                        "content": f"Thanks for the {tier_text}sub, @{username}!"
                    })

        except Exception as e:
            handle_error(e, {"event": "twitch_subscription", "data": data})

    def _handle_subscription_gift(self, data: Dict[str, Any]):
        try:
            gifter = data.get("gifter", {})
            gifter_name = gifter.get("name", "unknown")
            channel = data.get("channel", "unknown")
            count = data.get("count", 1)
            sub_plan = data.get("sub_plan", "")
            recipients = data.get("recipients", [])

            sub_plan_name = "Tier 1"
            if sub_plan == "2000":
                sub_plan_name = "Tier 2"
            elif sub_plan == "3000":
                sub_plan_name = "Tier 3"

            logger.info(
                f"Sub Gift: {gifter_name} gifted {count} {sub_plan_name} subs to {channel}")

            if recipients:
                recipient_names = [r.get("name", "unknown")
                                   for r in recipients]
                logger.info(f"Recipients: {', '.join(recipient_names)}")

            # Send a thank you message
            if self.channel:
                tier_text = f"{sub_plan_name} " if sub_plan_name != "Tier 1" else ""
                if count == 1 and recipients:
                    self._send_message({
                        "channel": self.channel,
                        "content": f"Thanks for gifting a {tier_text}sub to {recipients[0].get('name', 'someone')}, @{gifter_name}!"
                    })
                else:
                    self._send_message({
                        "channel": self.channel,
                        "content": f"Thanks for gifting {count} {tier_text}subs, @{gifter_name}!"
                    })

        except Exception as e:
            handle_error(
                e, {"event": "twitch_subscription_gift", "data": data})

    def _handle_bits(self, data: Dict[str, Any]):
        try:
            user = data.get("user", {})
            username = user.get("name", "unknown")
            bits_used = data.get("bits_used", 0)
            channel = data.get("channel", "unknown")
            message = data.get("message", "")

            logger.info(
                f"Bits: {username} cheered {bits_used} bits in {channel}")
            if message:
                logger.info(f"Cheer message: {message}")

            # Send a thank you message
            if self.channel:
                self._send_message({
                    "channel": self.channel,
                    "content": f"Thanks for the {bits_used} bits, @{username}!"
                })

            # Check if we need to trigger any actions based on bits amount
            from db.database import db
            try:
                bits_action = db.fetchone(
                    "SELECT action_sequence_id FROM twitch_bits WHERE bits = ?",
                    (bits_used,)
                )

                if bits_action and bits_action.get('action_sequence_id'):
                    logger.info(
                        f"Found action sequence {bits_action['action_sequence_id']} for {bits_used} bits")
                    # Update the bits usage counter
                    db.execute(
                        "UPDATE twitch_bits SET uses = uses + 1 WHERE bits = ?",
                        (bits_used,)
                    )

                    # TODO: Trigger the action sequence
                    # This would be handled by the OBS connector/subscriber

            except Exception as db_error:
                logger.error(f"Error checking bits actions: {db_error}")

        except Exception as e:
            handle_error(e, {"event": "twitch_bits", "data": data})

    def _handle_follow(self, data: Dict[str, Any]):
        try:
            user = data.get("user", {})
            username = user.get("name", "unknown")
            channel = data.get("channel", "unknown")

            logger.info(f"Follow: {username} followed {channel}")

            # Optional: Send a thank you message
            if self.channel:
                self._send_message({
                    "channel": self.channel,
                    "content": f"Thanks for the follow, @{username}!"
                })

        except Exception as e:
            handle_error(e, {"event": "twitch_follow", "data": data})

    def _handle_raid(self, data: Dict[str, Any]):
        try:
            raider = data.get("raider", {})
            raider_name = raider.get("name", "unknown")
            channel = data.get("channel", "unknown")
            viewer_count = data.get("viewer_count", 0)

            logger.info(
                f"Raid: {raider_name} raided {channel} with {viewer_count} viewers")

            # Send a welcome message
            if self.channel:
                self._send_message({
                    "channel": self.channel,
                    "content": f"Thanks for the raid with {viewer_count} viewers, @{raider_name}! Welcome raiders!"
                })

        except Exception as e:
            handle_error(e, {"event": "twitch_raid", "data": data})

    def _handle_channel_point_redemption(self, data: Dict[str, Any]):
        try:
            user = data.get("user", {})
            username = user.get("name", "unknown")
            channel = data.get("channel", "unknown")
            reward = data.get("reward", {})
            reward_title = reward.get("title", "unknown")

            logger.info(
                f"Channel Point Redemption: {username} redeemed '{reward_title}' in {channel}")

            # Use the channel points service to handle the redemption
            from utils.channel_points_service import channel_points_service
            channel_points_service.handle_redemption(data)

        except Exception as e:
            handle_error(
                e, {"event": "twitch_channel_point_redemption", "data": data})

    def _send_message(self, data: Dict[str, Any]):
        try:
            channel = data.get("channel", self.channel)
            content = data.get("content", "")

            if not channel or not content:
                logger.warning(
                    "Cannot send message: missing channel or content")
                return

            result = twitch_pub.send_message(channel, content)
            if not result:
                logger.warning(f"Failed to send message to {channel}")
        except Exception as e:
            handle_error(NetworkError(f"Failed to send Twitch message: {str(e)}"),
                         {"channel": data.get("channel"), "content": data.get("content")})


# Singleton instance
twitch_sub = TwitchEventHandler(event_bus)
