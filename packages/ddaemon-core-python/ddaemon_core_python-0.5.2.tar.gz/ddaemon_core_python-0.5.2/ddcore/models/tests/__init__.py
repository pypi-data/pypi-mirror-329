"""(C) 2013-2025 Copycat Software, LLC. All Rights Reserved."""

from django.db import connection
from django.test import TestCase
from django.test.client import RequestFactory

from ddcore.models import (
    AttachmentMixin,
    User,
    UserProfile)


class GenericUserTestCase(TestCase):
    """Generic User Model Test Class."""

    def setUp(self):
        """Constructor."""
        super().setUp()

        self.admin = User.objects.create(
            id=1,
            uid="17615b57-cfa9-41e5-a8cb-7fa79e0d03fc",
            first_name="John",
            last_name="Doe",
            username="admin",
            email="admin@2remember.live",
            password="pbkdf2_sha256$600000$yegBmCRvGllFovCDN3DGaz$EkWe1oz928/o1fw7qE9GD+tBkRlI0gifIXvkjEMGHsE=",
            is_active=True,
            is_staff=True,
            is_superuser=True)
        self.user = User.objects.create(
            id=2,
            uid="0e2a03c3-12e4-4cd3-a118-0dbf79baa444",
            first_name="John",
            last_name="Smith",
            username="user",
            email="user@2remember.live",
            password="pbkdf2_sha256$600000$yegBmCRvGllFovCDN3DGaz$EkWe1oz928/o1fw7qE9GD+tBkRlI0gifIXvkjEMGHsE=",
            is_active=True,
            is_staff=False,
            is_superuser=False)

        # self.profile = UserProfile.objects.create(user=self.user)

        self.ip = "127.0.0.1"
        self.user_agent = (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/126.0.0.0 Safari/537.36")
        self.provider = "Cox"
        self.geo_data = {
            "country_code":     "XX",
            "country_name":     "unknown",
            "remote_addr":      "127.0.0.1",
        }

    def tearDown(self):
        """Destructor."""
        super().tearDown()

    def _generate_post_request(self, headers=None):
        """Generate POST Request."""
        rf = RequestFactory(headers=headers) if headers else RequestFactory()
        request = rf.post("/singin/")
        setattr(request, "user", self.user)
        setattr(request, "geo_data", self.geo_data)

        return request


class TestUserProfile(UserProfile, AttachmentMixin):
    """UserProfile Test Model."""
    __test__ = False

    class Meta:
        app_label = "test_user_profile_model"
        db_table = "test_user_profile_model"


class AbstractTestCase(TestCase):
    """Abstract Model Base Test Class."""

    model = None  # Define in the Child Class.

    def setUp(self):
        """Constructor."""
        with connection.constraint_checks_disabled():
            with connection.schema_editor() as schema_editor:
                connection.disable_constraint_checking()
                schema_editor.connection.in_atomic_block = False
                schema_editor.create_model(self.model)

    def tearDown(self):
        """Destructor."""
        with connection.constraint_checks_disabled(), connection.schema_editor() as schema_editor:
            schema_editor.connection.in_atomic_block = False
            schema_editor.delete_model(self.model)
            schema_editor.connection.in_atomic_block = True
