import pytest

from src.lib.run_context import RunContext
from src.snapshot.publisher import publish_snapshot


def test_requires_release_tag() -> None:
    ctx = RunContext()
    assert ctx.release_tag is None
    with pytest.raises(ValueError, match="release_tag"):
        publish_snapshot(ctx, None, "rpt_policy_in_force", "SELECT 1")  # type: ignore[arg-type]


def test_release_tag_present_does_not_raise_on_validation() -> None:
    ctx = RunContext(release_tag="v1.0.0")
    assert ctx.release_tag == "v1.0.0"


def test_snapshot_id_is_unique_across_calls() -> None:
    import uuid
    ids = {str(uuid.uuid4()) for _ in range(100)}
    assert len(ids) == 100


def test_run_context_release_tag_roundtrip() -> None:
    ctx = RunContext(release_tag="v2.3.0-rc1")
    assert ctx.release_tag == "v2.3.0-rc1"
    assert ctx.run_id != ""
