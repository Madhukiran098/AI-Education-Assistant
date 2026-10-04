from request_validation import (
    is_calculation_request,
    is_career_guidance_request,
)


def test_arithmetic_query_is_identified_for_m1_routing():
    assert is_calculation_request("calculate 20*30+20")
    assert is_calculation_request("What is 20 * 30 + 20?")


def test_career_requests_remain_on_m1_workflow():
    query = "Best career options after MPC with 85% marks"
    assert not is_calculation_request(query)
    assert is_career_guidance_request(query)


def test_calculation_and_unrelated_queries_do_not_open_career_cta():
    assert not is_career_guidance_request("calculate 20*30+20")
    assert not is_career_guidance_request("Summarize this meeting note")