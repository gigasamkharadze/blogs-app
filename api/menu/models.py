from django.db import models


class Menu(models.Model):
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Menu'
        verbose_name_plural = 'Menu Items'

    def __str__(self):
        return self.title