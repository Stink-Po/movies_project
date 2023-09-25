from django.db import models
from django.utils.text import slugify
from taggit.managers import TaggableManager
from datetime import datetime as dt


class Actor(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Director(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class MovieManager(models.Manager):
    def get_queryset(self):
        past_year = str(dt.utcnow().year - 1)
        results = super().get_queryset().filter(release_year=past_year).order_by('-release_date')
        return results


class Movie(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date="release_date")
    image = models.URLField()
    genres = TaggableManager()
    description = models.TextField()
    release_year = models.PositiveIntegerField()
    release_date = models.DateField(auto_now=True)
    actors = models.ManyToManyField(Actor, related_name="movies_app")
    director = models.ManyToManyField(Director, related_name="movies_app")

    objects = models.Manager()
    year = MovieManager()

    class Meta:
        ordering = ["-release_date"]

        indexes = [
            models.Index(
                fields=[
                    "-release_date"
                ]
            ),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
