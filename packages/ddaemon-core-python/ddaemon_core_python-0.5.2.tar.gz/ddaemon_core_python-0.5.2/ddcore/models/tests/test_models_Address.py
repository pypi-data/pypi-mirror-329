"""(C) 2013-2025 Copycat Software, LLC. All Rights Reserved."""

from django.test import TestCase

from ddcore.models import Address


class AddressTestCase(TestCase):
    """Address Model Test Class."""

    def setUp(self):
        """Constructor."""
        self.short_address = "New Valentina, Wisconsin, US"
        self.full_address = "57732 Dereck Shore Apt. 157, New Valentina, Wisconsin 85716, US"

    def test_success(self):
        """Test Case: Success."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        Address.objects.create(
            address_1="57732 Dereck Shore",
            address_2="Apt. 157",
            city="New Valentina",
            zip_code="85716",
            province="Wisconsin",
            country="USA",
            notes="Some Notes")
        address = Address.objects.latest("id")

        # ---------------------------------------------------------------------
        # --- Assertions.
        # ---------------------------------------------------------------------
        self.assertEqual(address.short_address, self.short_address)
        self.assertEqual(address.full_address, self.full_address)

        self.assertTrue(callable(address.pre_save))
        self.assertTrue(callable(address.post_save))
        self.assertTrue(callable(address.pre_delete))
        self.assertTrue(callable(address.post_delete))
        self.assertTrue(callable(address.m2m_changed))

    def test_short_address(self):
        """Test Case: Short Address."""
        # ---------------------------------------------------------------------
        # --- Only City and Country.
        # ---------------------------------------------------------------------
        Address.objects.create(
            # address_1="57732 Dereck Shore",
            # address_2="Apt. 157",
            city="New Valentina",
            # zip_code="85716",
            # province="Wisconsin",
            country="USA",
            # notes="Some Notes"
            )
        address = Address.objects.latest("id")

        self.assertEqual(address.short_address, "New Valentina, US")

        # ---------------------------------------------------------------------
        # --- Only Province and Country.
        # ---------------------------------------------------------------------
        Address.objects.create(
            # address_1="57732 Dereck Shore",
            # address_2="Apt. 157",
            # city="New Valentina",
            # zip_code="85716",
            province="Wisconsin",
            country="USA",
            # notes="Some Notes"
            )
        address = Address.objects.latest("id")

        self.assertEqual(address.short_address, "Wisconsin, US")

        # ---------------------------------------------------------------------
        # --- Only Country.
        # ---------------------------------------------------------------------
        Address.objects.create(
            # address_1="57732 Dereck Shore",
            # address_2="Apt. 157",
            # city="New Valentina",
            # zip_code="85716",
            # province="Wisconsin",
            country="USA",
            # notes="Some Notes"
            )
        address = Address.objects.latest("id")

        self.assertEqual(address.short_address, "US")

    def test_full_address(self):
        """Test Case: Full Address."""
        # ---------------------------------------------------------------------
        # --- Only Address 1 and Country.
        # ---------------------------------------------------------------------
        Address.objects.create(
            address_1="57732 Dereck Shore",
            # address_2="Apt. 157",
            # city="New Valentina",
            # zip_code="85716",
            # province="Wisconsin",
            country="USA",
            # notes="Some Notes"
            )
        address = Address.objects.latest("id")

        self.assertEqual(address.full_address, "57732 Dereck Shore, US")

        # ---------------------------------------------------------------------
        # --- Only Address 2 and Country.
        # ---------------------------------------------------------------------
        Address.objects.create(
            # address_1="57732 Dereck Shore",
            address_2="Apt. 157",
            # city="New Valentina",
            # zip_code="85716",
            # province="Wisconsin",
            country="USA",
            # notes="Some Notes"
            )
        address = Address.objects.latest("id")

        self.assertEqual(address.full_address, "Apt. 157, US")

        # ---------------------------------------------------------------------
        # --- Only Address 1, Address 2 and Country.
        # ---------------------------------------------------------------------
        Address.objects.create(
            address_1="57732 Dereck Shore",
            address_2="Apt. 157",
            # city="New Valentina",
            # zip_code="85716",
            # province="Wisconsin",
            country="USA",
            # notes="Some Notes"
            )
        address = Address.objects.latest("id")

        self.assertEqual(address.full_address, "57732 Dereck Shore Apt. 157, US")

        # ---------------------------------------------------------------------
        # --- Only City and Country.
        # ---------------------------------------------------------------------
        Address.objects.create(
            # address_1="57732 Dereck Shore",
            # address_2="Apt. 157",
            city="New Valentina",
            # zip_code="85716",
            # province="Wisconsin",
            country="USA",
            # notes="Some Notes"
            )
        address = Address.objects.latest("id")

        self.assertEqual(address.full_address, "New Valentina, US")

        # ---------------------------------------------------------------------
        # --- Only Zipcode and Country.
        # ---------------------------------------------------------------------
        Address.objects.create(
            # address_1="57732 Dereck Shore",
            # address_2="Apt. 157",
            # city="New Valentina",
            zip_code="85716",
            # province="Wisconsin",
            country="USA",
            # notes="Some Notes"
            )
        address = Address.objects.latest("id")

        self.assertEqual(address.full_address, "85716, US")

        # ---------------------------------------------------------------------
        # --- Only Province and Country.
        # ---------------------------------------------------------------------
        Address.objects.create(
            # address_1="57732 Dereck Shore",
            # address_2="Apt. 157",
            # city="New Valentina",
            # zip_code="85716",
            province="Wisconsin",
            country="USA",
            # notes="Some Notes"
            )
        address = Address.objects.latest("id")

        self.assertEqual(address.full_address, "Wisconsin, US")

        # ---------------------------------------------------------------------
        # --- Only Zipcode, Province and Country.
        # ---------------------------------------------------------------------
        Address.objects.create(
            # address_1="57732 Dereck Shore",
            # address_2="Apt. 157",
            # city="New Valentina",
            zip_code="85716",
            province="Wisconsin",
            country="USA",
            # notes="Some Notes"
            )
        address = Address.objects.latest("id")

        self.assertEqual(address.full_address, "Wisconsin 85716, US")

        # ---------------------------------------------------------------------
        # --- Only Country.
        # ---------------------------------------------------------------------
        Address.objects.create(
            # address_1="57732 Dereck Shore",
            # address_2="Apt. 157",
            # city="New Valentina",
            # zip_code="85716",
            # province="Wisconsin",
            country="USA",
            # notes="Some Notes"
            )
        address = Address.objects.latest("id")

        self.assertEqual(address.full_address, "US")
