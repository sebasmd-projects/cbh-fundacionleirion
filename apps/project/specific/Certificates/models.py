import hashlib

from django.db import models
from django.urls import reverse


class CertificateModel(models.Model):
    nombre = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20)
    short_url = models.URLField(blank=True, null=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    contador_total = models.IntegerField(default=0)
    contador_unicos = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.short_url:
            hash_value = hashlib.sha256(
                f'{self.nombre}{self.cedula}{self.fecha_creacion}'.encode()
            ).hexdigest()[:6]
            self.short_url = reverse('certificado_detail', args=[hash_value])
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Certificado - {self.nombre}'


class CertificateValidationModel(models.Model):
    certificado = models.ForeignKey(CertificateModel, on_delete=models.CASCADE)
    fecha_lectura = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField()
    user_agent = models.TextField()
    geo_info = models.JSONField(default=dict)

    def __str__(self):
        return f'Lectura - {self.certificado.nombre} en {self.fecha_lectura}'
