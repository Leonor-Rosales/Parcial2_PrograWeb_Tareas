from django.db import models


class Tarea(models.Model):
    titulo = models.CharField(max_length=200)
    curso = models.CharField(max_length=100)
    fechaEntrega = models.DateField()
    estado = models.CharField(max_length=10, default='pendiente', choices=[
        ('pendiente', 'Pendiente'), ('completada', 'Completada'),
    ])

    class Meta:
        ordering = ['fechaEntrega', 'id']
        constraints = [models.CheckConstraint(
            condition=models.Q(estado__in=['pendiente', 'completada']),
            name='tarea_estado_valido',
        )]

    def to_dict(self):
        return {'id': self.pk, 'titulo': self.titulo, 'curso': self.curso,
                'fechaEntrega': self.fechaEntrega.isoformat(), 'estado': self.estado}
