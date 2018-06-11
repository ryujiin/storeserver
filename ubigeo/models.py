from django.db import models
from django.core.exceptions import ValidationError


class Departamento(models.Model):
    coddpto = models.CharField('Code', max_length=2, db_index=True)
    nom_dpto = models.CharField('Departamento', max_length=50)

    class Meta:
        ordering = ('nom_dpto', )

    def __str__(self):
        return self.nom_dpto


class Provincia(models.Model):
    idprov = models.CharField('IDProv', max_length=4, db_index=True)
    coddpto = models.CharField('Code Departamento', max_length=2, db_index=True)
    nom_dpto = models.CharField('Departamento', max_length=50)
    codprov = models.CharField('Code Provincia', max_length=2, db_index=True)
    nom_prov = models.CharField('Provincia', max_length=50)

    class Meta:
        ordering = ('nom_dpto', 'nom_prov')

    def __str__(self):
        return self.nom_prov


class Distrito(models.Model):
    iddist = models.CharField('IDDist', max_length=6, db_index=True)
    coddpto = models.CharField('Code Departamento', max_length=2, db_index=True)
    nom_dpto = models.CharField('Departamento', max_length=50)
    codprov = models.CharField('Code Provincia', max_length=2, db_index=True)
    nom_prov = models.CharField('Provincia', max_length=50)
    coddist = models.CharField('Code Distrito', max_length=2, db_index=True)
    nom_dist = models.CharField('Distrito', max_length=50)

    class Meta:
        ordering = ('nom_dpto', 'nom_prov', 'nom_dist')

    def __str__(self):
        return self.nom_dist
