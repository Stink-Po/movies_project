import json

from django.core.management.base import BaseCommand
from movies_app.models import Movie, Actor, Director
from boxoffice_api import BoxOffice
import os
from datetime import datetime, date


class Command(BaseCommand):
    help = "run daily task"
    filename = os.path.join("static", "boxoffice.json")

    def handle(self, *args, **options):
        # getting information from box office mojo
        box_office = BoxOffice(api_key="4764dba0")
        result = box_office.get_weekend(year=int(datetime.utcnow().year), week=int(datetime.now().strftime("%U")) - 2)
        print(result[0])
        # write information into a json file to use in view
        with open(self.filename, 'w') as json_file:
            json.dump(result, json_file)
        # looping into the results and if there is a new movie or director or actor adding it to database
        for movie in result:
            actors = movie['Actors'].split(",")
            for actor in actors:
                if Actor.objects.filter(name=actor.lstrip()).first():
                    continue
                else:
                    new_actor = Actor(name=actor.lstrip())
                    new_actor.save()

            directors = movie['Director'].split(",")
            for director in directors:
                if Director.objects.filter(name=director.lstrip()).first():
                    continue
                else:
                    new_director = Director(name=director.lstrip())
                    new_director.save()

            if Movie.objects.filter(title=movie['title']).first():
                continue
            else:
                new_movie = Movie(
                    title=movie['title'],
                    image=movie['Poster'],
                    description=movie['description'],
                    release_year=movie["Released"].split(" ")[-1],
                    release_date=datetime.strptime(movie['Released'], "%d %b %Y").date(),
                )
                new_movie.save()
                for gener in movie['Genre'].split(","):
                    new_movie.genres.add(gener.lstrip())

                for actor in movie['Actors'].split(","):
                    act = Actor.objects.filter(name=actor.lstrip()).first()
                    new_movie.actors.add(act)

                for director in movie['Director'].split(","):
                    dire = Director.objects.filter(name=director).first()
                    new_movie.director.add(dire)

        print("test")
        self.stdout.write("Daily task done")


