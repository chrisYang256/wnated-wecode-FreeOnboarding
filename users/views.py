import json
import re
import bcrypt
import jwt

from django.http  import JsonResponse
from django.views import View

from my_settings import SECRET_KEY, ALGORITHMS
from users.models import User

class SignUp(View):
    def post(self, request):
        data              = json.loads(request.body)
        REGX_EMAIL        = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        REGX_PASSWORD     = '^(?=.*\d)(?=.*[a-zA-Z])[0-9a-zA-Z!@#$%^&*]{8,20}$'

        try:
            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'message': 'EXIST_EMAIL'}, status=400)

            if not re.match(REGX_EMAIL, data['email']):
                return JsonResponse({'message': 'INVALID_EMAIL_FORM'}, status=400)

            if not re.match(REGX_PASSWORD, data['password']):
                return JsonResponse({'message': 'INVALID_PASSWORD_FORM'}, status=400)

            password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            User.objects.create(
                name     = data['name'],
                email    = data['email'],
                password = password,
            )

            return JsonResponse({'message': 'SUCCESS'}, status=201)
        
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

class SignIn(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = User.objects.get(email = data['email'])

            if not (user and bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8'))):
                return JsonResponse({"message" : "INVALID_USER"}, status=401)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)

        access_token = jwt.encode({'user_id' : user.id}, SECRET_KEY, ALGORITHMS)

        return JsonResponse({'access_token' : access_token}, status=201)
