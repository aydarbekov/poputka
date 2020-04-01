import csv, os, sys

# project_dir = "~/attractor/projects/poputka/source/main/"
#
# sys.path.append(project_dir)
#
# os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
#
# import django
#
# django.setup()

from webapp.models import Car, CarModel

data = csv.reader(open("/home/attractor/projects/poputka/csv.csv"), delimeter=';')

for row in data:
    car = CarModel()
    car.mark = row[0]
    car.model = row[1]
    car.save()
