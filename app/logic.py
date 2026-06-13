"""Pure business logic of the application.

Keeping the logic away from the HTTP layer makes it easy to write fast
unit tests (without starting a server).
"""

from decimal import ROUND_HALF_UP, Decimal


def calculate_gross(net: float, vat_rate: float) -> float:
    """Calculate the gross amount from the net amount and a VAT rate (in percent).

    >>> calculate_gross(100, 23)
    123.0
    """
    if net < 0:
        raise ValueError("Net amount cannot be negative")
    if vat_rate < 0:
        raise ValueError("VAT rate cannot be negative")

    gross = Decimal(str(net)) * (Decimal("1") + Decimal(str(vat_rate)) / Decimal("100"))
    gross = gross.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return float(gross)