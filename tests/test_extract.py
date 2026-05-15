from src.ingest.core_admin.extract import _mask_pii
from src.ingest.core_admin.table_config import TABLES


def test_pii_masking_replaces_known_fields() -> None:
    row = {
        "customer_id": 1,
        "name": "Alice Wong",
        "date_of_birth": "1980-01-01",
        "id_number": "A123456",
        "email": "alice@example.com",
        "phone": "+852 9000 0000",
        "status": "active",
    }
    pii = TABLES["customers"].pii_fields
    masked = _mask_pii(row, pii)
    assert masked["name"] == "***"
    assert masked["date_of_birth"] == "***"
    assert masked["id_number"] == "***"
    assert masked["email"] == "***"
    assert masked["phone"] == "***"


def test_pii_masking_preserves_non_pii_fields() -> None:
    row = {"customer_id": 42, "name": "Bob", "status": "active"}
    pii = TABLES["customers"].pii_fields
    masked = _mask_pii(row, pii)
    assert masked["customer_id"] == 42
    assert masked["status"] == "active"


def test_pii_masking_empty_pii_set_leaves_row_unchanged() -> None:
    row = {"policy_id": 99, "product_code": "UL01", "status": "in-force"}
    pii = TABLES["policies"].pii_fields
    masked = _mask_pii(row, pii)
    assert masked == row


def test_table_config_covers_expected_tables() -> None:
    assert "policies" in TABLES
    assert "customers" in TABLES
    assert "products" in TABLES


def test_customers_table_config_has_pii_fields() -> None:
    tcfg = TABLES["customers"]
    assert "name" in tcfg.pii_fields
    assert "email" in tcfg.pii_fields
    assert "id_number" in tcfg.pii_fields


def test_policies_table_config_has_no_pii_fields() -> None:
    tcfg = TABLES["policies"]
    assert len(tcfg.pii_fields) == 0
