from django.db import models


class BaseModel(models.Model):
    """
    The common field in all the models are defined here
    """

    # A timestamp representing when this object was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # A timestamp reprensenting when this object was last updated.
    updated_at = models.DateTimeField(auto_now=True)

    # add deleted option for every entry
    deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super(BaseModel, self).save()

    class Meta:
        abstract = True
