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
# === COMMENT BASE MODEL
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- Comment Model Manager.
# -----------------------------------------------------------------------------
class CommentManager(models.Manager):
    """Comment Manager."""

    def get_queryset(self):
        """Docstring."""
        return super().get_queryset()


# -----------------------------------------------------------------------------
# --- Comment Model.
# -----------------------------------------------------------------------------
@autoconnect
class Comment(BaseModel):
    """Comment Model.

    Attributes
    ----------
    author                  : obj       User.
    text                    : str       Comment Text.

    is_deleted              : bool      Is deleted?

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
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        db_index=True,
        on_delete=models.CASCADE)
    text = models.TextField(
        verbose_name="Text",
        help_text=_("Comment Text"))

    # -------------------------------------------------------------------------
    # --- Flags.
    is_deleted = models.BooleanField(default=False)

    # -------------------------------------------------------------------------
    # --- Content Type.
    content_type = models.ForeignKey(
        ContentType,
        null=True, blank=True, default=None,
        on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(null=True, blank=True, default=None)
    content_object = fields.GenericForeignKey("content_type", "object_id")

    objects = CommentManager()

    class Meta:
        verbose_name = _("comment")
        verbose_name_plural = _("comments")
        ordering = ["created", ]

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
# --- Comment Model Mixin.
# -----------------------------------------------------------------------------
class CommentMixin:
    """Comment Mixin Class.

    Methods
    -------

    Properties
    ----------
    comment_list                        Returns a List of Comments.
    comments_count                      Returns a Count of Comments.

    """

    # -------------------------------------------------------------------------
    # --- Comments.
    @property
    def comment_list(self):
        """Returns a List of Comments."""
        return Comment.objects.filter(
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.id,
            is_deleted=False,
        ).order_by("-created")

    @property
    def comments_count(self):
        """Returns a Count of Comments."""
        return self.comment_list.count()
