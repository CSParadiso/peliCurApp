from datetime import *
from peliCura.models import *

# si no hay personas, Crear Personas
if Persona.manager.all().count() == 0:
  Persona.manager.crear_persona("Silvio", "Iparaguirre", "Coqui", "Argentina",
                               1900, "Varón del tango arrabalero")

  Persona.manager.crear_persona("Julia", "Mariani", "Coca", "Brasil", 1998,
                              "Fundamentalista del cinismo radial periodístico")

persona_uno = Persona.manager.all().get(id=1)
persona_dos = Persona.manager.all().get(id=2)

# Si no hay géneros, Crear Géneros
if Genero.manager.all().count() == 0:
  Genero.manager.crear_genero("Comedia", "Animación picaresca del alma sonriente")
  Genero.manager.crear_genero("Terror", "Susto del ocaso")

genero_uno = Genero.manager.all().get(id=1)
genero_dos = Genero.manager.all().get(id=2)

# Si no hay películas, crear Películas
if Pelicula.manager.all().count() == 0:
  Pelicula.manager.crear_pelicula("El meridiano solar", "Un hombre en busca de la luz", 
                                2005, 132, genero_dos, persona_dos, persona_uno)
  Pelicula.manager.crear_pelicula("Sixty suns", "Florida mide nazismo en encuesta", 
                                2008, 103, genero_uno, persona_uno, persona_uno)

pelicula_dos = Pelicula.manager.all().get(id=1)
pelicula_uno = Pelicula.manager.all().get(id=2)

if Comentario.manager.all().count() == 0:
  Comentario.manager.crear_comentario(pelicula_uno, "Una bazofia atómica", 2.1)
  Comentario.manager.crear_comentario(pelicula_uno, "Horrible, simple", 3)

comentario_uno = Comentario.manager.all().get(id=1)
comentario_udos = Comentario.manager.all().get(id=2)


input("Continue, por favor")
