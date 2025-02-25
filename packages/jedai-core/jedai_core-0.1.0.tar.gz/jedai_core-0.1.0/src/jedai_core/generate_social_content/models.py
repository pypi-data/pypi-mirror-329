from django.db import models
from marketing_bot.models import User


# Create your models here.
class LiveSettings(models.Model):
    model = models.CharField(max_length=32, primary_key=True)
    api_key = models.TextField()
    config = models.JSONField()

    def __str__(self):
        return self.model


class Inference(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    detailed_instructions = models.TextField()
    model_alias = models.CharField(max_length=128)
    response = models.TextField()
    run_on = models.DateTimeField(auto_now_add=True)
    runtime = models.DecimalField(max_digits=11, decimal_places=2)

    def __str__(self):
        return self.model_alias
