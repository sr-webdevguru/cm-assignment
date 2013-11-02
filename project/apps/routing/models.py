from django.db import models


class Domains(models.Model):
    domain_id = models.AutoField(primary_key=True)
    domain = models.CharField(max_length=80)
    laravel_domain = models.CharField(max_length=80)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.domain


class RoutingCompany(models.Model):
    resort_token = models.CharField(max_length=100, unique=True)
    resort_name = models.CharField(max_length=50)
    domain = models.ForeignKey(Domains)

    def __unicode__(self):
        return self.resort_name


class RoutingUser(models.Model):
    email = models.EmailField()
    domain = models.ForeignKey(Domains)

    def __unicode__(self):
        return self.email


class Languages(models.Model):
    language_id = models.AutoField(primary_key=True)
    language_label = models.CharField(max_length=50)
    language_code = models.CharField(max_length=20)

    def __unicode__(self):
        return self.language_label
