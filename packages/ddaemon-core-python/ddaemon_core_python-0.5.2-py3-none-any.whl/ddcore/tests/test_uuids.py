"""(C) 2013-2025 Copycat Software, LLC. All Rights Reserved."""

import re
import unittest

from django.test import TestCase
from django.test.client import RequestFactory

from ddcore import uuids


class UUIDsTestCase(TestCase):
    def setUp(self):
        """Constructor."""
        self.uuid4_re = "^([0-9A-Fa-f]{8}(-[0-9A-Fa-f]{4}){3}-[0-9A-Fa-f]{12})$"
        self.pattern = re.compile(self.uuid4_re)

    def _generate_request(self, headers=None):
        rf = RequestFactory(headers=headers) if headers else RequestFactory()
        request = rf.post("/singin/")

        return request

    # @unittest.skip("Skip the Test")
    def test_get_unique_hashname(self):
        """Docstring."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        hashname = uuids.get_unique_hashname()

        # ---------------------------------------------------------------------
        # --- Assertions.
        # ---------------------------------------------------------------------
        self.assertTrue(self.pattern.match(hashname))

    # @unittest.skip("Skip the Test")
    def test_get_unique_filename(self):
        """Docstring."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        file_name = "sample"
        file_ext = "exe"

        filename = uuids.get_unique_filename(f"{file_name}.{file_ext}")

        # ---------------------------------------------------------------------
        # --- Assertions.
        # ---------------------------------------------------------------------
        self.assertTrue(self.pattern.match(filename.split(".")[0]))
        self.assertEquals(filename.split(".")[1], file_ext)

    # @unittest.skip("Skip the Test")
    def test_get_request_id(self):
        """Docstring."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        request = self._generate_request()

        # ---------------------------------------------------------------------
        # --- Assertions.
        # ---------------------------------------------------------------------
        request_id = uuids.get_request_id(request)
        self.assertTrue(self.pattern.match(request_id))

        setattr(request, "request_id", request_id)

        request_id = uuids.get_request_id(request)
        self.assertTrue(self.pattern.match(request_id))
