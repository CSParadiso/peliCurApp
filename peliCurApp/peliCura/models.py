from django.db import models
from peliCura.managers import *
from django.core.exceptions import *
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse, reverse_lazy
from datetime import datetime, timedelta
from django_countries.fields import CountryField



# Create your models here.

# Existen argumentos disponibles para todos los tipos de campos. Todos opcionales:
# 
# Field.null: null = false --> Default. El campo no acepta nulos. 
# Evitar en campos de tipo CharField y TextField. 
# Referido a la BBDD.
# 
# Field.blank: blank = false --> Default. El campo acepta blancos.
# Referido a la validación.
#
# Field.choices: choices es una secuencia de iterables con exactamente dos ítems para usar como
# opciones para una campo [(A, B)].  
# <select name="" id="">
#   <option value="">CADA UNA DE LAS OPCIONES</option>
# </select> 
# El primer elemento en cada tupla (A, B) es el valor actual en el modelo y el segundo es el 
# nombre que es leíble por el hombre.
# Generalmente, es mejor definir las opciones dentro de un modelo de clase y definir una
# constante de nombre adecuado para cada valor:
# class Developer(models.Model):
#   SENIOR = "SR"
#   MID_LEVEL = "ML"
#   JUNIOR = "JR"  
#   CATEGORIA_DEVELOPER_CHOICES = [
#       (SENIOR, "Senior"),
#       (MID_LEVEL, "Mid-Level"),
#       (JUNIOR, "Junior"),
#   ]
#   nombre = models.Charfield(max_length = 60)
#   categoria = models.CharField(
#     max_length = 2,
#     choices = CATEGORIA_DEVELOPER_CHOICES, 
#     default = JUNIOR
#   )
#   Para cada campo que tiene choices, el objeto tendrá un método:
#   objeto.get_nombre_campo_display() que retorna el valor leíble por el humano del campo:
#   developer = Developer(nombre="" categoria="MID_LEVEL")
#   developer.categoria --> ML
#   developer.get_categoria_display() --> Mid-Level
#   
#   Field.db_column: db_column = nombreCampo --> default.
# 
#   Field.db_comment: útil para documentar campos
# 
#   Field.db_index: db_index = True --> default (EVITAR USAR, usar en su lugar Meta.indexes).
#   Crea índices de BBDD para este campo
# 
#   Field.default: se usa cuando se crea una nueva instancia del modelo sin completar el valor del campo
# 
#   Field.editable: editable = True --> default. Si es falso, el campo no se muestra en formularios 
#   o al admin.
#
#   Field.error_messages: error_messages = mensaje_por_defecto_campo. Este argumento permite
#   sobreescribir el mensaje por defecto del campo. La mayoría de los formualarios no muestran 
#   estos errores.
#   Es necesario que pasemos un diccionario con claves que coincidan con los mensajes de error que 
#   querramos sobreescribir. Algunas llaves son: null, blank, invalid, invalid_choice, unique, 
#   unique_for_date, etc. 
# 
#   Field.help_text: es un texto de ayuda para mostrarse en el formulario. Sirve como documentación.
# 
#   Field.primary_key: si el valor es True, establece el campo como clave primaria del modelo.
#   Esto implica que null=False y unique=True. Si no se especifíca una clave primaria, Django
#   crea un campo de clave primaria por defecto, el cual se puede cambiar en la aplicación en 
#   AppConfig.default_auto_field y globalmente en la setting DEFAULT_AUTO_FIELD. 
#   
#   Field.unique: si el valor es verdadero, debe ser único a través de la tabla.
#   Un django.db.IntegrityError será lanzado por el método save() si se intenta
#   guardar un modelo con un valor duplicado en un campo unique.
#   No se puede usar en ManyToManyField o en OneToOneField
# 
#   Field.unique_for_date     Por ejemplo, si se tiene un campo titulo que tiene
#   Field.unique_for_month    un unique_for_date="fecha_publicacion", entonces Django no permitirá
#   Field.unique_for_year     dos registros con el mismo título y fecha_publicación.
#                             fecha_publicacion = DateField() o DateTiemField()
#   
#   Field.verbose_name: un nombre verbal leíble por el humano. Si el verbose_name no es provisto, Django
#   crea uno usando el nombre de atributo del campo, convirtiendo guiones bajos a espacios.
#   primer_nombre = models.CharField("primer nombre persona", max_length=30) --> "primer nombre persona"
#   primer_nombre = models.CharField(max_length=30) --> "primer nombre"
# 
#   Field.validators: una lista de validadores para ejecutar con este campo.
#   def validator_par(valor):
#     if valor % 2 != 0:
#       raise validationError(
#         _("%(value)s no es un número par"),
#         params = {"value": value},
#       ) 
#   campo_par = models.IntegerField(validators=[validator_par])
#   

class Persona(models.Model):
    manager = PersonaManager()
    nombre = models.CharField("Nombre", max_length=70) # <input type="text"> en HTML
    apellido = models.CharField("Apellido", max_length=70) 
    nombre_artistico = models.CharField("Nombre artístico", max_length=70, null=True, blank=True)
    nacionalidad = CountryField("Nacionalidad", max_length=70)
    foto = models.ImageField("Foto", upload_to='fotos_personas', null=True) # form widget es ClearableFileInput
                               # Hereda todo de FileField. <input type="file" ...> en HTML
    fecha_nacimiento = models.DateField("Fecha de nacimiento") # Solo el año
    biografia = models.TextField("Biografía", max_length=300)
    
    # Definir para usar formularios de CreateView
    def get_absolute_url(self):
        return reverse("detalle-pelicula-id", kwargs={'pk':self.pk})
    
    # Redefinimos el método __str__
    def __str__(self) -> str:
        if self.nombre_artistico:
            return f"{self.nombre} '{self.nombre_artistico}' {self.apellido}"  
        else:
          return f"{self.nombre} {self.apellido}" 




class Genero(models.Model):
    manager = GeneroManager()
    nombre = models.CharField("Nombre Género", max_length=20, unique=True)
    # Definir para usar formularios de CreateView
    def get_absolute_url(self):
        return reverse("detalle-pelicula-id", kwargs={'pk':self.pk})

    # Redefinimos el método __str__
    def __str__(self) -> str:
      return self.nombre  


class Pelicula(models.Model):
    # recuperar --> peliculax = Pelicula.manager.get(id=x)
    manager = PeliculaManager()
    titulo = models.CharField("Titulo", max_length=100) # <input type="text"> en HTML
    sinopsis = models.TextField("Sinospis", max_length=500) # <textarea> en HTML
    anio_realizacion = models.DateField("Año estreno") # solo el año
    duracion = models.IntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(1240) # 1240 minutos = 24 hs de duración
    ]) # timedelta(days, seconds, miliseconds) en Python
    # asignación --> duracion = timedelta(minutes=X)
    # horas = pelicula.duracion.seconds // 60
    # minutos_restantes = pelicula.duracion.seconds / 60 % 60
    genero = models.ManyToManyField(Genero) # Relación muchos a muchos con Género
    # asignación --> pelicula.genero.add(genero.id)
    # consulta --> pelicula.genero.values('nombre') = <QuerySet [{'nombre': 'Comedia'}]>
    # consulta --> pelicula.genero.values()[0]['nombre'] = 'Comedia'
    director = models.ManyToManyField(Persona, related_name="director") # Relación muchos a muchos con Persona
    # asignación --> pelicula.director.add(persona.id)
    actor = models.ManyToManyField(Persona, related_name="actor") # Relación muchos a muchos con Persona
    # asignación --> pelicula.actor.add(persona.id)
    # retrieve --> pelicula.actor.all() = <QuerySet [<Persona: Persona object (1)>, <Persona: Persona object (2)>]>
    # retrieve --> pelicula.actor.values_list('nombre_artistico') = <QuerySet ['Lillard', 'Quique']>
    # retrieve --> pelicula.actor.values('nombre_artistico')[0]['nombre_artistico'] = 'Lillard'
    # retrieve all --> for i in range(pelicula.actor.all().count()):
    #                       print(pelicula.actor.values('nombre_artistico')[i]['nombre_artistico'], end=" ")
    #                       = Lillaed Quique
    # retrieve all --> list(pelicula.actor.values_list('nombre_artistico', flat=True)) = ['Lillard', 'Quique']
    puntuacion = models.FloatField("Puntuacion", default=0) # <input type="number"> y Float
    poster = models.ImageField("Póster", upload_to='posters_peliculas', null=True)

    @property
    # Calcular puntuacion para que se vea y podamos usarlo en el template
    def calcular_puntuacion(self):
        nro_comentarios = self.comentario_set.count()
        puntuacion = 0
        # Obtener la lista de las valoraciones de la película
        puntuaciones = list(self.comentario_set.values_list('valoracion')) # retorna tupla
        for i in puntuaciones:
            puntuacion += i[0]
        # Si no hay comentarios, no dividimos por cero
        if nro_comentarios == 0:
            self.puntuacion = 0.0
        else:
            self.puntuacion = (puntuacion / nro_comentarios)
        return self.puntuacion 

    # Actualizar puntuación película
    def agregar_puntuacion(self, valoracion):
        # calcular cantidad puntuaciones
        nro_comentarios = self.comentario_set.count() + 1 # agregamos el actual
        # asignar nueva puntuación
        self.puntuacion = (self.calcular_puntuacion + valoracion) / nro_comentarios
        self.save()
        return self.puntuacion
    
    # Definir para usar formularios de CreateView
    def get_absolute_url(self):
        return reverse("detalle-pelicula-id", kwargs={'pk':self.pk})
    
    # Redefinimos el método __str__
    def __str__(self) -> str:
      return self.titulo  
    
    


class Comentario(models.Model):
    ESCRITO = "E"
    ACEPTADO = "A"
    CENSURADO = "C"
    ESTADO_COMENTARIO_CHOICES = [
        (ESCRITO, "escrito"),
        (ACEPTADO, "publicado"),
        (CENSURADO, "censurado"), 
    ]
    estado = models.CharField("Estado", 
        max_length = 1,
        choices = ESTADO_COMENTARIO_CHOICES,
        default = ESCRITO,
    )
    manager = ComentarioManager()
    fecha = models.DateTimeField("Fecha", 
                                  default=datetime.now)  # Fecha de creado el objeto datetime
    # recuperar --> comentario.fecha = datetime.datetime(2023, 5, 20, 22, 55, 4, 393404, tzinfo=datetime.timezone.utc)
    # recupera en string --> comentario.fecha.strftime('%Y-%m') = '2023-05'
    descripcion = models.TextField("Comentario", max_length=100)
    valoracion = models.FloatField("Puntaje",                           # <input type="number"> y Float
                                   validators = [MinValueValidator(1),  # DEBE SER ENTRE 1
                                                 MaxValueValidator(5)]) #  y 5  
    pelicula = models.ForeignKey("Pelicula", on_delete=models.CASCADE) 
    # asignación --> comentario = Comentario.objects.create(descripcion="", pelicula=nombreObjectoPelicula)
    # recuperar todos los comentarios:
    # comentarios = [comentario['descripcion'] for comentario in pelicula.comentario_set.values('descripcion')]
    nombre = models.CharField("Nombre usuario", max_length=100)
    email = models.EmailField("Correo electrónico")

     # Auditar comentario cuando administrador audite los comentarios
    def auditar_comentario(self, state):
        if state in dict(self.ESTADO_COMENTARIO_CHOICES):
            self.estado = state   
            self.save()     
        else:
            raise ValidationError('Estado Inválido')
        return state

    # Sobreescribir save() de Comentario para que actualice puntuacion de la película solo la primera vez
    def save(self, *args, **kwargs):
        # Performamos nuestra intervención
        if not self.pk:
            # Solo actualizar si es un nuevo comentario (aún sin primary key)
            self.pelicula.agregar_puntuacion(self.valoracion)
        # Guardamos para que ya exista
        super().save(*args, **kwargs)

        
        

    # Definir para usar formularios de CreateView
    def get_absolute_url(self):
        return reverse("detalle-pelicula-id", kwargs={'pk':self.pelicula.pk})

    # Redefinimos el método __str__
    def __str__(self) -> str:
      return self.descripcion


