from typing import Any
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

alpha = RegexValidator(r'^[a-zA-Z]*$', 'Only alphabetic characters are allowed.')


class Workspace(models.Model):
    creator = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    members = models.CharField(max_length=255)

    def __str__(self) -> str:
        return str(self.name)

class Columns(models.Model):
    name = models.CharField(max_length=255)
    workspace = models.ForeignKey(Workspace, on_delete=models.PROTECT,default="")

    def __str__(self) -> str:
        return str(self.name)


class Cards(models.Model):
    title = models.CharField(validators=[alpha],max_length=255)
    description = models.CharField(max_length=25)
    column = models.ForeignKey(Columns, on_delete=models.CASCADE)

