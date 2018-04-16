from django.db import models

# Create your models here.


class AdministratorInfo(models.Model):
    nid = models.AutoField(primary_key=True)
    ad_phone = models.CharField(max_length=32)
    ad_password = models.CharField(max_length=64)

    def __unicode__(self):
        return self.ad_password
