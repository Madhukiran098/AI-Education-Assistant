import re


_CALCULATION_KEYWORD = re.compile(
    r"\b(calculate|calculation|compute|arithmetic|multiply|divide|"
    r"subtract|sum|average|equation)\b",
    re.IGNORECASE,
)
_ARITHMETIC_EXPRESSION = re.compile(
    r"\d+(?:\.\d+)?\s*[+*/×÷^%-]\s*\d+"
)
_CAREER_GUIDANCE_TERMS = re.compile(
    r"\b(career|careers|college|colleges|university|universities|"
    r"course|courses|job|jobs|profession|employment|roadmap|"
    r"MPC|engineering|degree|entrance exam|skills)\b",
    re.IGNORECASE,
)


def is_calculation_request(request: str) -> bool:
    text = str(request or "").strip()
    return bool(
        _CALCULATION_KEYWORD.search(text)
        or _ARITHMETIC_EXPRESSION.search(text)
    )


def is_career_guidance_request(request: str) -> bool:
    text = str(request or "").strip()
    return bool(
        text
        and not is_calculation_request(text)
        and _CAREER_GUIDANCE_TERMS.search(text)
    )