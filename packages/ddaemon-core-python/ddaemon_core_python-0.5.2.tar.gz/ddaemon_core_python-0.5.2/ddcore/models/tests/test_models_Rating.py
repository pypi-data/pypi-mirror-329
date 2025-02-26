"""(C) 2013-2025 Copycat Software, LLC. All Rights Reserved."""

from django.test import TestCase

from ddcore.models import Rating


class RatingTestCase(TestCase):
    """Rating Model Test Class."""

    def setUp(self):
        """Constructor."""

    def test_success(self):
        """Test Case: Success."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Assertions.
        # ---------------------------------------------------------------------
        self.assertTrue(callable(Rating.pre_save))
        self.assertTrue(callable(Rating.post_save))
        self.assertTrue(callable(Rating.pre_delete))
        self.assertTrue(callable(Rating.post_delete))
        self.assertTrue(callable(Rating.m2m_changed))
