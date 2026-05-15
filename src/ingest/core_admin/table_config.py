from dataclasses import dataclass


@dataclass(frozen=True)
class TableConfig:
    pk_col: str
    updated_at_col: str
    pii_fields: frozenset[str]
    source_table: str
    raw_table: str


TABLES: dict[str, TableConfig] = {
    "policies": TableConfig(
        pk_col="policy_id",
        updated_at_col="updated_at",
        pii_fields=frozenset(),
        source_table="policies",
        raw_table="policies",
    ),
    "customers": TableConfig(
        pk_col="customer_id",
        updated_at_col="updated_at",
        pii_fields=frozenset({"name", "date_of_birth", "id_number", "email", "phone"}),
        source_table="customers",
        raw_table="customers",
    ),
    "products": TableConfig(
        pk_col="product_id",
        updated_at_col="updated_at",
        pii_fields=frozenset(),
        source_table="products",
        raw_table="products",
    ),
}
