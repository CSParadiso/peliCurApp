from django import template

register = template.Library()

# @register.filter
# def filtrar_estado(comentario, estado):
#     return comentario.filter(estado = estado)

# @register.filter
# def humanizar_timedelta(timedelta):
#     horas = timedelta.seconds // 3600
#     minutos = (timedelta.seconds // 60) % 60
#     return f"{horas:02}h{minutos:02}m"