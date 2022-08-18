# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models




class Clientes(models.Model):
    id = models.IntegerField( primary_key=True)
    nombre = models.TextField(blank=True, null=True)
    apellido = models.TextField(blank=True, null=True)
    sexo_id = models.TextField(blank=True, null=True)
    edad = models.IntegerField(blank=True, null=True)
    cliente_id = models.IntegerField(blank=True, null=True)
    categoria = models.TextField(blank=True, null=True)
    sucursal = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clientes'


class Cuentas(models.Model):
    id = models.IntegerField(primary_key=True)
    cliente_id = models.IntegerField(blank=True, null=True)
    saldo = models.IntegerField(blank=True, null=True)
    tipo = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cuentas'



class Empleados(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.TextField(blank=True, null=True)
    apellido = models.TextField(blank=True, null=True)
    sexo_id = models.TextField(blank=True, null=True)
    edad = models.IntegerField(blank=True, null=True)
    cliente_id = models.IntegerField(blank=True, null=True)
    categoria = models.TextField(blank=True, null=True)
    sucursal = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'empleados'


class Movimientos(models.Model):
    id = models.IntegerField(primary_key=True)
    cliente_id = models.IntegerField(blank=True, null=True)
    fecha = models.TextField(blank=True, null=True)
    importe = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movimientos'


class Sucursales(models.Model):
    id = models.IntegerField(primary_key=True)
    calle = models.TextField(blank=True, null=True)
    altura = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sucursales'


        

class ids(models.Model):
    id = models.IntegerField(primary_key=True)
    cliente_id = models.IntegerField(blank=True, null=False)
    username = models.TextField(blank=True, null=False)
    class Meta:            
        db_table = 'ids'



class Prestamos(models.Model):
    id = models.IntegerField(primary_key=True)
    cliente_id = models.TextField(blank=True, null=True)
    monto = models.TextField(blank=True, null=True)
    fecha_inicio = models.TextField(blank=True, null=True)
    tipo = models.TextField(blank=True, null=True)

    class Meta:
        
        db_table = 'prestamos'