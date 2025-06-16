from django.db import models

class Structure(models.Model):
    photo = models.FileField(blank=True, null=True)
    nom = models.CharField(max_length=255)
    designation = models.CharField(max_length=255, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom