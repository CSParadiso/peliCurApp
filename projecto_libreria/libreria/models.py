from django.db import models
import random
from datetime import date, timedelta 

# Create your models here.

class AutorManager(models.Manager):
  def crear_nacionalidad(self):
    numero = random.randint(1, 3)
    return ("Argentina" if numero == 2 else ("Chile" if numero == 1 else "Uruguay"))
  
  def crear_fecha(self, ene):
    return date.today() + timedelta(days=ene)
    
  def crear_autor(self, cantidad):
    autores = []
    for i in range(cantidad):
      autores.append(self.create(nombre="Autor" + str(i), nacionalidad = self.crear_nacionalidad(), fecha_nacimiento = self.crear_fecha(i)))
    return autores
      
 
class Autor(models.Model):
  objects = AutorManager()
  nombre = models.CharField(max_length=100)
  nacionalidad = models.CharField(max_length=100)
  fecha_nacimiento = models.DateField(default='--')
    
class LibroManager(models.Manager):
  def crear_libros(self,cantidad):
    for i in range(cantidad):
      randa=random.randint(1,6)
      autor_rand=Autor.objects.all()[randa:randa+1].get()
      a=self.create(
        isbn=11112223+i,
        titulo="titulo"+str(i),
        editorial="editorial"+str(i),
        anio=1988+random.randint(1,6),
        tipo_libro=Libro.TIPO_LIBRO_CHOICES[random.randint(0, 3)]
        )
      a.autor.add(autor_rand)                   
                
  

class Libro(models.Model):
  objects=LibroManager()
  TIPO_LIBRO_CHOICES = [
    ("NOVELA", 'Novela'),
    ("TEATRO", 'Teatro'), 
    ("POESIA", 'Poesía'), 
    ("ENSAYO", 'Ensayo'),
  ]
  titulo = models.CharField(max_length= 100, default='--')
  tipo_libro = models.CharField(
    max_length = 20, 
    choices = TIPO_LIBRO_CHOICES,
    default = "POESIA",
  )  
  editorial = models.CharField(max_length=100, default='--')
  anio = models.IntegerField(default='--')
  isbn = models.IntegerField(default='--')
  # Se declara una relacion muchos a muchos con Autor, pero solo aquí porque está declarado arriba Autor
  autor = models.ManyToManyField(Autor)
  
class Copia(models.Model):
  TIPO_ESTADO_CHOICES = [
    ('PRESTADA', "Prestada"), 
    ("BIBLIOTECA", 'En biblioteca'), 
    ('RETRASO', 'Retraso'), 
    ('REPARACION', 'Repatración'),
  ]
  tipo_estado = models.CharField(
    max_length = 20,
    choices = TIPO_ESTADO_CHOICES,
    default = 'BIBLIOTECA',
  )
  
class Lector(models.Model):
  ESTADO_LECTOR_CHOICES = [
    ('HABILITADO', 'Habilitado'), 
    ('MULTADO', 'Multado'), 
    ]
  estado_lector = models.CharField(
    max_length = 20,
    choices = ESTADO_LECTOR_CHOICES,
    default = 'HABILITADO',
  )  
  
class Prestamo(models.Model):
  f_entrega = models.DateField
  f_devolucion = models.DateField
  multa = models.BooleanField
  
