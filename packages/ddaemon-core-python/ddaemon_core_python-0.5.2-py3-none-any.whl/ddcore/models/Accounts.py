"""(C) 2013-2025 Copycat Software, LLC. All Rights Reserved."""

import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from django_extensions.db.fields.json import JSONField
from django_extensions.db.models import TimeStampedModel

from termcolor import cprint

from .Base import BaseModel
from .. import enum
from ..Decorators import autoconnect
from ..Utilities import get_client_ip
from ..uuids import get_unique_filename


class User(AbstractUser):
    """Docstring."""

    uid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        primary_key=False,
        editable=False)


# =============================================================================
# ===
# === USER PROFILE MODEL
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- User Profile Model Choices.
# -----------------------------------------------------------------------------
GenderType = enum(
    FEMALE="0",
    MALE="1",
    OTHER="2")
gender_choices = [
    (GenderType.FEMALE, _("Female")),
    (GenderType.MALE,   _("Male")),
    (GenderType.OTHER,  _("I prefer not to mention")),
]


# -----------------------------------------------------------------------------
# --- User Profile Model Manager.
# -----------------------------------------------------------------------------
class UserProfileManager(models.Manager):
    """User Profile Manager."""

    def get_queryset(self):
        """Docstring."""
        return super().get_queryset()


# -----------------------------------------------------------------------------
# --- User Profile Model.
# -----------------------------------------------------------------------------
def user_directory_path(instance, filename):
    """User Directory Path."""
    # --- File will be uploaded to
    #     MEDIA_ROOT/accounts/<id>/avatars/<filename>
    fname = get_unique_filename(filename.split("/")[-1])

    return f"accounts/{instance.user.id}/avatars/{fname}"


@autoconnect
class UserProfile(BaseModel):
    """User Profile Base Model.

    Attributes
    ----------
    user                    : obj       User.
    avatar                  : obj       Profile Avatar Image.
    nickname                : str       Profile Nickname.
    bio                     : str       Profile Bio.
    gender                  : str       Profile Gender.
    birth_day               : datetime  Profile Birthday.

    custom_data             : dict      Custom Data JSON Field.

    created_by              : obj       User, created   the Object.
    modified_by             : obj       User, modified  the Object.

    created                 : datetime  Timestamp the Object has been created.
    modified                : datetime  Timestamp the Object has been modified.

    Methods
    -------
    stat_gender_name()                  Returns Gender Name.
    full_name_straight()                Returns full   Name.
    full_name()                         Returns full   Name.
    short_name()                        Returns short  Name.
    auth_name()                         Returns Auth   Name.
    name()                              Returns        Name.

    pre_save()                          `pre_save`    Object Signal.
    post_save()                         `post_save`   Object Signal.
    pre_delete()                        `pre_delete`  Object Signal.
    post_delete()                       `posr_delete` Object Signal.
    m2m_changed()                       `m2m_changed` Object Signal.

    """

    # -------------------------------------------------------------------------
    # --- Basics
    # -------------------------------------------------------------------------
    user = models.OneToOneField(
        User,
        db_index=True,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name=_("User"),
        help_text=_("User"))
    avatar = models.ImageField(
        upload_to=user_directory_path,
        blank=True)
    nickname = models.CharField(
        db_index=True,
        max_length=32, null=True, blank=True,
        default="",
        verbose_name=_("Nickname"),
        help_text=_("User Nickname"))
    bio = models.TextField(
        null=True, blank=True,
        default="",
        verbose_name="Bio",
        help_text=_("User Bio"))

    gender = models.CharField(
        max_length=2,
        choices=gender_choices, default=GenderType.OTHER,
        verbose_name=_("Gender"),
        help_text=_("User Gender"))
    birth_day = models.DateField(
        db_index=True,
        null=True, blank=True,
        verbose_name=_("Birthday"),
        help_text=_("User Birthday"))

    USERNAME_FIELD = "email"

    objects = UserProfileManager()

    class Meta:
        verbose_name = _("user profile")
        verbose_name_plural = _("user profiles")
        ordering = [
            "user__first_name",
            "user__last_name",
        ]

        abstract = True

    def __repr__(self):
        """Docstring."""
        return f"<{self.__class__.__name__} ({self.id}: '{self.user}')>"

    def __str__(self):
        """Docstring."""
        return self.user.get_full_name()

    # -------------------------------------------------------------------------
    # --- Properties.
    # -------------------------------------------------------------------------
    @property
    def stat_gender_name(self):
        """Docstring."""
        for code, name in gender_choices:
            if self.gender == code:
                return name.lower()

        return ""

    @property
    def full_name_straight(self):
        """Docstring."""
        return self.user.first_name + " " + self.user.last_name

    @property
    def full_name(self):
        """Docstring."""
        return self.user.last_name + ", " + self.user.first_name

    @property
    def short_name(self):
        """Docstring."""
        try:
            return self.user.first_name + " " + self.user.last_name[0] + "."
        except Exception as exc:
            # -----------------------------------------------------------------
            # --- Logging.
            print(f"### EXCEPTION : {type(exc).__name__} : {str(exc)}")

            return self.user.first_name

    @property
    def auth_name(self):
        """Docstring."""
        try:
            if self.short_name:
                return self.short_name

            if self.nickname:
                return self.nickname

            return self.user.email.split("@")[0]
        except Exception as exc:
            print(f"### EXCEPTION : {type(exc).__name__} : {str(exc)}")

        return "------"

    @property
    def name(self):
        """Docstring."""
        return self.user.get_full_name()

    # -------------------------------------------------------------------------
    # --- Methods.
    # -------------------------------------------------------------------------


# =============================================================================
# ===
# === USER LOGIN MODEL
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- User Login Model Choices.
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# --- User Login Model Manager.
# -----------------------------------------------------------------------------
class UserLoginManager(models.Manager):
    """User Login Manager."""

    def get_queryset(self):
        """Docstring."""
        return super().get_queryset()

    def insert(self, request, user=None, user_agent=None, provider=None):
        """Docstring."""
        try:
            ip = get_client_ip(request)

            if not user:
                user = request.user

            if (
                    not user_agent and
                    "User-Agent" in request.headers):
                user_agent = request.headers["User-Agent"]

            if not provider:
                pass

            login = self.model(
                user=user,
                ip=ip,
                user_agent=user_agent,
                provider=provider,
                geo_data=request.geo_data)
            login.save(using=self._db)

            return login

        except Exception as exc:
            # -----------------------------------------------------------------
            # --- Logging.
            cprint(f"### EXCEPTION : {type(exc).__name__} : {str(exc)}", "red", "on_white")


# -----------------------------------------------------------------------------
# --- User Login Model.
# -----------------------------------------------------------------------------
@autoconnect
class UserLogin(TimeStampedModel):
    """User Login Model.

    Attributes
    ----------
    user                    : obj       User.
    ip                      : str       User IP Address.
    user_agent              : str       User Agent.
    provider                : str       User Internet Provider.
    geo_data                : dict      User Geolocation.

    created_by              : obj       User, created  the Object.
    modified_by             : obj       User, modified the Object.

    created                 : datetime  Timestamp the Object has been created.
    modified                : datetime  Timestamp the Object has been modified.

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
    # -------------------------------------------------------------------------
    user = models.ForeignKey(
        User,
        db_index=True,
        on_delete=models.CASCADE,
        related_name="user_login",
        verbose_name=_("User"),
        help_text=_("User"))
    ip = models.CharField(
        db_index=True,
        max_length=16,
        verbose_name=_("IP"),
        help_text=_("User IP Address"))
    user_agent = models.CharField(
        max_length=128,
        null=True, blank=True,
        verbose_name=_("User Agent"),
        help_text=_("User Agent"))
    provider = models.CharField(
        max_length=128,
        null=True, blank=True,
        verbose_name=_("Provider"),
        help_text=_("User Internet Provider"))

    # -------------------------------------------------------------------------
    # --- Geolocation.
    # -------------------------------------------------------------------------
    geo_data = JSONField(null=True, blank=True)

    objects = UserLoginManager()

    class Meta:
        verbose_name = _("user login")
        verbose_name_plural = _("user logins")
        ordering = ["-created", ]

    def __repr__(self):
        """Docstring."""
        return f"<{self.__class__.__name__} ({self.id}: '{self.user}')>"

    def __str__(self):
        """Docstring."""
        return self.__repr__()

    # -------------------------------------------------------------------------
    # --- Signals.
    # -------------------------------------------------------------------------
    def pre_save(self, **kwargs):
        """Docstring."""

    def post_save(self, created, **kwargs):
        """Docstring."""

    def pre_delete(self, **kwargs):
        """Docstring."""

    def post_delete(self, **kwargs):
        """Docstring."""

    def m2m_changed(self, **kwargs):
        """M2M changed Signal."""
