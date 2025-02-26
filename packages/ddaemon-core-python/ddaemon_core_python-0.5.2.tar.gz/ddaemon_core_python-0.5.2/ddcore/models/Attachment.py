"""(C) 2013-2025 Copycat Software, LLC. All Rights Reserved."""

from datetime import datetime

from django.contrib.contenttypes import fields
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from .Base import BaseModel
from .. import enum
from ..Decorators import autoconnect
from ..Utilities import get_youtube_video_id
from ..uuids import get_unique_filename


# =============================================================================
# ===
# === TEMPORARY FILE MODEL
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- Temporary File Model Choices.
# -----------------------------------------------------------------------------
UploadType = enum(
    DOCUMENT="document",
    IMAGE="image",
    VIDEO="video",
    AUDIO="audio",
    OTHER="other")
upload_type_choices = [
    (UploadType.DOCUMENT,   _("Document")),
    (UploadType.IMAGE,      _("Image")),
    (UploadType.VIDEO,      _("Video")),
    (UploadType.AUDIO,      _("Audio")),
    (UploadType.OTHER,      _("Other")),
]


# -----------------------------------------------------------------------------
# --- Temporary File Model Manager.
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# --- Temporary File Model.
# -----------------------------------------------------------------------------
def tmp_directory_path(instance, filename):
    """Temporary File Directory Path."""
    # --- File Will be uploaded to
    #     MEDIA_ROOT/tmp/<YYYY>/<MM>/<DD>/<filename>
    today = datetime.today().strftime("%Y/%m/%d")

    return f"tmp/{today}/{filename}"


@autoconnect
class TemporaryFile(BaseModel):
    """Temporary File Model.

    Attributes
    ----------
    file                    : obj       File Object.
    name                    : str       File Name.
    upload_type             : str       File Type.

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
    # -------------------------------------------------------------------------
    file = models.FileField(upload_to=tmp_directory_path)
    name = models.CharField(max_length=255)

    upload_type = models.CharField(
        max_length=10,
        choices=upload_type_choices, default=UploadType.OTHER,
        verbose_name=_("Type"),
        help_text=_("Upload Type"))

    # TODO Write cron job for deleting old, not used temporary files,
    # e.g. when submitting form was canceled.

    def __repr__(self):
        """Docstring."""
        return f"<{self.__class__.__name__} ({self.id}: '{self.file.name}')>"

    def __str__(self):
        """Docstring."""
        return self.__repr__()

    class Meta:
        verbose_name = _("temporary file")
        verbose_name_plural = _("temporary files")
        ordering = ["-id", ]

    def pre_save(self, **kwargs):
        """Docstring."""

    def post_save(self, created, **kwargs):
        """Docstring."""

    def pre_delete(self, **kwargs):
        """Docstring."""
        try:
            self.file.delete()
        except:
            pass

    def post_delete(self, **kwargs):
        """Docstring."""


# =============================================================================
# ===
# === ATTACHMENT MODEL
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- Attachment Model Manager.
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# --- Attachment Model.
# -----------------------------------------------------------------------------
def attachment_image_directory_path(instance, filename):
    """Attachment Image Directory Path."""
    # --- File Will be uploaded to
    #     MEDIA_ROOT/<ct_name>/<ct_object_id>/attachments/images/<filename>
    fname = get_unique_filename(filename.split("/")[-1])

    return f"{instance.content_type.name}s/{instance.object_id}/attachments/images/{fname}"


def attachment_document_directory_path(instance, filename):
    """Attachment Document Directory Path."""
    # --- File Will be uploaded to
    #     MEDIA_ROOT/<ct_name>/<ct_object_id>/attachments/documents/<filename>
    fname = get_unique_filename(filename.split("/")[-1])

    return f"{instance.content_type.name}s/{instance.object_id}/attachments/documents/{fname}"


@autoconnect
class AttachedImage(BaseModel):
    """Attached Image Model.

    Attributes
    ----------
    name                    : str       File Name.
    image                   : obj       File Object.
    is_hidden               : bool      Is hidden?
    is_private              : bool      Is private?

    content_type            : obj       Content Type.
    object_id               : int       Object  ID.
    content_object          : obj       Content Object.

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
    # -------------------------------------------------------------------------
    name = models.CharField(
        db_index=True,
        max_length=255, null=True, blank=True,
        verbose_name=_("Name"),
        help_text=_("File Name"))
    image = models.ImageField(upload_to=attachment_image_directory_path)

    # -------------------------------------------------------------------------
    # --- Flags.
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # --- Content Type.
    # -------------------------------------------------------------------------
    content_type = models.ForeignKey(
        ContentType,
        null=True, blank=True, default=None,
        on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(null=True, blank=True, default=None)
    content_object = fields.GenericForeignKey("content_type", "object_id")

    def __repr__(self):
        """Docstring."""
        return f"<{self.__class__.__name__} ({self.id}: '{self.content_object}')>"

    def __str__(self):
        """Docstring."""
        return self.__repr__()

    class Meta:
        verbose_name = _("attached image")
        verbose_name_plural = _("attached images")
        ordering = ["-id", ]

    def pre_save(self, **kwargs):
        """Docstring."""

    def post_save(self, created, **kwargs):
        """Docstring."""

    def pre_delete(self, **kwargs):
        """Docstring."""
        try:
            self.image.delete()
        except Exception as exc:
            print(f"### EXCEPTION : {str(exc)}")

    def post_delete(self, **kwargs):
        """Docstring."""


@autoconnect
class AttachedDocument(BaseModel):
    """Attached Document Model

    Attributes
    ----------
    name                    : str       File Name.
    document                : obj       File Object.
    is_hidden               : bool      Is hidden?
    is_private              : bool      Is private?

    content_type            : obj       Content Type.
    object_id               : int       Object  ID.
    content_object          : obj       Content Object.

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
    # -------------------------------------------------------------------------
    name = models.CharField(
        db_index=True,
        max_length=255, null=True, blank=True,
        verbose_name=_("Name"),
        help_text=_("File Name"))
    document = models.FileField(upload_to=attachment_document_directory_path)

    # -------------------------------------------------------------------------
    # --- Flags.
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # --- Content Type.
    # -------------------------------------------------------------------------
    content_type = models.ForeignKey(
        ContentType,
        null=True, blank=True, default=None,
        on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(null=True, blank=True, default=None)
    content_object = fields.GenericForeignKey("content_type", "object_id")

    def __repr__(self):
        """Docstring."""
        return f"<{self.__class__.__name__} ({self.id}: '{self.content_object}')>"

    def __str__(self):
        """Docstring."""
        return self.__repr__()

    def url(self):
        """Docstring."""
        return self.document.url

    class Meta:
        verbose_name = _("attached document")
        verbose_name_plural = _("attached documents")
        ordering = ["-id", ]

    def pre_save(self, **kwargs):
        """Docstring."""

    def post_save(self, created, **kwargs):
        """Docstring."""

    def pre_delete(self, **kwargs):
        """Docstring."""
        try:
            self.document.delete()
        except Exception as exc:
            print(f"### EXCEPTION : {str(exc)}")

    def post_delete(self, **kwargs):
        """Docstring."""


@autoconnect
class AttachedUrl(BaseModel):
    """Attached URL Model.

    Attributes
    ----------
    url                     : str       URL Address.
    title                   : str       URL Title.
    is_hidden               : bool      Is hidden?
    is_private              : bool      Is private?

    content_type            : obj       Content Type.
    object_id               : int       Object  ID.
    content_object          : obj       Content Object.

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
    # -------------------------------------------------------------------------
    url = models.URLField()
    title = models.CharField(
        db_index=True,
        max_length=255, null=True, blank=True,
        verbose_name=_("Title"),
        help_text=_("URL Title"))

    # -------------------------------------------------------------------------
    # --- Flags.
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # --- Content Type.
    # -------------------------------------------------------------------------
    content_type = models.ForeignKey(
        ContentType,
        null=True, blank=True, default=None,
        on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(null=True, blank=True, default=None)
    content_object = fields.GenericForeignKey("content_type", "object_id")

    def __repr__(self):
        """Docstring."""
        return f"<{self.__class__.__name__} ({self.id}: '{self.content_object}')>"

    def __str__(self):
        """Docstring."""
        return self.__repr__()

    class Meta:
        verbose_name = _("attached url")
        verbose_name_plural = _("attached urls")
        ordering = ["-id", ]

    def pre_save(self, **kwargs):
        """Docstring."""

    def post_save(self, created, **kwargs):
        """Docstring."""

    def pre_delete(self, **kwargs):
        """Docstring."""

    def post_delete(self, **kwargs):
        """Docstring."""


@autoconnect
class AttachedVideoUrl(BaseModel):
    """Attached Video URL Model.

    Attributes
    ----------
    url                     : obj       URL Address.
    is_hidden               : bool      Is hidden?
    is_private              : bool      Is private?

    content_type            : obj       Content Type.
    object_id               : int       Object  ID.
    content_object          : obj       Content Object.

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
    # -------------------------------------------------------------------------
    url = models.URLField()

    # -------------------------------------------------------------------------
    # --- Flags.
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # --- Content Type.
    # -------------------------------------------------------------------------
    content_type = models.ForeignKey(
        ContentType,
        null=True, blank=True, default=None,
        on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(null=True, blank=True, default=None)
    content_object = fields.GenericForeignKey("content_type", "object_id")

    def __repr__(self):
        """Docstring."""
        return f"<{self.__class__.__name__} ({self.id}: '{self.content_object}')>"

    def __str__(self):
        """Docstring."""
        return self.__repr__()

    def get_youtube_video_id(self):
        """Docstring."""
        return get_youtube_video_id(self.url)

    class Meta:
        verbose_name = _("attached video url")
        verbose_name_plural = _("attached video urls")
        ordering = ["-id", ]

    def pre_save(self, **kwargs):
        """Docstring."""

    def post_save(self, created, **kwargs):
        """Docstring."""

    def pre_delete(self, **kwargs):
        """Docstring."""

    def post_delete(self, **kwargs):
        """Docstring."""


# -----------------------------------------------------------------------------
# --- Attachment Model Mixin.
# -----------------------------------------------------------------------------
class AttachmentMixin:
    """Attachment Mixin Class.

    Methods
    -------

    Properties
    ----------
    image_list                          Return a List of attached Images.
    image_count                         Return a Number of attached Images.
    document_list                       Return a List of attached Documents.
    document_count                      Return a Number of attached Documents.
    url_list                            Return a List of attached URLs.
    url_count                           Return a Number of attached URLs.
    video_url_list                      Return a List of attached Videos.
    video_url_count                     Return a Number of attached Videos.

    """

    # -------------------------------------------------------------------------
    # --- Get List of Attachments.
    # -------------------------------------------------------------------------
    @property
    def image_list(self):
        """Return a List of attached Images."""
        return AttachedImage.objects.filter(
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.id,
        ).order_by("-created")

    @property
    def image_count(self):
        """Return a Number of attached Images."""
        return self.image_list.count()

    @property
    def document_list(self):
        """Return a List of attached Documents."""
        return AttachedDocument.objects.filter(
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.id,
        ).order_by("-created")

    @property
    def document_count(self):
        """Return a Number of attached Documents."""
        return self.document_list.count()

    @property
    def url_list(self):
        """Return a List of attached URLs."""
        return AttachedUrl.objects.filter(
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.id,
        ).order_by("-created")

    @property
    def url_count(self):
        """Return a Number of attached URLs."""
        return self.url_list.count()

    @property
    def video_url_list(self):
        """Return a List of attached Videos."""
        return AttachedVideoUrl.objects.filter(
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.id,
        ).order_by("-created")

    @property
    def video_url_count(self):
        """Return a Number of attached Videos."""
        return self.video_url_list.count()
