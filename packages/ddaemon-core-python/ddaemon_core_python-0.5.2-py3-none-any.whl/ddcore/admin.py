"""(C) 2013-2025 Copycat Software, LLC. All Rights Reserved."""

from django.contrib.contenttypes import admin as ct_admin
from django.utils.html import format_html

from ddcore.models import (
    Address,
    AttachedImage,
    AttachedDocument,
    AttachedVideoUrl,
    AttachedUrl,
    Comment,
    Complaint,
    Phone,
    Rating,
    SocialLink,
    View)


# =============================================================================
# ===
# === IMAGES ADMIN MIXIN
# ===
# =============================================================================
class ImagesAdminMixin:
    """Mixin for displaying Images in Django Admin."""

    def image_tag(self, obj):
        """Render Image Thumbnail."""
        if obj.image:
            return format_html(f"<img src='{obj.image.url}' width='60' height='60' />")

        return "(Sin Imagen)"

    image_tag.short_description = "Image"
    image_tag.allow_tags = True

    def avatar_image_tag(self, obj):
        """Render Avatar Thumbnail."""
        if obj.avatar:
            return format_html(f"<img src='{obj.avatar.url}' width='60' height='60' />")

        return "(Sin Imagen)"

    avatar_image_tag.short_description = "Avatar"
    avatar_image_tag.allow_tags = True

    def preview_image_tag(self, obj):
        """Render Preview Thumbnail."""
        if obj.preview:
            return format_html(f"<img src='{obj.preview.url}' width='100' height='60' />")

        return "(Sin Imagen)"

    preview_image_tag.short_description = "Preview"
    preview_image_tag.allow_tags = True

    def cover_image_tag(self, obj):
        """Render Cover Thumbnail."""
        if obj.cover:
            return format_html(f"<img src='{obj.cover.url}' width='100' height='60' />")

        return "(Sin Imagen)"

    cover_image_tag.short_description = "Cover"
    cover_image_tag.allow_tags = True


# =============================================================================
# ===
# === INLINES
# ===
# =============================================================================
class AddressInline(ct_admin.GenericTabularInline):
    """Address Inline."""

    classes = [
        "grp-collapse grp-open",
    ]
    inline_classes = [
        "grp-collapse grp-open",
    ]
    fields = [
        "id", "address_1", "address_2", "city", "zip_code", "province", "country",
        "created_by", "created", "modified_by", "modified",
    ]
    readonly_fields = [
        "created", "modified",
    ]

    model = Address
    extra = 1


class AttachedImageInline(ct_admin.GenericTabularInline):
    """Social Link Inline."""

    classes = [
        "grp-collapse grp-closed",
    ]
    inline_classes = [
        "grp-collapse grp-closed",
    ]
    fields = [
        "id", "name",
        "created_by", "created", "modified_by", "modified",
    ]
    readonly_fields = [
        "created", "modified",
    ]

    model = AttachedImage
    extra = 1


class AttachedDocumentInline(ct_admin.GenericTabularInline):
    """Social Link Inline."""

    classes = [
        "grp-collapse grp-closed",
    ]
    inline_classes = [
        "grp-collapse grp-closed",
    ]
    fields = [
        "id", "name",
        "created_by", "created", "modified_by", "modified",
    ]
    readonly_fields = [
        "created", "modified",
    ]

    model = AttachedDocument
    extra = 1


class AttachedVideoUrlInline(ct_admin.GenericTabularInline):
    """Social Link Inline."""

    classes = [
        "grp-collapse grp-closed",
    ]
    inline_classes = [
        "grp-collapse grp-closed",
    ]
    fields = [
        "id", "url",
        "created_by", "created", "modified_by", "modified",
    ]
    readonly_fields = [
        "created", "modified",
    ]

    model = AttachedVideoUrl
    extra = 1


class AttachedUrlInline(ct_admin.GenericTabularInline):
    """Social Link Inline."""

    classes = [
        "grp-collapse grp-closed",
    ]
    inline_classes = [
        "grp-collapse grp-closed",
    ]
    fields = [
        "id", "title", "url",
        "created_by", "created", "modified_by", "modified",
    ]
    readonly_fields = [
        "created", "modified",
    ]

    model = AttachedUrl
    extra = 1


class CommentInline(ct_admin.GenericTabularInline):
    """Comment Inline."""

    classes = [
        "grp-collapse grp-closed",
    ]
    inline_classes = [
        "grp-collapse grp-closed",
    ]
    fields = [
        "id", "text", "is_deleted",
        "created_by", "created", "modified_by", "modified",
    ]
    readonly_fields = [
        "created", "modified",
    ]

    model = Comment
    extra = 1


class ComplaintInline(ct_admin.GenericTabularInline):
    """Complaint Inline."""

    classes = [
        "grp-collapse grp-closed",
    ]
    inline_classes = [
        "grp-collapse grp-closed",
    ]
    fields = [
        "id", "text", "is_processed", "is_deleted",
        "created_by", "created", "modified_by", "modified",
    ]
    readonly_fields = [
        "created", "modified",
    ]

    model = Complaint
    extra = 1


class PhoneNumberInline(ct_admin.GenericTabularInline):
    """Phone Number Inline."""

    classes = [
        "grp-collapse grp-open",
    ]
    inline_classes = [
        "grp-collapse grp-open",
    ]
    fields = [
        "id", "phone_type", "phone_number", "phone_number_ext",
        "created_by", "created", "modified_by", "modified",
    ]
    readonly_fields = [
        "created", "modified",
    ]

    model = Phone
    extra = 1


class RatingInline(ct_admin.GenericTabularInline):
    """Rating Inline."""

    classes = [
        "grp-collapse grp-closed",
    ]
    inline_classes = [
        "grp-collapse grp-closed",
    ]
    fields = [
        "id", "rating", "review_text",
        "created_by", "created", "modified_by", "modified",
    ]
    readonly_fields = [
        "created", "modified",
    ]

    model = Rating
    extra = 1


class SocialLinkInline(ct_admin.GenericTabularInline):
    """Social Link Inline."""

    classes = [
        "grp-collapse grp-open",
    ]
    inline_classes = [
        "grp-collapse grp-open",
    ]
    fields = [
        "id", "social_app", "url",
        "created_by", "created", "modified_by", "modified",
    ]
    readonly_fields = [
        "created", "modified",
    ]

    model = SocialLink
    extra = 1


class ViewInline(ct_admin.GenericTabularInline):
    """View Inline."""

    classes = [
        "grp-collapse grp-closed",
    ]
    inline_classes = [
        "grp-collapse grp-closed",
    ]
    fields = [
        "id", "viewer",
        "created_by", "created", "modified_by", "modified",
    ]
    readonly_fields = [
        "created", "modified",
    ]

    model = View
    extra = 1
