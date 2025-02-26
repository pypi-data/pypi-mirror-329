"""(C) 2013-2025 Copycat Software, LLC. All Rights Reserved."""

from django.test import TestCase

from ddcore.models import Complaint


class ComplaintTestCase(TestCase):
    """Complaint Model Test Class."""

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
        self.assertTrue(callable(Complaint.pre_save))
        self.assertTrue(callable(Complaint.post_save))
        self.assertTrue(callable(Complaint.pre_delete))
        self.assertTrue(callable(Complaint.post_delete))
        self.assertTrue(callable(Complaint.m2m_changed))
