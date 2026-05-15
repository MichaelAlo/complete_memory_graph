class StandardisationGateError(Exception):
    def __init__(self, table: str, failed_checks: list[str]) -> None:
        self.table = table
        self.failed_checks = failed_checks
        super().__init__(f"Quality gate failed for {table!r}: {', '.join(failed_checks)}")
