import uuid

from django.db import models


def upload_certificate(instance, filename):
    return f"certificates/{uuid.uuid4()}/{filename}"


class Product(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default="Price is not available at the moment"
    )
    certificate = models.ImageField(upload_to=upload_certificate, null=True)

    def __str__(self):
        return self.title
