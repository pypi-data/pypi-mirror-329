"""(C) 2013-2025 Copycat Software, LLC. All Rights Reserved."""

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.db import models

from django_extensions.db.fields import ModificationDateTimeField
from django_extensions.db.models import (
    TimeStampedModel,
    TitleDescriptionModel,
    TitleSlugDescriptionModel)

from ddcore.Decorators import autoconnect
from ddcore.Serializers import JSONEncoder


# =============================================================================
# ===
# === BASE MODEL
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- Base Model Manager.
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# --- Base Model.
# -----------------------------------------------------------------------------
@autoconnect
class BaseModel(TimeStampedModel):
    """Base Model Class.

    Provides the Base Model Class.

    Attributes
    ----------
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
    pre_save()                          `pre_save`    Object Signal.
    post_save()                         `post_save`   Object Signal.
    pre_delete()                        `pre_delete`  Object Signal.
    post_delete()                       `posr_delete` Object Signal.
    m2m_changed()                       `m2m_changed` Object Signal.

    """
    custom_data = models.JSONField(
        null=True, blank=True,
        encoder=JSONEncoder,
        verbose_name=_("Custom Data"))

    # -------------------------------------------------------------------------
    # --- Flags.
    is_hidden = models.BooleanField(
        default=False,
        verbose_name=_("Is hidden?"),
        help_text=_("Is Object hidden?"))
    is_private = models.BooleanField(
        default=False,
        verbose_name=_("Is private?"),
        help_text=_("Is Object private?"))
    is_deleted = models.BooleanField(
        default=False,
        verbose_name=_("Is deleted?"),
        help_text=_("Is Object deleted?"))

    # -------------------------------------------------------------------------
    # --- Custom.
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        db_index=True,
        on_delete=models.CASCADE,
        related_name="user_created_%(class)s",
        verbose_name=_("Created by"),
        help_text=_("User, created the Object."))
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        db_index=True,
        on_delete=models.CASCADE,
        related_name="user_modified_%(class)s",
        verbose_name=_("Modified by"),
        help_text=_("User, modified the Object."))
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        db_index=True,
        on_delete=models.CASCADE,
        related_name="user_deleted_%(class)s",
        verbose_name=_("Deleted by"),
        help_text=_("User, deleted the Object."))

    # -------------------------------------------------------------------------
    # --- Significant Dates.
    deleted = ModificationDateTimeField(_("deleted"), auto_now=False, blank=True, null=True)

    class Meta:
        """Meta Class."""

        verbose_name = _("base model")
        verbose_name_plural = _("base models")
        ordering = [
            "created",
        ]

        abstract = True

    def __repr__(self):
        """Docstring."""
        return f"<{self.__class__.__name__}>"

    def __str__(self):
        """Docstring."""
        return self.__repr__()

    # -------------------------------------------------------------------------
    # --- Properties.
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # --- Methods.
    # -------------------------------------------------------------------------
    def save(self, *args, **kwargs):
        """Save the Object."""
        request = kwargs.pop("request", None)
        if request:
            self.modified_by = request.user

            if not self.created_by:
                self.created_by = request.user

        super().save(*args, **kwargs)

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
        """Pre-save Object Signal."""

    def post_save(self, created, **kwargs):
        """Post-save Object Signal."""

    def pre_delete(self, **kwargs):
        """Pre-delete Object Signal."""

    def post_delete(self, **kwargs):
        """Post-delete Object Signal."""

    def m2m_changed(self, **kwargs):
        """M2M changed Signal."""


# =============================================================================
# ===
# === TITLE/DESCRIPTION BASE MODEL
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- Title/Description Model Manager.
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# --- Title/Description Model.
# -----------------------------------------------------------------------------
class TitleDescriptionBaseModel(BaseModel, TitleDescriptionModel):
    """Title/Description Base Model.

    Provides the Title/Description Base Model Class.

    Attributes
    ----------
    title                   : str       Title Field.
    description             : str       Description Field.

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
    pre_save()                          `pre_save`    Object Signal.
    post_save()                         `post_save`   Object Signal.
    pre_delete()                        `pre_delete`  Object Signal.
    post_delete()                       `posr_delete` Object Signal.
    m2m_changed()                       `m2m_changed` Object Signal.

    """

    class Meta:
        """Meta Class."""

        verbose_name = _("title/description base model")
        verbose_name_plural = _("title/description base models")
        ordering = [
            "created",
        ]

        abstract = True


# =============================================================================
# ===
# === TITLE/SLUG/DESCRIPTION BASE MODEL
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- Title/Slug/Description Model Manager.
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# --- Title/Slug/Description Model.
# -----------------------------------------------------------------------------
class TitleSlugDescriptionBaseModel(BaseModel, TitleSlugDescriptionModel):
    """Title/Slug/Description Base Model.

    Provides the Title/Slug/Description Base Model Class.

    Attributes
    ----------
    title                   : str       Title Field.
    slug                    : str       Slug Field, populated from Title Field.
    description             : str       Description Field.

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
    pre_save()                          `pre_save`    Object Signal.
    post_save()                         `post_save`   Object Signal.
    pre_delete()                        `pre_delete`  Object Signal.
    post_delete()                       `posr_delete` Object Signal.
    m2m_changed()                       `m2m_changed` Object Signal.

    """

    class Meta:
        """Meta Class."""

        verbose_name = _("title/slug/description base model")
        verbose_name_plural = _("title/slug/description base models")
        ordering = [
            "created",
        ]

        abstract = True
