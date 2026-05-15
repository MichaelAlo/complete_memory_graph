from dataclasses import dataclass


@dataclass(frozen=True)
class TableConfig:
    business_key: list[str]
    required_fields: list[str]
    type_map: dict[str, type]
    codelist_maps: dict[str, dict[str, str]]


TABLE_CONFIG: dict[str, TableConfig] = {
    "policies": TableConfig(
        business_key=["policy_id"],
        required_fields=["policy_id", "product_code", "status", "inception_date"],
        type_map={"policy_id": int},
        codelist_maps={
            "status": {
                "A": "active",
                "L": "lapsed",
                "S": "surrendered",
                "M": "matured",
                "D": "death-claim",
            }
        },
    ),
    "customers": TableConfig(
        business_key=["customer_id"],
        required_fields=["customer_id", "status"],
        type_map={"customer_id": int},
        codelist_maps={},
    ),
    "products": TableConfig(
        business_key=["product_id"],
        required_fields=["product_id", "product_code", "product_type"],
        type_map={"product_id": int},
        codelist_maps={},
    ),
}
