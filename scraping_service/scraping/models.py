from django.db import models

from scraping.utils import from_cyrillic_to_eng


# Create your models here.

def default_urls():
    return {'work_ua': '', 'rabota_ua': '', 'dou_ua': '', 'djinni_co': ''}


class City(models.Model):
    name = models.CharField(max_length=50, verbose_name='City name', unique=True)
    slug = models.CharField(max_length=50, blank=True, unique=True)

    class Meta:
        verbose_name = 'City name'
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))
        super().save(*args, **kwargs)


class Language(models.Model):
    name = models.CharField(max_length=50, verbose_name='Language', unique=True)
    slug = models.CharField(max_length=50, blank=True, unique=True)

    class Meta:
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))
        super().save(*args, **kwargs)


class Vacancy(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=250, verbose_name='Vacancy title')
    company = models.CharField(max_length=250, verbose_name='Company')
    description = models.TextField(verbose_name='Description vacancy')
    city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='City', related_name='vacancies')
    language = models.ForeignKey('Language', on_delete=models.CASCADE, verbose_name='Language')
    timestamp = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Vacancy'
        verbose_name_plural = 'Vacancies'
        ordering = ['-timestamp']

    def __str__(self):
        return self.title


class Errors(models.Model):
    timestamp = models.DateField(auto_now_add=True)
    data_errors = models.JSONField()

    def __str__(self):
        return str(self.timestamp)


class Url(models.Model):
    city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='City')
    language = models.ForeignKey('Language', on_delete=models.CASCADE, verbose_name='Language')
    url_data = models.JSONField(default=default_urls)

    class Meta:
        unique_together = ('city', 'language')
