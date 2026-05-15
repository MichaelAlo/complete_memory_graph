from src.standardise.pipeline import _coerce, _gate, _harmonise, deduplicate, harmonise_codelist
from src.standardise.table_config import TABLE_CONFIG


def test_type_coercion_converts_string_id_to_int() -> None:
    row = {"policy_id": "42", "status": "active", "inception_date": "2023-01-01"}
    result = _coerce(row, {"policy_id": int})
    assert result["policy_id"] == 42
    assert isinstance(result["policy_id"], int)


def test_type_coercion_leaves_non_mapped_fields_unchanged() -> None:
    row = {"policy_id": "1", "status": "active"}
    result = _coerce(row, {"policy_id": int})
    assert result["status"] == "active"


def test_harmonise_maps_source_code_to_canonical() -> None:
    row = {"policy_id": 1, "status": "A"}
    policy_maps = TABLE_CONFIG["policies"].codelist_maps
    result = _harmonise(row, policy_maps)
    assert result["status"] == "active"


def test_harmonise_leaves_unknown_code_unchanged() -> None:
    row = {"policy_id": 1, "status": "X"}
    policy_maps = TABLE_CONFIG["policies"].codelist_maps
    result = _harmonise(row, policy_maps)
    assert result["status"] == "X"


def test_gate_blocks_empty_batch() -> None:
    failed = _gate([], ["policy_id", "status"])
    assert "row_count=0" in failed


def test_gate_blocks_null_required_field() -> None:
    rows = [
        {"policy_id": 1, "status": None, "product_code": "UL01", "inception_date": "2023-01-01"}
    ]
    failed = _gate(rows, ["policy_id", "status"])
    assert any("nulls:status" in f for f in failed)


def test_gate_passes_complete_batch() -> None:
    rows = [
        {"policy_id": 1, "status": "active", "product_code": "UL01", "inception_date": "2023-01-01"}
    ]
    failed = _gate(rows, ["policy_id", "status", "product_code", "inception_date"])
    assert failed == []


def test_deduplicate_keeps_most_recent() -> None:
    rows: list[dict[str, object]] = [
        {"policy_id": 1, "status": "lapsed", "updated_at": "2023-01-01"},
        {"policy_id": 1, "status": "active", "updated_at": "2023-06-01"},
    ]
    result = deduplicate(rows, ["policy_id"])
    assert len(result) == 1
    assert result[0]["status"] == "active"


def test_gate_error_null_required_field() -> None:
    rows = [
        {"policy_id": None, "status": "active", "product_code": "X", "inception_date": "2023-01-01"}
    ]
    failed = _gate(rows, ["policy_id"])
    assert failed


def test_harmonise_codelist_direct() -> None:
    assert harmonise_codelist("A", {"A": "active"}) == "active"
    assert harmonise_codelist("Z", {"A": "active"}) == "Z"
