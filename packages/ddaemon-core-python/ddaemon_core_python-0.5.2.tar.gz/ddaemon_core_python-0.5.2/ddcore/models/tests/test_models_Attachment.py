"""(C) 2013-2025 Copycat Software, LLC. All Rights Reserved."""

from django.test import TestCase

from ddcore.models import (
    AttachedImage,
    AttachedDocument,
    AttachedUrl,
    AttachedVideoUrl,
    AttachmentMixin,
    GenderType,
    TemporaryFile,
    User,
    UserProfile)
from ddcore.models.tests import TestUserProfile


class TemporaryFileTestCase(TestCase):
    """TemporaryFile Model Test Class."""

    def setUp(self):
        """Constructor."""
        self.name = "Attachment"

    def test_success(self):
        """Test Case: Success."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        TemporaryFile.objects.create(
            # file=
            name=self.name)
        attachment = TemporaryFile.objects.latest("id")

        # ---------------------------------------------------------------------
        # --- Assertions.
        # ---------------------------------------------------------------------
        self.assertEqual(attachment.name, self.name)

        self.assertTrue(callable(TemporaryFile.pre_save))
        self.assertTrue(callable(TemporaryFile.post_save))
        self.assertTrue(callable(TemporaryFile.pre_delete))
        self.assertTrue(callable(TemporaryFile.post_delete))
        self.assertTrue(callable(TemporaryFile.m2m_changed))


# class AttachedImageTestCase(AbstractTestCase):
class AttachedImageTestCase(TestCase):
    """AttachedImage Model Test Class."""

    model = TestUserProfile  # Way to test the abstract UserProfile Model.

    def setUp(self):
        """Constructor."""
        # super().setUp()

        self.name = "Attachment"

    def test_success(self):
        """Test Case: Success."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        AttachedImage.objects.create(
            # image=None,
            name=self.name
            # content_type=
            # object_id=
            )
        attachment_1 = AttachedImage.objects.latest("id")

        AttachedImage.objects.create(
            # image=None,
            name=self.name,
            is_hidden=True,
            is_private=True
            # content_type=
            # object_id=
            )
        attachment_2 = AttachedImage.objects.latest("id")

        # ---------------------------------------------------------------------
        # --- Assertions.
        # ---------------------------------------------------------------------
        self.assertEqual(attachment_1.name, self.name)
        self.assertFalse(attachment_1.is_hidden)
        self.assertFalse(attachment_1.is_private)

        self.assertEqual(attachment_2.name, self.name)
        self.assertTrue(attachment_2.is_hidden)
        self.assertTrue(attachment_2.is_private)

        self.assertTrue(callable(AttachedImage.pre_save))
        self.assertTrue(callable(AttachedImage.post_save))
        self.assertTrue(callable(AttachedImage.pre_delete))
        self.assertTrue(callable(AttachedImage.post_delete))
        self.assertTrue(callable(AttachedImage.m2m_changed))


class AttachedDocumentTestCase(TestCase):
    """AttachedDocument Model Test Class."""

    def setUp(self):
        """Constructor."""
        self.name = "Attachment"

    def test_success(self):
        """Test Case: Success."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        AttachedDocument.objects.create(
            # document=None,
            name=self.name
            # content_type=
            # object_id=
            )
        attachment_1 = AttachedDocument.objects.latest("id")

        AttachedDocument.objects.create(
            # document=None,
            name=self.name,
            is_hidden=True,
            is_private=True
            # content_type=
            # object_id=
            )
        attachment_2 = AttachedDocument.objects.latest("id")

        # ---------------------------------------------------------------------
        # --- Assertions.
        # ---------------------------------------------------------------------
        self.assertEqual(attachment_1.name, self.name)
        self.assertFalse(attachment_1.is_hidden)
        self.assertFalse(attachment_1.is_private)

        self.assertEqual(attachment_2.name, self.name)
        self.assertTrue(attachment_2.is_hidden)
        self.assertTrue(attachment_2.is_private)

        self.assertTrue(callable(AttachedDocument.pre_save))
        self.assertTrue(callable(AttachedDocument.post_save))
        self.assertTrue(callable(AttachedDocument.pre_delete))
        self.assertTrue(callable(AttachedDocument.post_delete))
        self.assertTrue(callable(AttachedDocument.m2m_changed))


class AttachedUrlTestCase(TestCase):
    """AttachedUrl Model Test Class."""

    def setUp(self):
        """Constructor."""
        self.title = "Attachment"

    def test_success(self):
        """Test Case: Success."""
        AttachedUrl.objects.create(
            # url=None,
            title=self.title
            # content_type=
            # object_id=
            )
        attachment_1 = AttachedUrl.objects.latest("id")

        AttachedUrl.objects.create(
            # url=None,
            title=self.title,
            is_hidden=True,
            is_private=True
            # content_type=
            # object_id=
            )
        attachment_2 = AttachedUrl.objects.latest("id")

        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Assertions.
        # ---------------------------------------------------------------------
        self.assertEqual(attachment_1.title, self.title)
        self.assertFalse(attachment_1.is_hidden)
        self.assertFalse(attachment_1.is_private)

        self.assertEqual(attachment_2.title, self.title)
        self.assertTrue(attachment_2.is_hidden)
        self.assertTrue(attachment_2.is_private)

        self.assertTrue(callable(AttachedUrl.pre_save))
        self.assertTrue(callable(AttachedUrl.post_save))
        self.assertTrue(callable(AttachedUrl.pre_delete))
        self.assertTrue(callable(AttachedUrl.post_delete))
        self.assertTrue(callable(AttachedUrl.m2m_changed))


class AttachedVideoUrlTestCase(TestCase):
    """AttachedVideoUrl Model Test Class."""

    def setUp(self):
        """Constructor."""

    def test_success(self):
        """Test Case: Success."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        AttachedVideoUrl.objects.create(
            # url=None,
            # content_type=
            # object_id=
            )
        attachment_1 = AttachedVideoUrl.objects.latest("id")

        AttachedVideoUrl.objects.create(
            # url=None,
            is_hidden=True,
            is_private=True
            # content_type=
            # object_id=
            )
        attachment_2 = AttachedVideoUrl.objects.latest("id")

        # ---------------------------------------------------------------------
        # --- Assertions.
        # ---------------------------------------------------------------------
        self.assertFalse(attachment_1.is_hidden)
        self.assertFalse(attachment_1.is_private)

        self.assertTrue(attachment_2.is_hidden)
        self.assertTrue(attachment_2.is_private)

        self.assertTrue(callable(AttachedVideoUrl.pre_save))
        self.assertTrue(callable(AttachedVideoUrl.post_save))
        self.assertTrue(callable(AttachedVideoUrl.pre_delete))
        self.assertTrue(callable(AttachedVideoUrl.post_delete))
        self.assertTrue(callable(AttachedVideoUrl.m2m_changed))
