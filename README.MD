# To set up and create new token use below script:

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# Create a new user
user = User.objects.create_user(username='alisha', email='alishachopra1903@gmail.com', password='password')

# Optionally, set additional attributes
user.first_name = 'Alisha'
user.last_name = 'Chopra'
user.save()
token, created = Token.objects.get_or_create(user=user)
print(token.key)

# Create new token, Use this token like Token c1fe893aa977e9d20632da911ae48ba56e835927 to access all api's
python manage.py drf_create_token <username>


# Create virtualenv like python 
python3 -m virtualenv venv 

# Activate venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
