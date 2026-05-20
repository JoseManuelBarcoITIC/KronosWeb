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
from django.db import models

class StratigraphicUnit(models.Model):
    DEFINITION_CHOICES = [
        ('layer', 'Layer'),
        ('structure', 'Structure'),
        ('cut', 'Cut'),
    ]

    sector = models.ForeignKey(
        "Sectors",
        on_delete=models.CASCADE,
        related_name="stratigraphic_units"
    )
    ue_number = models.PositiveIntegerField()
    definition = models.CharField(max_length=15, choices=DEFINITION_CHOICES, default='layer')

    length = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    width = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    top_elevation = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    bottom_elevation = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    sheet_data = models.JSONField(default=dict, blank=True)
    site_photo = models.ImageField(upload_to="ue_photos/%Y/%m/", blank=True, null=True)

    relations = models.ManyToManyField(
        'self',
        through='UERelationship',
        through_fields=('from_ue', 'to_ue'),
        symmetrical=False,
        related_name='related_by'
    )

    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "stratigraphic_units"
        unique_together = ('sector', 'ue_number')

    def __str__(self):
        return f"UE {self.ue_number} (Sector: {self.sector.name})"


class UERelationship(models.Model):
    RELATION_TYPES = [
        ('covers', 'Covers / Covered by'),
        ('fills', 'Fills / Filled by'),
        ('cuts', 'Cuts / Cut by'),
        ('leans', 'Leans / Leaned by'),
        ('abuts', 'Abuts / Abutted by'),
        ('equal', 'Equal to'),
    ]

    from_ue = models.ForeignKey(StratigraphicUnit, on_delete=models.CASCADE, related_name='from_relations')
    to_ue = models.ForeignKey(StratigraphicUnit, on_delete=models.CASCADE, related_name='to_relations')
    type_relation = models.CharField(max_length=15, choices=RELATION_TYPES)

    class Meta:
        db_table = "ue_relationships"
        unique_together = ('from_ue', 'to_ue', 'type_relation')