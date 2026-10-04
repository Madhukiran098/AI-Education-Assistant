from datetime import datetime
from typing import Dict, Any

PAYMENT_AMOUNT = 150.0

def verify_student_payment(
    student_id: str,
    payment_status: bool,
    amount: float = 0.0,
) -> Dict[str, Any]:

    student_id = student_id.strip()

    if not student_id:
        return {
            "verified": False,
            "status": "invalid_student",
            "message": "Student ID is required.",
        }

    if not payment_status:
        return {
            "verified": False,
            "status": "payment_required",
            "amount": PAYMENT_AMOUNT,
            "message": "Personalized career roadmap requires a ₹150 payment.",
        }

    if float(amount) < PAYMENT_AMOUNT:
        return {
            "verified": False,
            "status": "insufficient_payment",
            "amount": PAYMENT_AMOUNT,
            "message": "Payment amount is less than the required ₹150.",
        }

    return {
        "verified": True,
        "status": "paid",
        "student_id": student_id,
        "amount": PAYMENT_AMOUNT,
        "verified_at": datetime.now().isoformat(),
        "message": "Student payment verified successfully.",
    }


if __name__ == "__main__":
    print("Paid:", verify_student_payment("STU001", True, 150))
    print("Free:", verify_student_payment("STU002", False, 0))


