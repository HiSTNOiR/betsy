from db.database import db
from core.logging import get_logger

logger = get_logger("user_service")


def get_user_from_db(twitch_user_id):
    try:
        user = db.fetchone(
            "SELECT * FROM users WHERE twitch_user_id = ?",
            (twitch_user_id,)
        )
        return user
    except Exception as e:
        logger.error(f"Error fetching user from database: {e}")
        return None


def enrich_user_data(user_data):
    if not user_data or "id" not in user_data:
        return user_data

    db_user = get_user_from_db(user_data["id"])
    if db_user:
        # Create a new dict to avoid modifying the original
        enriched_data = dict(user_data)

        # Add the is_bot_admin flag based on DB rank
        enriched_data["is_bot_admin"] = db_user.get("rank") == "bot_admin"

        # Add any other relevant fields from DB
        enriched_data["db_rank"] = db_user.get("rank")
        enriched_data["db_points"] = db_user.get("points", 0)

        return enriched_data
    return user_data
