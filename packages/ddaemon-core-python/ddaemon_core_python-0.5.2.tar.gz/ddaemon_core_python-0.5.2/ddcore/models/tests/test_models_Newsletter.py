"""(C) 2013-2025 Copycat Software, LLC. All Rights Reserved."""

from django.test import TestCase

from ddcore.models import Newsletter


class NewsletterTestCase(TestCase):
    """Newsletter Model Test Class."""

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
        self.assertTrue(callable(Newsletter.pre_save))
        self.assertTrue(callable(Newsletter.post_save))
        self.assertTrue(callable(Newsletter.pre_delete))
        self.assertTrue(callable(Newsletter.post_delete))
        self.assertTrue(callable(Newsletter.m2m_changed))
