"""Custom exceptions for tokmon."""


class BudgetExceeded(RuntimeError):
    """Raised when a tracked function exceeds its token/cost budget."""

    def __init__(self, feature: str, actual: float, limit: float, unit: str = "USD") -> None:
        self.feature = feature
        self.actual = actual
        self.limit = limit
        self.unit = unit
        super().__init__(
            f"Budget exceeded for '{feature}': "
            f"${actual:.4f} > ${limit:.4f}" if unit == "USD"
            else f"{actual:,} > {limit:,} tokens"
        )
