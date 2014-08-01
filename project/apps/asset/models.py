import uuid

from django.db import models

from apps.resorts.models import ResortLocation, Resort

LIVE = 0
DELETED = 1
ASSET_STATUS = (
    (LIVE, 'live'),
    (DELETED, 'deleted')
)

ASSET_TYPE_STATUS = (
    (LIVE, 'live'),
    (DELETED, 'deleted')
)


class AssetType(models.Model):
    asset_type_pk = models.AutoField(primary_key=True, db_column="asset_type_pk", verbose_name="asset type pk")
    asset_type_id = models.UUIDField(db_column="asset_type_id", verbose_name="asset type id", default=uuid.uuid4,
                                     editable=False)
    asset_type_name = models.CharField(db_column="asset_type_name", verbose_name="asset type name", max_length=140,
                                       blank=False, null=False)
    asset_type_status = models.IntegerField(db_column="asset_type_status", verbose_name="asset type status",
                                            choices=ASSET_TYPE_STATUS, default=LIVE)
    resort = models.ForeignKey(Resort, db_column="resort", verbose_name="resort")

    def __unicode__(self):
        return self.asset_type_name


class Assets(models.Model):
    asset_pk = models.AutoField(primary_key=True, db_column="asset_pk", verbose_name="asset pk")
    asset_id = models.UUIDField(db_column="asset_id", verbose_name="asset id", default=uuid.uuid4, editable=False)
    location = models.ForeignKey(ResortLocation, db_column="location", verbose_name="location")
    asset_type = models.ForeignKey(AssetType, db_column="asset_type", verbose_name="asset type")
    asset_name = models.CharField(db_column="asset_name", verbose_name="asset name", max_length=140, blank=False,
                                  null=False)
    asset_status = models.IntegerField(db_column="asset_status", verbose_name="asset status", choices=ASSET_STATUS,
                                       default=LIVE)
    resort = models.ForeignKey(Resort, db_column="resort", verbose_name="resort")
