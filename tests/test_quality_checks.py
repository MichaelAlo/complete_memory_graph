from src.quality.checks import QualityResult, run_all


def test_run_all_passes_when_all_pass():
    checks = [QualityResult("a", True), QualityResult("b", True)]
    assert run_all(checks) is True


def test_run_all_fails_when_any_fails():
    checks = [QualityResult("a", True), QualityResult("b", False, "2 nulls")]
    assert run_all(checks) is False


def test_quality_result_detail_optional():
    r = QualityResult("row_count:nexus_raw.policy", True)
    assert r.detail is None
