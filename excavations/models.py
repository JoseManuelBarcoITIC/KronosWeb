from django.db import models

class Excavations(models.Model):  # Se llama Excavations
    name = models.CharField(max_length=30)
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="owned_excavations"
    )
    users = models.ManyToManyField(
        "users.User",
        related_name="participating_excavations"
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "excavations"

class Sectors(models.Model):
    name = models.CharField(max_length=30)
    excavation = models.ForeignKey(
        "Excavations",
        on_delete=models.CASCADE,
        related_name="sectors"
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "sectors"