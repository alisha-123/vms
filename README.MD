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


python manage.py drf_create_token <username>





DIVIDE BY ZERO CHECK
HISTORICAL DATA 
UNIT TEST CHECK