from datetime import datetime
from typing import Dict, Any


ANNUAL_SUBSCRIPTION_FEE = 5000.0


COLLEGE_SUBSCRIPTIONS: Dict[str, Dict[str, Any]] = {
    "COL001": {
        "college_name": "Demo College",
        "is_active": True,
        "annual_fee": ANNUAL_SUBSCRIPTION_FEE,
    },
    "COL002": {
        "college_name": "Demo College 2",
        "is_active": True,
        "annual_fee": ANNUAL_SUBSCRIPTION_FEE,
    },
}


def verify_college_subscription(
    college_id: str,
) -> Dict[str, Any]:
    """
    Verify whether a college has an active annual subscription.
    """

    college_id = college_id.strip()

    subscription = COLLEGE_SUBSCRIPTIONS.get(college_id)

    if not subscription:
        return {
            "college_id": college_id,
            "verified": False,
            "status": "not_registered",
            "message": "College subscription was not found.",
        }

    if not subscription.get("is_active", False):
        return {
            "college_id": college_id,
            "verified": False,
            "status": "inactive",
            "message": "College subscription is inactive.",
        }

    return {
        "college_id": college_id,
        "verified": True,
        "status": "active",
        "college_name": subscription["college_name"],
        "annual_fee": subscription["annual_fee"],
        "verified_at": datetime.now().isoformat(),
        "message": "College subscription verified successfully.",
    }
