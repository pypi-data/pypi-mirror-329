"""(C) 2013-2025 Copycat Software, LLC. All Rights Reserved."""

from django.contrib.contenttypes import fields
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from .Base import BaseModel
from .. import enum
from ..Decorators import autoconnect


# =============================================================================
# ===
# === PHONE MODEL
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- Phone Model Choices.
# -----------------------------------------------------------------------------
PhoneType = enum(
    NONE="--------",
    HOME="0",
    WORK="1",
    MOBILE="2",
    GOOGLE="4",
    FAX="8")
phone_type_choices = [
    (PhoneType.NONE,    _("--------")),
    (PhoneType.HOME,    _("Home")),
    (PhoneType.WORK,    _("Work")),
    (PhoneType.MOBILE,  _("Mobile")),
    (PhoneType.GOOGLE,  _("Google Voice")),
    (PhoneType.FAX,     _("Fax")),
]

PhoneTypeIcons = enum(
    NONE="--------",
    HOME="0",
    WORK="1",
    MOBILE="2",
    GOOGLE="4",
    FAX="8")
phone_type_icons = [
    (PhoneTypeIcons.NONE,   ""),
    (PhoneTypeIcons.HOME,   "bi bi-telephone"),
    (PhoneTypeIcons.WORK,   "bi bi-building"),
    (PhoneTypeIcons.MOBILE, "bi bi-phone"),
    (PhoneTypeIcons.GOOGLE, "bi bi-google"),
    (PhoneTypeIcons.FAX,    "bi bi-printer"),
]

# -----------------------------------------------------------------------------
# --- Phone Model Manager.
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# --- Phone Model.
# -----------------------------------------------------------------------------
@autoconnect
class Phone(BaseModel):
    """Phone Model.

    Attributes
    ----------
    phone_number            : str       Phone Number.
    phone_number_ext        : str       Phone Number Extension.
    phone_type              : str       Phone Type.

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
    stat_phone_type_icon()              Return Phone Type's Representation as Icon.

    pre_save()                          `pre_save`    Object Signal.
    post_save()                         `post_save`   Object Signal.
    pre_delete()                        `pre_delete`  Object Signal.
    post_delete()                       `posr_delete` Object Signal.
    m2m_changed()                       `m2m_changed` Object Signal.

    """

    # -------------------------------------------------------------------------
    # --- Basics.
    phone_number = PhoneNumberField(
        db_index=True,
        null=True, blank=True,
        verbose_name=_("Phone Number"),
        help_text=_("Please, use the International Format, e.g. +1-202-555-0114."))
    phone_number_ext = models.CharField(
        max_length=8, null=True, blank=True,
        verbose_name=_("Ext."),
        help_text=_("Ext."))
    phone_type = models.CharField(
        max_length=16, null=True, blank=True,
        choices=phone_type_choices,
        default=PhoneType.NONE,
        verbose_name=_("Phone Type"),
        help_text=_("Phone Type"))

    # -------------------------------------------------------------------------
    # --- Content Type.
    content_type = models.ForeignKey(
        ContentType,
        null=True, blank=True, default=None,
        on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(null=True, blank=True, default=None)
    content_object = fields.GenericForeignKey("content_type", "object_id")

    class Meta:
        """Meta."""
        verbose_name = _("phone number")
        verbose_name_plural = _("phone numbers")
        ordering = ["-id", ]

    def __repr__(self):
        """Docstring."""
        return f"<{self.__class__.__name__} ({self.id}: '{self.phone_number}', '{self.phone_type}')>"

    def __str__(self):
        """Docstring."""
        if self.phone_number:
            return f"{self.phone_number}"

        return ""

    # -------------------------------------------------------------------------
    # --- Properties.
    @property
    def stat_phone_type_icon(self):
        """Return Phone Type's Representation as Icon."""
        for code, icon in phone_type_icons:
            if self.phone_type == code:
                return icon

        return ""

    def pre_save(self, **kwargs):
        """Docstring."""

    def post_save(self, created, **kwargs):
        """Docstring."""

    def pre_delete(self, **kwargs):
        """Docstring."""

    def post_delete(self, **kwargs):
        """Docstring."""
