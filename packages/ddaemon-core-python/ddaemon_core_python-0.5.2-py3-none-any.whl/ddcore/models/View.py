"""(C) 2013-2025 Copycat Software, LLC. All Rights Reserved."""

from django.conf import settings
from django.contrib.contenttypes import fields
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from .Base import BaseModel
from ..Decorators import autoconnect


# =============================================================================
# ===
# === VIEW MODEL
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- View Model Manager.
# -----------------------------------------------------------------------------
class ViewManager(models.Manager):
    """Views Manager."""

    def get_queryset(self):
        """Docstring."""
        return super().get_queryset()


# -----------------------------------------------------------------------------
# --- View Model.
# -----------------------------------------------------------------------------
@autoconnect
class View(BaseModel):
    """View Model.

    Attributes
    ----------
    viewer                  : obj       User.

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
    pre_save()                          `pre_save`    Object Signal.
    post_save()                         `post_save`   Object Signal.
    pre_delete()                        `pre_delete`  Object Signal.
    post_delete()                       `posr_delete` Object Signal.
    m2m_changed()                       `m2m_changed` Object Signal.

    """

    # -------------------------------------------------------------------------
    # --- Basics.
    viewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        db_index=True,
        null=True, blank=True,
        on_delete=models.CASCADE)

    # -------------------------------------------------------------------------
    # --- Content Type.
    content_type = models.ForeignKey(
        ContentType,
        null=True, blank=True, default=None,
        on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(null=True, blank=True, default=None)
    content_object = fields.GenericForeignKey("content_type", "object_id")

    objects = ViewManager()

    class Meta:
        verbose_name = _("view")
        verbose_name_plural = _("views")
        ordering = ["-id", ]

    def __repr__(self):
        """Docstring."""
        return f"<{self.__class__.__name__} ({self.id}: '{self.content_object}')>"

    def __str__(self):
        """Docstring."""
        return self.__repr__()

    def pre_save(self, **kwargs):
        """Docstring."""

    def post_save(self, created, **kwargs):
        """Docstring."""

    def pre_delete(self, **kwargs):
        """Docstring."""

    def post_delete(self, **kwargs):
        """Docstring."""


# -----------------------------------------------------------------------------
# --- View Model Mixin.
# -----------------------------------------------------------------------------
class ViewMixin:
    """View Mixin Class.

    Attributes
    ----------

    Methods
    -------
    increase_views_count()              Increases Views Count.

    Properties
    ----------
    get_views_count                     Returns Views Count.

    """

    # -------------------------------------------------------------------------
    # --- Views
    def increase_views_count(self, request):
        """Increases Views Count."""
        if request.user.is_authenticated:
            viewing, created = View.objects.get_or_create(
                viewer=request.user,
                content_type=ContentType.objects.get_for_model(self),
                object_id=self.id)

            return created

        return False

    @property
    def views_count(self):
        """Returns Views Count."""
        return View.objects.filter(
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.id,
        ).order_by("-created").count()
