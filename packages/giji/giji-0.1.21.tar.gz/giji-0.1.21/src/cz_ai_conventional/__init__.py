"""
Custom Commitizen plugin that uses Google Gemini to generate conventional commit messages.
"""

from .version import VERSION

__version__ = VERSION


def AIConventionalCz(config):
    """Factory function for AIConventionalCz class"""
    from .cz_ai_conventional import AIConventionalCz as CzClass

    return CzClass(config)


__all__ = ["AIConventionalCz", "__version__"]
