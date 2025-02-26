"""(C) 2013-2025 Copycat Software, LLC. All Rights Reserved."""

from django.test import TestCase

from ddcore.models import SocialLink


class SocialLinkTestCase(TestCase):
    """SocialLink Model Test Class."""

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
        self.assertTrue(callable(SocialLink.pre_save))
        self.assertTrue(callable(SocialLink.post_save))
        self.assertTrue(callable(SocialLink.pre_delete))
        self.assertTrue(callable(SocialLink.post_delete))
        self.assertTrue(callable(SocialLink.m2m_changed))
