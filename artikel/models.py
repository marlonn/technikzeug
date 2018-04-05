# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from __future__ import unicode_literals

from django.db import models

class Artikel(models.Model):
    # Field renamed to remove unsuitable characters.
    a_id = models.AutoField(db_column='a-id', primary_key=True)  
    titel = models.CharField(max_length=512)
    text = models.TextField(max_length=10000)
    tags = models.CharField(max_length=256)
    datum = models.DateField()
    bild = models.CharField(max_length=128, blank=True)
    owner = models.ForeignKey(  'auth.User',
                                related_name='artikel', 
                                on_delete=models.CASCADE,
                                null=False
                            )

    class Meta:
        managed = True 
        db_table = 'artikel'

    def __str__(self):
        return self.titel

