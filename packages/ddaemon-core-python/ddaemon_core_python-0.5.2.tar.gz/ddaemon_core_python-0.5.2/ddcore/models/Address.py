"""(C) 2013-2025 Copycat Software, LLC. All Rights Reserved."""

from django.contrib.contenttypes import fields
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from django_countries.fields import CountryField

from .Base import BaseModel
from ..Decorators import autoconnect
from ..Utilities import get_purified_str


# =============================================================================
# ===
# === ADDRESS MODEL
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- Address Model Choices.
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# --- Address Model Manager.
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# --- Address Model.
# -----------------------------------------------------------------------------
@autoconnect
class Address(BaseModel):
    """Address Model.

    Attributes
    ----------
    address_1               : str       Address Line #1 Field.
    address_2               : str       Address Line #2 Field.
    city                    : str       City Field.
    zip_code                : str       Zip/Postal Code Field.
    province                : str       State/Province Field.
    country                 : str       Country Field.
    notes                   : str       Notes Field.

    content_type            : obj       Content Type.
    object_id               : int       Object  ID.
    content_object          ; obj       Content Object.

    custom_data             : dict      Custom Data JSON Field.

    is_hidden               : bool      Is Object hidden?
    is_private              : bool      Is Object private?
    is_deleted              : bool      Is Object deleted?

    created_by              : obj       User, created  the Object.
    modified_by             : obj       User, modified the Object.
    deleted_by              : obj       User, deleted the Object.

    created                 : datetime  Timestamp the Object has been created.
    modified                : datetime  Timestamp the Object has been modified.
    deleted                 : datetime  Timestamp the Object has been deleted.

    Methods
    -------
    short_address()
    full_address()

    pre_save()                          `pre_save`    Object Signal.
    post_save()                         `post_save`   Object Signal.
    pre_delete()                        `pre_delete`  Object Signal.
    post_delete()                       `posr_delete` Object Signal.
    m2m_changed()                       `m2m_changed` Object Signal.

    """

    # -------------------------------------------------------------------------
    # --- Basics.
    address_1 = models.CharField(
        db_index=True,
        max_length=80, null=True, blank=True,
        verbose_name=_("Address Line #1"),
        help_text=_("Address Line #1"))
    address_2 = models.CharField(
        db_index=True,
        max_length=80, null=True, blank=True,
        verbose_name=_("Address Line #2"),
        help_text=_("Address Line #2"))
    city = models.CharField(
        db_index=True,
        max_length=80, null=True, blank=True,
        verbose_name=_("City"),
        help_text=_("City"))
    zip_code = models.CharField(
        db_index=True,
        max_length=80, null=True, blank=True,
        verbose_name=_("Zip/Postal Code"),
        help_text=_("Zip/Postal Code"))
    province = models.CharField(
        db_index=True,
        max_length=80, null=True, blank=True,
        verbose_name=_("State/Province"),
        help_text=_("State/Province"))
    country = CountryField(
        db_index=True,
        verbose_name=_("Country"),
        help_text=_("Country"))

    # -------------------------------------------------------------------------
    # --- Notes.
    notes = models.TextField(
        null=True, blank=True,
        verbose_name=_("Notes"),
        help_text=_(
            "Here you can provide additional Notes, Directions, and any other Advice, "
            "regarding the Location."))

    # -------------------------------------------------------------------------
    # --- Content Type.
    content_type = models.ForeignKey(
        ContentType,
        null=True, blank=True, default=None,
        on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(null=True, blank=True, default=None)
    content_object = fields.GenericForeignKey("content_type", "object_id")

    class Meta:
        verbose_name = _("address")
        verbose_name_plural = _("addresses")
        ordering = ["-id", ]

    def __repr__(self):
        """Docstring."""
        return f"<{self.__class__.__name__} ({self.id}: '{self.short_address}')>"

    def __str__(self):
        """Docstring."""
        return self.__repr__()

    # -------------------------------------------------------------------------
    # --- Properties.
    # -------------------------------------------------------------------------
    @property
    def short_address(self):
        """Docstring."""
        address = ""

        if self.city:
            address += f"{self.city}"

            if (
                    self.province or
                    self.country):
                address += ", "

        if self.province:
            address += f"{self.province}"

            if self.country:
                address += ", "

        if self.country:
            address += f"{self.country}"

        return address

    @property
    def full_address(self):
        """Docstring."""
        address = ""

        if (
                self.address_1 and
                self.address_2):
            address += f"{self.address_1} {self.address_2}, "
        elif self.address_1:
            address += f"{self.address_1}, "
        elif self.address_2:
            address += f"{self.address_2}, "

        if self.city:
            address += f"{self.city}, "

        if (
                self.province and
                self.zip_code):
            address += f"{self.province} {self.zip_code}, "
        elif self.province:
            address += f"{self.province}, "
        elif self.zip_code:
            address += f"{self.zip_code}, "

        if self.country:
            address += f"{self.country}"

        return address

    # -------------------------------------------------------------------------
    # --- Methods.
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # --- Static Methods.
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # --- Class Methods.
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # --- Signals.
    # -------------------------------------------------------------------------
    def pre_save(self, **kwargs):
        """Docstring."""
        # ---------------------------------------------------------------------
        # --- Remove special Characters, duplicated and trailing Spaces.
        self.address_1 = get_purified_str(self.address_1)
        self.address_2 = get_purified_str(self.address_2)
        self.city = get_purified_str(self.city)
        self.province = get_purified_str(self.province)

    def post_save(self, created, **kwargs):
        """Docstring."""

    def pre_delete(self, **kwargs):
        """Docstring."""

    def post_delete(self, **kwargs):
        """Docstring."""
