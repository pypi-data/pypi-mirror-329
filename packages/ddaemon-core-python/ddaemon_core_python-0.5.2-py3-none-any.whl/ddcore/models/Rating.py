"""(C) 2013-2025 Copycat Software, LLC. All Rights Reserved."""

from django.conf import settings
from django.contrib.contenttypes import fields
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _

from annoying.functions import get_object_or_None

from .Base import BaseModel
from ..Decorators import autoconnect


# =============================================================================
# ===
# === RATING MODEL
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- Rating Model Manager.
# -----------------------------------------------------------------------------
class RatingManager(models.Manager):
    """Rating Manager."""

    def get_queryset(self):
        """Docstring."""
        return super().get_queryset()


# -----------------------------------------------------------------------------
# --- Rating Model.
# -----------------------------------------------------------------------------
@autoconnect
class Rating(BaseModel):
    """Rating Model.

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
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        db_index=True,
        on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        db_index=True,
        default=0)

    # -------------------------------------------------------------------------
    # --- Significant Texts.
    review_text = models.TextField(
        null=True, blank=True,
        verbose_name=_("Review Text"),
        help_text=_("Review Text"))

    # -------------------------------------------------------------------------
    # --- Content Type.
    content_type = models.ForeignKey(
        ContentType,
        null=True, blank=True, default=None,
        on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(null=True, blank=True, default=None)
    content_object = fields.GenericForeignKey("content_type", "object_id")

    objects = RatingManager()

    class Meta:
        verbose_name = _("rating")
        verbose_name_plural = _("ratings")
        ordering = ["-id", ]

    def __repr__(self):
        """Docstring."""
        return f"<{self.__class__.__name__} ({self.content_object}: '{self.rating}')>"

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
# --- Rating Model Mixin.
# -----------------------------------------------------------------------------
class RatingMixin:
    """Rating Mixin Class.

    Methods
    -------
    is_rated_by_user()                  Return True, if authenticated User rated the Object.
    get_rating_percent_for()

    Properties
    ----------
    rating_avg                          Return average Rating.
    rating_avg_float                    Return average rating as float.
    rating_5_percent                    Return Ratio of "5-Star" ratings.
    rating_4_percent                    Return Ratio of "4-Star" ratings.
    rating_3_percent                    Return Ratio of "3-Star" ratings.
    rating_2_percent                    Return Ratio of "2-Star" ratings.
    rating_1_percent                    Return Ratio of "1-Star" ratings.
    review_list                         Return a List of Reviews.
    rating_count                        Return a Count of Ratings.

    """

    # -------------------------------------------------------------------------
    # --- Ratings and Reviews
    def is_rated_by_user(self, user):
        """Return True, if authenticated User rated the Object."""
        is_rated = get_object_or_None(
            Rating,
            author=user,
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.id)

        if is_rated:
            return True

        return False

    def get_rating_percent_for(self, rating):
        """Docsrting."""
        rating_count = Rating.objects.filter(
            rating=rating,
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.id,
        ).count()

        try:
            return int((rating_count / float(self.get_rating_count)) * 100)
        except Exception as exc:
            print(f"### EXCEPTION : {str(exc)}")

        return 0

    @property
    def rating_avg(self):
        """Return average Rating."""
        rating_sum = Rating.objects.filter(
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.id,
        ).aggregate(Sum("rating"))

        try:
            if rating_sum["rating__sum"]:
                return rating_sum["rating__sum"] / self.get_rating_count
        except Exception as exc:
            print(f"### EXCEPTION : {str(exc)}")

        return 0

    @property
    def rating_avg_float(self):
        """Return average rating as float."""
        rating_sum = Rating.objects.filter(
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.id,
        ).aggregate(Sum("rating"))

        try:
            if rating_sum["rating__sum"]:
                return round(rating_sum["rating__sum"] / float(self.get_rating_count), 2)
        except Exception as exc:
            print(f"### EXCEPTION : {str(exc)}")

        return 0.0

    @property
    def rating_5_percent(self):
        """Return Ratio of "5-Star" ratings."""
        return self.get_rating_percent_for(5)

    @property
    def rating_4_percent(self):
        """Return Ratio of "4-Star" ratings."""
        return self.get_rating_percent_for(4)

    @property
    def rating_3_percent(self):
        """Return Ratio of "3-Star" ratings."""
        return self.get_rating_percent_for(3)

    @property
    def rating_2_percent(self):
        """Return Ratio of "2-Star" ratings."""
        return self.get_rating_percent_for(2)

    @property
    def rating_1_percent(self):
        """Return Ratio of "1-Star" ratings."""
        return self.get_rating_percent_for(1)

    @property
    def review_list(self):
        """Return a List of Reviews."""
        return Rating.objects.filter(
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.id,
        ).order_by("-created")

    @property
    def rating_count(self):
        """Return a Count of Ratings."""
        return self.review_list.count()
