"""(C) 2013-2025 Copycat Software, LLC. All Rights Reserved."""

from django.core.files.storage import get_storage_class

from storages.backends.s3boto3 import S3Boto3Storage


class StaticS3BotoStorage(S3Boto3Storage):
    """Docstring."""

    location = "static"
    default_acl = "public-read"


class CachedS3BotoStorage(StaticS3BotoStorage):
    """S3 Storage Backend, that saves the Files locally, too."""

    def __init__(self, *args, **kwargs):
        """Constructor."""
        super().__init__(*args, **kwargs)

        self.local_storage = get_storage_class("compressor.storage.CompressorFileStorage")()

    def save(self, name, content):
        """Docstring."""
        self.local_storage.save(name, content)

        super().save(name, self.local_storage._open(name))

        return name


class PublicMediaS3BotoStorage(S3Boto3Storage):
    """Docstring."""

    location = "media"
    default_acl = "public-read"
    file_overwrite = False


class PrivateMediaS3BotoStorage(S3Boto3Storage):
    """Docstring."""

    location = "private"
    default_acl = "private"
    file_overwrite = False
    custom_domain = False
