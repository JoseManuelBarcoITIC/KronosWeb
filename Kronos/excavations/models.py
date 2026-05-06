from django.db import models

class Excavations(models.Model):
    name = models.CharField(max_length=30)
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE,related_name="excavation_owner")
    users = models.ManyToManyField("users.User")

    class Meta:
        db_table = "excavations"

class Sectors(models.Model):
    name = models.CharField(max_length=30)
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE,related_name="excavation_owner")
    excavationid = models.ForeignKey(
        "Excavations",
        on_delete=models.CASCADE,
        related_name="sectors"
    )

    class Meta:
        db_table = "sectors"


