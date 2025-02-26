"""(C) 2013-2025 Copycat Software, LLC. All Rights Reserved."""

from django.test import TestCase

from ddcore.models import Comment


class CommentTestCase(TestCase):
    """Comment Model Test Class."""

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
        self.assertTrue(callable(Comment.pre_save))
        self.assertTrue(callable(Comment.post_save))
        self.assertTrue(callable(Comment.pre_delete))
        self.assertTrue(callable(Comment.post_delete))
        self.assertTrue(callable(Comment.m2m_changed))
