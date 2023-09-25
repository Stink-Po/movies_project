from datetime import datetime, date
from django.shortcuts import render
from .models import Movie
from boxoffice_api import BoxOffice
import os
import json


def index(request):
    filename = os.path.join("static", "boxoffice.json")
    with open(filename, "r") as file:
        box_office_data = json.load(file)

    current_user = request.user
    return render(request, 'movies_app/index.html', context={
        "user": current_user,
        "box_office_data": box_office_data,
    })
