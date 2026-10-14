import json
from django.test import TestCase, Client
from .models import Tarea


class ApiTests(TestCase):
    def setUp(self):
        self.tarea = Tarea.objects.create(titulo='Ensayo', curso='Historia', fechaEntrega='2026-11-01')
        Tarea.objects.create(titulo='Lectura', curso='Literatura', fechaEntrega='2026-11-02', estado='completada')
        self.url = f'/api/tarea/{self.tarea.pk}'

    def test_lista_y_campos(self):
        r = self.client.get('/api/tarea/')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 2)
        self.assertEqual(set(r.json()[0]), {'id', 'titulo', 'curso', 'fechaEntrega', 'estado'})

    def test_detalle_y_no_encontrada(self):
        self.assertEqual(self.client.get(self.url).json()['titulo'], 'Ensayo')
        self.assertEqual(self.client.get('/api/tarea/9999').status_code, 404)

    def test_filtros(self):
        for estado in ['pendiente', 'completada']:
            r = self.client.get('/api/tarea/', {'estado': estado})
            self.assertEqual(len(r.json()), 1)
            self.assertEqual(r.json()[0]['estado'], estado)
        for query in ['estado=otro', 'estado=', 'estadopendiente', 'estado=pendiente&estado=completada']:
            self.assertEqual(self.client.get('/api/tarea/?'+query).status_code, 400)

    def test_completar_persistente_e_idempotente(self):
        for _ in range(2):
            r = self.client.patch(self.url, json.dumps({'estado': 'completada'}), content_type='application/json')
            self.assertEqual(r.status_code, 200)
        self.tarea.refresh_from_db()
        self.assertEqual(self.tarea.estado, 'completada')
        self.assertEqual(self.client.get('/api/tarea/?estado=pendiente').json(), [])

    def test_patch_invalido_no_modifica(self):
        for body in ['{', 'null', '[]', '{}', '{"estado":"pendiente"}', '{"estado":"completada","titulo":"Otro"}']:
            self.assertEqual(self.client.patch(self.url, body, content_type='application/json').status_code, 400)
        self.assertEqual(self.client.patch(self.url, 'x', content_type='text/plain').status_code, 415)
        self.tarea.refresh_from_db()
        self.assertEqual(self.tarea.estado, 'pendiente')

    def test_metodos_restringidos(self):
        self.assertEqual(self.client.post('/api/tarea/').status_code, 405)
        self.assertEqual(self.client.delete(self.url).status_code, 405)
        self.assertEqual(self.client.put(self.url).status_code, 405)

    def test_csrf_dashboard(self):
        cliente = Client(enforce_csrf_checks=True)
        body = json.dumps({'estado': 'completada'})
        self.assertEqual(cliente.patch(self.url, body, content_type='application/json').status_code, 403)
        self.assertEqual(cliente.get('/').status_code, 200)
        token = cliente.cookies['csrftoken'].value
        self.assertEqual(cliente.patch(self.url, body, content_type='application/json', HTTP_X_CSRFTOKEN=token).status_code, 200)
