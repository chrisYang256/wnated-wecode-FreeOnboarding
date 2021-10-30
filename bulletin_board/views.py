import json
import time
import datetime

from django.http  import JsonResponse
from django.views import View

from users.utils  import login_decorator
from .models      import BulletinBoard
from users.models import User
    
class Post(View):
    def get(self, request):
        limit  = int(request.GET.get('limit', 5))
        offset = int(request.GET.get('offset', 0))

        limit  = limit + offset

        post_list = BulletinBoard.objects.all()[offset:limit]

        results = [
            {
            'author'     : post.author.name if post.author else "사라진 회원입니다.",
            'title'      : post.title,
            'created_at' : post.created_at
        } for post in post_list]

        return JsonResponse({'results' : results}, status=200)

    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)

            if not User.objects.filter(id=request.user.id):
                return JsonResponse({'message' : 'INVALID_USER'}, status=404)

            BulletinBoard.objects.create(
                    author_id   = request.user.id,
                    title       = data['title'],
                    description = data['description'],
                    created_at  = data['created_at']
            )

            time.sleep(1)

            return JsonResponse({'message' : 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

    @login_decorator
    def patch(self, request, post_id):
        try:
            data = json.loads(request.body)
            post = BulletinBoard.objects.get(id = post_id)

            if not post.author_id == request.user.id:
                return JsonResponse({'message' : 'INVALID_USER'}, status=404)

            post.title       = data['title']
            post.description = data['description']
            post.updated_at  = datetime.datetime.now()
            post.save()

            return JsonResponse({'message' : 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400) 

        except BulletinBoard.DoesNotExist:
                return JsonResponse({'message' : 'INVALID_POST'}, status=404)  

    @login_decorator
    def delete(self, request, post_id):
        try:
            post = BulletinBoard.objects.get(id = post_id)

            if not post.author_id == request.user.id:
                return JsonResponse({'message' : 'INVALID_USER'}, status=404)

            BulletinBoard.objects.get(id=post_id).delete()

            return JsonResponse({'message' : 'SUCCESS'}, status=200)

        except BulletinBoard.DoesNotExist:
                return JsonResponse({'message' : 'INVALID_POST'}, status=404)
            
class PostDetail(View):
    def get(self, request, post_id):
        try:
            post = BulletinBoard.objects.get(id=post_id)

            results = {
                'author'      : post.author.name if post.author else "사라진 회원입니다.",
                'title'       : post.title,
                'description' : post.description,
                'created_at'  : post.created_at,
                'updated_at'  : post.updated_at
            }

            return JsonResponse({'results' : results}, status=200)

        except BulletinBoard.DoesNotExist:
                return JsonResponse({'message' : 'INVALID_POST'}, status=404)
