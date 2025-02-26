"""(C) 2013-2025 Copycat Software, LLC. All Rights Reserved."""

from django.contrib.contenttypes import fields
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from .Base import BaseModel
from .. import enum
from ..Decorators import autoconnect


# =============================================================================
# ===
# === SOCIAL LINK MODEL
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- SOCIAL LINKS CHOICES
# -----------------------------------------------------------------------------
SocialApp = enum(
    NONE="--------",
    FACEBOOK="0",
    TWITTER="1",
    LINKEDIN="2",
    GOOGLE="4",
    PINTEREST="8",
    INSTAGRAM="16",
    TUMBLR="32",
    YOUTUBE="64")
social_app_choices = [
    (SocialApp.NONE,       _("--------")),
    (SocialApp.FACEBOOK,   _("Facebook")),
    (SocialApp.TWITTER,    _("Twitter")),
    (SocialApp.LINKEDIN,   _("Linked In")),
    (SocialApp.GOOGLE,     _("Google +")),
    (SocialApp.PINTEREST,  _("Pinterest")),
    (SocialApp.INSTAGRAM,  _("Instagram")),
    (SocialApp.TUMBLR,     _("Tumblr")),
    (SocialApp.YOUTUBE,    _("YouTube")),
]

SocialAppIcons = enum(
    NONE="--------",
    FACEBOOK="0",
    TWITTER="1",
    LINKEDIN="2",
    GOOGLE="4",
    PINTEREST="8",
    INSTAGRAM="16",
    TUMBLR="32",
    YOUTUBE="64")
social_app_icons = [
    (SocialAppIcons.NONE,         ""),
    (SocialAppIcons.FACEBOOK,     "bi bi-facebook"),
    (SocialAppIcons.TWITTER,      "bi bi-twitter"),
    (SocialAppIcons.LINKEDIN,     "bi bi-linkedin"),
    (SocialAppIcons.GOOGLE,       "bi bi-google-plus"),
    (SocialAppIcons.PINTEREST,    "bi bi-pinterest"),
    (SocialAppIcons.INSTAGRAM,    "bi bi-instagram"),
    (SocialAppIcons.TUMBLR,       "bi bi-tumblr"),
    (SocialAppIcons.YOUTUBE,      "bi bi-youtube"),
]

SocialAppButtons = enum(
    NONE="--------",
    FACEBOOK="0",
    TWITTER="1",
    LINKEDIN="2",
    GOOGLE="4",
    PINTEREST="8",
    INSTAGRAM="16",
    TUMBLR="32",
    YOUTUBE="64")
social_app_buttons = [
    (SocialAppButtons.NONE,         ""),
    (SocialAppButtons.FACEBOOK,     "btn btn-facebook"),
    (SocialAppButtons.TWITTER,      "btn btn-twitter"),
    (SocialAppButtons.LINKEDIN,     "btn btn-linkedin"),
    (SocialAppButtons.GOOGLE,       "btn btn-google-plus"),
    (SocialAppButtons.PINTEREST,    "btn btn-pinterest"),
    (SocialAppButtons.INSTAGRAM,    "btn btn-instagram"),
    (SocialAppButtons.TUMBLR,       "btn btn-tumblr"),
    (SocialAppButtons.YOUTUBE,      "btn btn-youtube"),
]


# -----------------------------------------------------------------------------
# --- Social Link Model Manager.
# -----------------------------------------------------------------------------
class SocialLinkManager(models.Manager):
    """Social Link Manager."""

    def get_queryset(self):
        """Docstring."""
        return super().get_queryset()


# -----------------------------------------------------------------------------
# --- Social Link Model.
# -----------------------------------------------------------------------------
@autoconnect
class SocialLink(BaseModel):
    """Social Link Model.

    Attributes
    ----------
    social_app              : str       Social App Name.
    url                     : str       Social App URL.

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
    stat_social_app_icon()              Return Social App Representation as Icon.
    stat_social_app_button()            Return Social App Representation as Button.

    pre_save()                          `pre_save`    Object Signal.
    post_save()                         `post_save`   Object Signal.
    pre_delete()                        `pre_delete`  Object Signal.
    post_delete()                       `posr_delete` Object Signal.
    m2m_changed()                       `m2m_changed` Object Signal.

    """

    # -------------------------------------------------------------------------
    # --- Basics.
    social_app = models.CharField(
        max_length=16,
        choices=social_app_choices,
        default=SocialApp.NONE,
        verbose_name=_("Social App"),
        help_text=_("Social App"))
    url = models.URLField(
        db_index=True,
        null=True, blank=True,
        verbose_name=_("url"),
        help_text=_("Social Link"))

    # -------------------------------------------------------------------------
    # --- Content Type.
    content_type = models.ForeignKey(
        ContentType,
        related_name="content_type_social_links",
        null=True, blank=True, default=None,
        on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(null=True, blank=True, default=None)
    content_object = fields.GenericForeignKey("content_type", "object_id")

    # -------------------------------------------------------------------------
    # --- Status.

    # -------------------------------------------------------------------------
    # --- Significant Texts.

    # -------------------------------------------------------------------------
    # --- Significant Dates.

    objects = SocialLinkManager()

    class Meta:
        verbose_name = _("social link")
        verbose_name_plural = _("social links")
        ordering = ["created", ]

    def __repr__(self):
        """Docstring."""
        return f"<{self.__class__.__name__} ({self.id}: '{self.social_app}')>"

    def __str__(self):
        """Docstring."""
        return self.__repr__()

    # -------------------------------------------------------------------------
    # --- Properties.
    @property
    def stat_social_app_icon(self):
        """Docstring."""
        for code, icon in social_app_icons:
            if self.social_app == code:
                return icon

        return ""

    @property
    def stat_social_app_button(self):
        """Docstring."""
        for code, button in social_app_buttons:
            if self.social_app == code:
                return button

        return ""

    # -------------------------------------------------------------------------
    # --- Signals.
    def pre_save(self, **kwargs):
        """Docstring."""

    def post_save(self, created, **kwargs):
        """Docstring."""

    def pre_delete(self, **kwargs):
        """Docstring."""

    def post_delete(self, **kwargs):
        """Docstring."""
