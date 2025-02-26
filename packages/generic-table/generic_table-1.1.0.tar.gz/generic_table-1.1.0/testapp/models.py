import pytest
from django.db import models


@pytest.mark.django_db
class TestModel(models.Model):
    status = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "test_model"
        app_label = 'testapp'  # Explicitly set the app_label

@pytest.mark.django_db
class TestRelatedModel(models.Model):
    name = models.TextField()
    related = models.ForeignKey(TestModel, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = "test_related_model"
        app_label = 'testapp'