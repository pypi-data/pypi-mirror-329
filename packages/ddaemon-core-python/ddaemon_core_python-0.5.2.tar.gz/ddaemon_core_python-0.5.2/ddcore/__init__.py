"""(C) 2013-2025 Copycat Software, LLC. All Rights Reserved."""

__version__ = "0.5.2"


def enum(**args):
    """Enum."""
    return type("Enum", (), args)
