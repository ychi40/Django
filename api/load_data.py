import sys, os
import pandas as pd
import django
#You will need to set directory for your Django in order to connect to SQL lite directly
#Set Directory
project_dir = "C:/Users/Niche/Desktop/eb-virt/hextech"
#Append system path
sys.path.append(project_dir)
#Set up Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'hextech.hextech.settings'
django.setup()
#from hextech..t
#settings.configure(settings)
#settings.configure(settings)


#setup_environ(settings)

# The step above is similar to using shell but a little more complicate

#Import your Data
from api.models import Safeplace

# Read data using pandas
data = pd.read_csv('vicsafeplaces.csv', sep = ',')
for row in range(0, len(data)):
    # Import data for each variables, please make sure data fit the types
    x = data['Establishment'][row]
    y = data['Address'][row]
    z = data['Suburb'][row]
    a = data['Postcode'][row]
    b = data['State'][row]
    c = data['Establishment Type'][row]
    la = data['latitude'][row]
    lo = data['longtitude'][row]
    # Save to database
    api = Safeplace()
    api.establishment = x
    api.address = y
    api.suburb = z
    api.postcode = a
    api.state = b
    api.type = c
    api.latitude = la
    api.longitude = lo
    #Don't forget to save all
    api.save()