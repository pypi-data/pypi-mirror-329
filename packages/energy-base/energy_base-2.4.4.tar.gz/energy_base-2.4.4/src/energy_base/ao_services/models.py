from urllib.parse import urljoin

from django.db import models

from .constants import AOServices


class AOServiceManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().using('ao_services')


class AOService(models.Model):
    class Type(models.TextChoices):
        FILE_UPLOAD = 'FILE_UPLOAD'
        API_INTEGRATION = 'API_INTEGRATION'
        ADMIN = 'ADMIN'

    objects = AOServiceManager()
    name = models.CharField(max_length=255)
    title_translate_key = models.CharField(max_length=255)
    logo = models.FileField(upload_to='media/logo')
    type = models.CharField(max_length=20, choices=Type.choices)
    references_count = models.PositiveSmallIntegerField()
    ip = models.GenericIPAddressField()
    port = models.PositiveSmallIntegerField()

    def get_url(self, prefix: str):
        return urljoin(f'http://{self.ip}:{self.port}', prefix)

    def get_file_upload_status_url(self):
        return self.get_url('/api/file-upload-status/')

    def get_external_api_status_url(self):
        return self.get_url('/api/admin/external-api/status/')

    @staticmethod
    def get_by_name(name: AOServices):
        return AOService.objects.filter(name=name).first()

    class Meta:
        ordering = ['name']
        app_label = 'main'
