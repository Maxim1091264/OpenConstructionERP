"""Review status definitions.

This module is intentionally placeholder-only and does not enforce persistence.
"""

from enum import Enum


class ReviewStatus(str, Enum):
    draft = "draft"
    pending_review = "pending_review"
    approved_for_grandsmeta = "approved_for_grandsmeta"
    rejected = "rejected"
