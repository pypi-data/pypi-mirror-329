"""(C) 2013-2025 Copycat Software, LLC. All Rights Reserved."""

from django.conf import settings
from django.contrib.contenttypes import fields
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from annoying.functions import get_object_or_None

from .Base import BaseModel
from ..Decorators import autoconnect
from ..SendgridUtil import send_templated_email


# =============================================================================
# ===
# === COMPLAINT MODEL
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- Complaint Model Manager.
# -----------------------------------------------------------------------------
class ComplaintManager(models.Manager):
    """Complaint Manager."""

    def get_queryset(self):
        """Docstring."""
        return super().get_queryset()


# -----------------------------------------------------------------------------
# --- Complaint Model.
# -----------------------------------------------------------------------------
@autoconnect
class Complaint(BaseModel):
    """Complaint Model.

    Attributes
    ----------
    author                  : obj       User.
    text                    : str       Complaint Text.

    is_processed            : bool      Is processed?
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
        help_text=_("Complaint Text"))

    # -------------------------------------------------------------------------
    # --- Flags.
    is_processed = models.BooleanField(
        default=False,
        verbose_name=_("Is processed?"),
        help_text=_("Is Complaint processed?"))
    is_deleted = models.BooleanField(
        default=False,
        verbose_name=_("Is deleted?"),
        help_text=_("Is Complaint deleted?"))

    # -------------------------------------------------------------------------
    # --- Content Type.
    content_type = models.ForeignKey(
        ContentType,
        null=True, blank=True, default=None,
        on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(null=True, blank=True, default=None)
    content_object = fields.GenericForeignKey("content_type", "object_id")

    objects = ComplaintManager()

    class Meta:
        verbose_name = _("complaint")
        verbose_name_plural = _("complaints")
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

    # -------------------------------------------------------------------------
    # --- Methods.
    def email_notify_admins_complaint_created(self, request):
        """Send Notification to the Platform Admins."""
        for admin_name, admin_email in settings.ADMINS:
            # -----------------------------------------------------------------
            # --- Render HTML Email Content.
            greetings = _(
                "Dear, %(user)s.") % {
                    "user":     admin_name,
                }
            htmlbody = _(
                "<p>Member \"<a href=\"%(profile)s\">%(member)s</a>\" has reported Complaint to %(subject)s \"<a href=\"%(url)s\">%(name)s</a>\" with the following:</p>"
                "<p>%(text)s</p>"
                "<p>Please, don\'t forget to take some Action.</p>") % {
                    "user":     admin_name,
                    "member":   self.author.get_full_name(),
                    "profile":  self.author.profile.public_url(request),
                    "subject":  self.content_type.name.capitalize(),
                    "url":      self.content_object.public_url(request),
                    "name":     self.content_object.name,
                    "text":     self.text,
                }

            # -----------------------------------------------------------------
            # --- Send Email.
            send_templated_email(
                template_subj={
                    "name":     "common/emails/complaint_created_adm_subject.txt",
                    "context":  {},
                },
                template_text={
                    "name":     "common/emails/complaint_created_adm.txt",
                    "context":  {
                        "author":   self.author.get_full_name(),
                        "profile":  self.author.profile.public_url(request),
                        "subject":  self.content_type.name.capitalize(),
                        "url":      self.content_object.public_url(request),
                        "name":     self.content_object.name,
                        "text":     self.text,
                    },
                },
                template_html={
                    "name":     "emails/base.html",
                    "context":  {
                        "greetings":    greetings,
                        "htmlbody":     htmlbody,
                    },
                },
                from_email=settings.EMAIL_SENDER,
                to=[
                    admin_email,
                ],
                headers=None,
            )


# -----------------------------------------------------------------------------
# --- Complaint Model Mixin.
# -----------------------------------------------------------------------------
class ComplaintMixin:
    """Complaint Mixin Class.

    Methods
    -------
    is_complained_by_user()             Return True, if authenticated User complained about Object.

    Properties
    ----------
    complaint_list                      Return a List of Complaints.
    complaints_count                    Return a Count of Complaints.

    """

    # -------------------------------------------------------------------------
    # --- Complaints
    def is_complained_by_user(self, user):
        """Return True, if authenticated User complained about Object."""
        is_complained = get_object_or_None(
            Complaint,
            author=user,
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.id,
            is_processed=False,
            is_deleted=False)

        if is_complained:
            return True

        return False

    @property
    def complaint_list(self):
        """Return a List of Complaints."""
        return Complaint.objects.filter(
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.id,
            is_deleted=False,
        ).order_by("-created")

    @property
    def complaints_count(self):
        """Return a Count of Complaints."""
        return self.complaint_list.count()
