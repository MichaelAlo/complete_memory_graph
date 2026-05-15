from src.lib.run_context import RunContext


def test_run_id_is_unique():
    a = RunContext()
    b = RunContext()
    assert a.run_id != b.run_id


def test_as_dict_contains_required_fields():
    ctx = RunContext(extract_cut="2026-05-15", release_tag="v0.1.0")
    d = ctx.as_dict()
    assert d["extract_cut"] == "2026-05-15"
    assert d["release_tag"] == "v0.1.0"
    assert "run_id" in d
    assert "started_at" in d


def test_snapshot_requires_release_tag():
    ctx = RunContext()
    assert ctx.release_tag is None
