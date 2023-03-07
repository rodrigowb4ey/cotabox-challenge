from django.db import models

class Participant(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    participation = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'
