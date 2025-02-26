"""(C) 2013-2025 Copycat Software, LLC. All Rights Reserved."""

from django.test import TestCase

from ddcore.models import (
    Phone,
    PhoneType)


class PhoneTestCase(TestCase):
    """Phone Model Test Class."""

    def setUp(self):
        """Constructor."""
        Phone.objects.create(
            phone_number="",
            phone_number_ext="",
            phone_type=PhoneType.NONE)
        Phone.objects.create(
            phone_number="+1-202-555-0114",
            phone_number_ext="",
            phone_type=PhoneType.HOME)
        Phone.objects.create(
            phone_number="+1-202-555-0114",
            phone_number_ext="",
            phone_type=PhoneType.WORK)
        Phone.objects.create(
            phone_number="+1-202-555-0114",
            phone_number_ext="",
            phone_type=PhoneType.MOBILE)
        Phone.objects.create(
            phone_number="+1-202-555-0114",
            phone_number_ext="",
            phone_type=PhoneType.FAX)

    def test_success(self):
        """Test Case: Success."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        phone_1 = Phone.objects.get(pk=1)
        phone_2 = Phone.objects.get(pk=2)
        phone_3 = Phone.objects.get(pk=3)
        phone_4 = Phone.objects.get(pk=4)
        phone_5 = Phone.objects.get(pk=5)

        # ---------------------------------------------------------------------
        # --- Assertions.
        # ---------------------------------------------------------------------
        self.assertEqual(phone_1.phone_type, PhoneType.NONE)
        self.assertEqual(str(phone_1), "")
        self.assertEqual(phone_2.phone_type, PhoneType.HOME)
        self.assertEqual(phone_3.phone_type, PhoneType.WORK)
        self.assertEqual(phone_4.phone_type, PhoneType.MOBILE)
        self.assertEqual(phone_5.phone_type, PhoneType.FAX)

        self.assertTrue(callable(Phone.pre_save))
        self.assertTrue(callable(Phone.post_save))
        self.assertTrue(callable(Phone.pre_delete))
        self.assertTrue(callable(Phone.post_delete))
        self.assertTrue(callable(Phone.m2m_changed))
