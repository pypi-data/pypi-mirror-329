"""(C) 2013-2025 Copycat Software, LLC. All Rights Reserved."""

from django.test import TestCase

from ddcore.models import (
    BaseModel,
    TitleDescriptionBaseModel,
    TitleSlugDescriptionBaseModel)


class BaseTestCase(TestCase):
    """BaseModel Model Test Class."""

    def setUp(self):
        """Constructor."""

    def test_success(self):
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Assertions.
        # ---------------------------------------------------------------------
        self.assertIn("BaseModel", str(BaseModel))

        self.assertTrue(callable(BaseModel.pre_save))
        self.assertTrue(callable(BaseModel.post_save))
        self.assertTrue(callable(BaseModel.pre_delete))
        self.assertTrue(callable(BaseModel.post_delete))
        self.assertTrue(callable(BaseModel.m2m_changed))


class TitleDescriptionBaseTestCase(TestCase):
    """TitleDescriptionBaseModel Model Test Class."""

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
        self.assertIn("TitleDescriptionBaseModel", str(TitleDescriptionBaseModel))

        self.assertTrue(callable(TitleDescriptionBaseModel.pre_save))
        self.assertTrue(callable(TitleDescriptionBaseModel.post_save))
        self.assertTrue(callable(TitleDescriptionBaseModel.pre_delete))
        self.assertTrue(callable(TitleDescriptionBaseModel.post_delete))
        self.assertTrue(callable(TitleDescriptionBaseModel.m2m_changed))


class TitleSlugDescriptionBaseTestCase(TestCase):
    """TitleDescriptionBaseModel Model Test Class."""

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
        self.assertIn("TitleSlugDescriptionBaseModel", str(TitleSlugDescriptionBaseModel))

        self.assertTrue(callable(TitleDescriptionBaseModel.pre_save))
        self.assertTrue(callable(TitleDescriptionBaseModel.post_save))
        self.assertTrue(callable(TitleDescriptionBaseModel.pre_delete))
        self.assertTrue(callable(TitleDescriptionBaseModel.post_delete))
        self.assertTrue(callable(TitleDescriptionBaseModel.m2m_changed))
