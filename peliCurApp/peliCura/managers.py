from django.db import models
from datetime import timedelta

# Manager para Persona
class PersonaManager(models.Manager):
    
    ''' Crear persona (con foto)
    def crear_persona(self, name, last_name, art_name, country, picture, born, bio):
        self.create(nombre = name, apellido = last_name, nombre_artistico = art_name, 
                    nacionalidad = country, foto = picture, nacimiento = born, 
                    biografia = bio)
    '''
    # Crear persona (sin foto)
    def crear_persona(self, name, last_name, art_name, country, born, bio):
        self.create(nombre = name, apellido = last_name, nombre_artistico = art_name, 
                    nacionalidad = country, nacimiento = born, 
                    biografia = bio)
        # asignación --> Persona.manager.crear_persona("Apolinario", "Rodriguex Mirtó", "Luménico", "Serbia",
        #                                              "1985", "De la guerra balcana surgido")
        # recuperar Persona.manager.values()[indiceQuerySet]['elementoDiccionario']



# Manager para Comentario
class ComentarioManager(models.Manager):
   
    # Crear comentario
    def crear_comentario(self, peli_mentario, descri_mentario, rating):
        comentario = self.create(pelicula = peli_mentario, 
                                 descripcion = descri_mentario, 
                                 valoracion = rating)
        
        return comentario

    # Auditar comentario
    def auditar_comentario(self, state):
        estado = state
        


# Manager para Genero
class GeneroManager(models.Manager):
    
    # Crear género
    def crear_genero(self, nombre_genero, descripcion_genero):
        self.create(nombre = nombre_genero, descripcion = descripcion_genero)



# Manager para Pelicula
class PeliculaManager(models.Manager):
    
    # Crear duración
    def crear_duracion(self, minutos):
        return timedelta(minutes=minutos)

    # Crear película
    # pelicula = Pelicula.manager.crear_pelicula("El año de la bestia equilátera", 
    #                                            "Periplo de un hombre solo en el Valle de la Muerte",
    #                                             1987, 78, [genero, genero_uno], personaX,
    #                                             personaX)
    def crear_pelicula(self, title, abstract, year, minutes, genre, directed_by, acted_by):
        pelicula = self.create(titulo = title,
                              resumen = abstract, 
                              anio_realizacion = year, 
                              duracion = self.crear_duracion(minutes), 
                              puntuacion = 0)
        # agregar género
        pelicula.genero.add(genre) # agregar género a película (a través del int(id))
        # agregar director
        # ACEPTA PERSONA
        pelicula.director.add(directed_by)
        # agregar actor
        pelicula.actor.add(acted_by)
        # ACEPTA DICCIONARIO
        '''for a in acted_by:
            id = int(a.id) 
            pelicula.actor.add(id)
        '''

    