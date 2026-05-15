from src.standardise.pipeline import deduplicate, harmonise_codelist


def test_deduplicate_keeps_latest():
    rows = [
        {"id": "1", "updated_at": "2026-01-01", "value": "old"},
        {"id": "1", "updated_at": "2026-03-01", "value": "new"},
    ]
    result = deduplicate(rows, key_fields=["id"])
    assert len(result) == 1
    assert result[0]["value"] == "new"


def test_deduplicate_preserves_distinct_keys():
    rows = [
        {"id": "1", "updated_at": "2026-01-01", "value": "a"},
        {"id": "2", "updated_at": "2026-01-01", "value": "b"},
    ]
    result = deduplicate(rows, key_fields=["id"])
    assert len(result) == 2


def test_harmonise_codelist_maps_known_value():
    mapping = {"M": "MALE", "F": "FEMALE"}
    assert harmonise_codelist("M", mapping) == "MALE"


def test_harmonise_codelist_passes_through_unknown():
    mapping = {"M": "MALE"}
    assert harmonise_codelist("X", mapping) == "X"
