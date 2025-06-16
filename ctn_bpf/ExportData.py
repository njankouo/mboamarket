import csv
from .models import Personnel

with open('personnel.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['nom', 'mail'])

    for personnel in Personnel.objects.all():
        writer.writerow([personnel.nom, personnel.mail])