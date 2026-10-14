import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Tarea


def error(mensaje, status):
    return JsonResponse({'error': mensaje}, status=status)


def no_permitido(metodos):
    response = error('Método no permitido.', 405)
    response['Allow'] = metodos
    return response


@ensure_csrf_cookie
def dashboard(request):
    if request.method != 'GET':
        return no_permitido('GET')
    return render(request, 'tareas/dashboard.html')


def listar(request):
    if request.method != 'GET':
        return no_permitido('GET')
    if set(request.GET) - {'estado'}:
        return error('Parámetro desconocido. Usa ?estado=pendiente o ?estado=completada.', 400)
    tareas = Tarea.objects.all()
    if 'estado' in request.GET:
        estados = request.GET.getlist('estado')
        if len(estados) != 1 or estados[0] not in ('pendiente', 'completada'):
            return error('Estado inválido. Usa pendiente o completada.', 400)
        tareas = tareas.filter(estado=estados[0])
    return JsonResponse([t.to_dict() for t in tareas], safe=False)


def detalle(request, id):
    if request.method not in ('GET', 'PATCH'):
        return no_permitido('GET, PATCH')
    try:
        tarea = Tarea.objects.get(pk=id)
    except Tarea.DoesNotExist:
        return error('Tarea no encontrada.', 404)
    if request.method == 'PATCH':
        if request.content_type != 'application/json':
            return error('Usa Content-Type: application/json.', 415)
        try:
            datos = json.loads(request.body)
        except (ValueError, UnicodeDecodeError):
            return error('JSON inválido.', 400)
        if datos != {'estado': 'completada'}:
            return error('El cuerpo debe ser exactamente {"estado": "completada"}.', 400)
        tarea.estado = 'completada'
        tarea.save(update_fields=['estado'])
    return JsonResponse(tarea.to_dict())
