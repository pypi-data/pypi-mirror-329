"""(C) 2013-2025 Copycat Software, LLC. All Rights Reserved."""

from ddcore.models import View
from ddcore.models.tests import GenericUserTestCase


class ViewTestCase(GenericUserTestCase):
    """View Model Test Class."""

    def setUp(self):
        """Constructor."""
        super().setUp()

    def tearDown(self):
        """Destructor."""
        super().tearDown()

    def test_success(self):
        """Test Case: Success."""

        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        # self.user.profile.increase_views_count(request=self._generate_request())

        # ---------------------------------------------------------------------
        # --- Assertions.
        # ---------------------------------------------------------------------
        self.assertTrue(callable(View.pre_save))
        self.assertTrue(callable(View.post_save))
        self.assertTrue(callable(View.pre_delete))
        self.assertTrue(callable(View.post_delete))
        self.assertTrue(callable(View.m2m_changed))
