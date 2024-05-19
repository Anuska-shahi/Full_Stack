from django.shortcuts import render,get_object_or_404
from .models import BlogPost
from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from account.models import CustomUser
import json,jwt,time,datetime,math
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from rest_framework.exceptions import AuthenticationFailed

# Create your views here.

class BlogListView:
    @csrf_exempt
    def blog_list(request:HttpRequest):
        token=TokenRegeneration.check_token(request)
        if token:
            if request.method=='GET':
                if 'all' in request.GET and request.GET['all'].lower() == 'true':
                    blogs=BlogPost.objects.filter(deleted=False)
                elif 'deleted' in request.GET and request.GET['deleted'].lower() == 'true':
                    refresh_token= request.COOKIES.get("refresh_token")
                    payload=jwt.decode(refresh_token,'secret',algorithms='HS256')
                    author_id = payload.get('id')
                    author = CustomUser.objects.get(id=author_id)
                    blogs = BlogPost.objects.filter(deleted=True, author=author)
                else:
                    refresh_token= request.COOKIES.get("refresh_token")
                    payload=jwt.decode(refresh_token,'secret',algorithms='HS256')
                    author_id = payload.get('id')
                    author = CustomUser.objects.get(id=author_id)
                    blogs = BlogPost.objects.filter(deleted=False, author=author)
                blog_data = [{
                    'id': blog.id,
                    'title': blog.title, 
                    'Content': blog.content,
                    'published_date':blog.published_date,
                    'author_email': blog.author.email
                    } for blog in blogs]
                return JsonResponse(blog_data, safe=False)
            elif request.method=='POST':
                data = json.loads(request.body)
                refresh_token= request.COOKIES.get("refresh_token")
                payload=jwt.decode(refresh_token,'secret',algorithms='HS256')
                auth_author_id = payload.get('id')
                author = get_object_or_404(CustomUser, id=auth_author_id)
                blog=BlogPost.objects.create(title=data['title'], content=data['content'], author=author)
                return JsonResponse({
                    'id': blog.id,
                    'title': blog.title, 
                    'Content': blog.content,
                    'published_date':blog.published_date,
                    'author_email': blog.author.email
                    } ,status=201)
            else:
                return JsonResponse({'error': 'Method Not Allowed'}, status=405)
        else:
                return JsonResponse({'error':'Not Authenticated'})
        
class BlogDetailView:
    @csrf_exempt
    def blog_detail(request:HttpRequest,pk):
        token=TokenRegeneration.check_token(request)
        print("token",token)
        if token:
            if request.method=='GET':
                blog=BlogPost.objects.get(pk=pk)
                blog_data={
                    'id': blog.id,
                    'title': blog.title, 
                    'Content': blog.content,
                    'published_date':blog.published_date,
                    'author_email': blog.author.email
                    }
                return JsonResponse(blog_data)
            elif request.method=='PATCH':
                data=json.loads(request.body)
                blog=BlogPost.objects.get(pk=pk)
                blog.title=data['title']
                blog.content=data['content']
                blog.save()
                return JsonResponse({
                    'id': blog.id,
                    'title': blog.title, 
                    'Content': blog.content,
                    'published_date':blog.published_date,
                    'author_email': blog.author.email
                    })
            elif request.method=='DELETE':
                blog = BlogPost.objects.get(pk=pk)
                blog.delete()
                return JsonResponse({'message': 'Blog soft deleted successfully'}, status=204)
            else:
                return JsonResponse({'error': 'Method Not Allowed'}, status=405)
        else:
                return JsonResponse({'error':'Not Authenticated'})
      
class BlogRestoreView:
    @csrf_exempt
    def blog_restore(request: HttpRequest, pk):
        token=TokenRegeneration.check_token(request)
        print(token)
        if token:
            if request.method=='POST':
                blog = BlogPost.objects.get(pk=pk)
                blog.restore()
                return JsonResponse({'message': 'Blog restored successfully'}, status=200)
            else:
                return JsonResponse({'error': 'Method Not Allowed'}, status=405)
        else:
                return JsonResponse({'error':'Not Authenticated'})


class BlogPostHardDeleteView:
    @csrf_exempt
    def blog_hard_delete(request: HttpRequest, pk):
        token=TokenRegeneration.check_token(request)
        print(token)
        if token:
            if request.method=='DELETE':
                blog = BlogPost.objects.get(pk=pk)
                blog.delete(hard_delete=True) 
                return JsonResponse({'message': 'Blog  hard deleted successfully'}, status=204)
        else:
                return JsonResponse({'error':'Not Authenticated'})

class TokenRegeneration:
    @csrf_exempt
    def check_token(request:HttpRequest):
        token= request.COOKIES.get("access_token")
        if token:
            try:
                payload=jwt.decode(token,"secret",algorithms="HS256")
                user_id=payload.get('id')
                user=CustomUser.objects.get(pk=user_id)   
                res={
                    'message': "token Authorization",
                    'data': {
                        'id':user.id,
                        'first_name':user.first_name,
                        'last_name':user.last_name,
                        'address':user.address,
                        'phone_no':user.phone_no,
                        'email':user.email
                    }
                } 
                return JsonResponse(res,status=200)
            except ExpiredSignatureError:
                response=TokenRegeneration.regen(request)
                return response
            except InvalidTokenError:
                return JsonResponse({
                    'message':'token invalid',
                }) 
    @csrf_exempt
    def regen(request:HttpRequest):
        access_token= request.COOKIES.get("access_token")
        refresh_token = request.COOKIES.get('refresh_token')
        now = datetime.datetime.now()
        dt_now =int(now.timestamp())
        if not access_token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            access_token_payload=jwt.decode(access_token,'secret',algorithms='HS256')
        except jwt.ExpiredSignatureError:
            refresh_token_payload = jwt.decode(refresh_token,'secret',algorithms='HS256')
            if dt_now < refresh_token_payload['exp']:
                access_payload={
                    'type':'access',
                    'id':refresh_token_payload.get('id'),
                    'email':refresh_token_payload.get('email'),
                    'exp': math.floor(time.time())+600,
                    'iat':math.floor(time.time())
                }
                new_access_token = jwt.encode(access_payload,'secret',algorithm ='HS256')
                refresh_payload={
                    'type':'refresh',
                    'id':refresh_token_payload.get('id'),
                    'email':refresh_token_payload.get('email'),
                    'exp': math.floor(time.time())+3600,
                    'iat':math.floor(time.time())
                }
                new_refresh_token = jwt.encode(refresh_payload,'secret',algorithm ='HS256')
                response = JsonResponse({'message':'token regenerate','access token':new_access_token,'refresh token':new_refresh_token},status=204,safe=False)
                response.set_cookie('access_token',new_access_token, httponly=True)
                response.set_cookie('refresh_token',new_refresh_token, httponly=True)
                return response
            else:
                raise AuthenticationFailed('Session Expired')