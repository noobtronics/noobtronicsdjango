import os, django, sys
from pathlib import Path
sys.path.append(str(Path(os.getcwd()).parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

import csv
from products.models import ZipCodes


def save_zip(zipcode, district, state):
    try:
        z = ZipCodes(zipcode=zipcode, district=district, state=state)
        z.save()
    except:
        pass

def init_zipcode():
    data = {}
    with open('zipcode_csv.csv', 'r') as fil:
        csv_reader = csv.DictReader(fil)
        for row in csv_reader:
            status = row['Deliverystatus']
            zipcode = row['pincode']
            district = row['Districtname']
            state = row['statename']

            if status == 'Delivery':
                if zipcode not in data:
                    data[zipcode] = [district, state]


        for row in csv_reader:
            status = row['Deliverystatus']
            zipcode = row['pincode']
            district = row['Districtname']
            state = row['statename']

            if status != 'Delivery':
                if zipcode not in data:
                    data[zipcode] = [district, state]

        count = 0
        l = len(data)
        for zipcode in data:
            count+=1
            district, state = data[zipcode]
            save_zip(zipcode, district, state)
            if count % 1000 == 0:
                print(count)
        print('All zipcode initialized.')

init_zipcode()