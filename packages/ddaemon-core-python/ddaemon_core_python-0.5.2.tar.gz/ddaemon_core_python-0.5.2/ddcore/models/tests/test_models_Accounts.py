"""(C) 2013-2025 Copycat Software, LLC. All Rights Reserved."""

import pytest

from django.test import TestCase
from django.test.client import RequestFactory

from ddcore.models import (
    GenderType,
    User,
    UserProfile,
    UserLogin)
from ddcore.models.tests import GenericUserTestCase


# class UserProfileTestCase(AbstractTestCase):
#     """UserProfile Model Test Class."""

#     model = TestUserProfile  # Way to test the abstract UserProfile Model.

#     def setUp(self):
#         super().setUp()

#         self.user = User.objects.create(
#             id="17615b57-cfa9-41e5-a8cb-7fa79e0d03fc",
#             first_name="John",
#             last_name="Doe",
#             username="admin",
#             email="admin@2remember.live",
#             password="pbkdf2_sha256$600000$yegBmCRvGllFovCDN3DGaz$EkWe1oz928/o1fw7qE9GD+tBkRlI0gifIXvkjEMGHsE=",
#             is_active=True,
#             is_staff=True,
#             is_superuser=True)
#         self.model.objects.create(
#             user=self.user,
#             # avatar=
#             # nickname=
#             # bio=
#             gender=GenderType.MALE)

#     def tearDown(self):
#         super().tearDown()

#     def test_success(self):
#         # ---------------------------------------------------------------------
#         # --- Initials.
#         # ---------------------------------------------------------------------
#         user_profile = self.model.objects.get(pk=1)

#         # ---------------------------------------------------------------------
#         # --- Assertions.
#         # ---------------------------------------------------------------------
#         self.assertEqual(user_profile.stat_gender_name, GenderType.MALE)
#         self.assertEqual(user_profile.full_name_straight, GenderType.MALE)
#         self.assertEqual(user_profile.full_name, GenderType.MALE)
#         self.assertEqual(user_profile.short_name, GenderType.MALE)
#         self.assertEqual(user_profile.auth_name, GenderType.MALE)
#         self.assertEqual(user_profile.name, self.user.get_full_name())

#         self.assertTrue(callable(user_profile.pre_save))
#         self.assertTrue(callable(user_profile.post_save))
#         self.assertTrue(callable(user_profile.pre_delete))
#         self.assertTrue(callable(user_profile.post_delete))
#         self.assertTrue(callable(user_profile.m2m_changed))


class UserLoginTestCase(GenericUserTestCase):
    """UserLogin Model Test Class."""

    model = UserLogin

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
        self.model.objects.insert(
            request=self._generate_post_request(),
            user=self.user,
            user_agent=self.user_agent,
            provider=self.provider)
        user_login = self.model.objects.latest("id")

        # ---------------------------------------------------------------------
        # --- Assertions.
        # ---------------------------------------------------------------------
        self.assertEqual(user_login.user.id, self.user.id)
        self.assertEqual(user_login.ip, self.ip)
        self.assertEqual(user_login.user_agent, self.user_agent)
        self.assertEqual(user_login.provider, self.provider)
        self.assertEqual(user_login.geo_data, self.geo_data)

        self.assertTrue(callable(user_login.pre_save))
        self.assertTrue(callable(user_login.post_save))
        self.assertTrue(callable(user_login.pre_delete))
        self.assertTrue(callable(user_login.post_delete))
        self.assertTrue(callable(user_login.m2m_changed))

    def test_insert_no_user(self):
        """Test Case: Insert: No User passed."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        self.model.objects.insert(
            request=self._generate_post_request(),
            # user=self.user,
            user_agent=self.user_agent,
            provider=self.provider)
        user_login = self.model.objects.latest("id")

        # ---------------------------------------------------------------------
        # --- Assertions.
        # ---------------------------------------------------------------------
        self.assertEqual(user_login.user.id, self.user.id)

    def test_insert_no_user_agent(self):
        """"Test Case: Insert: No User Agent passed."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        self.model.objects.insert(
            request=self._generate_post_request(headers={
                "User-Agent":   self.user_agent,
            }),
            user=self.user,
            # user_agent=self.user_agent,
            provider=self.provider)
        user_login = self.model.objects.latest("id")

        # ---------------------------------------------------------------------
        # --- Assertions.
        # ---------------------------------------------------------------------
        self.assertEqual(user_login.user_agent, self.user_agent)

        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        self.model.objects.insert(
            request=self._generate_post_request(),
            user=self.user,
            # user_agent=self.user_agent,
            provider=self.provider)
        user_login = self.model.objects.latest("id")

        # ---------------------------------------------------------------------
        # --- Assertions.
        # ---------------------------------------------------------------------
        self.assertIsNone(user_login.user_agent)

    def test_insert_no_provider(self):
        """"Test Case: Insert: No Provider passed."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        self.model.objects.insert(
            request=self._generate_post_request(),
            user=self.user,
            user_agent=self.user_agent,
            # provider=self.provider
            )
        user_login = self.model.objects.latest("id")

        # ---------------------------------------------------------------------
        # --- Assertions.
        # ---------------------------------------------------------------------
        self.assertIsNone(user_login.provider)
