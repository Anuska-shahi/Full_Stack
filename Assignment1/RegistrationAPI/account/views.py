from django.shortcuts import render

from rest_framework.response import Response

from .models import CustomUser
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpRequest
from rest_framework.exceptions import AuthenticationFailed
from django.views import View
import json,jwt,math,time,datetime
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

class CustomUserListView:
    @csrf_exempt
    def user_list(request: HttpRequest):
        if request.method=='GET':
            if 'deleted' in request.GET and request.GET['deleted'].lower() == 'true':
                users = CustomUser.objects.filter(deleted=True)
            else:
                # users = CustomUser.objects.all()
                users = CustomUser.objects.filter(deleted=False)
            user_data = [{'id': user.id,'email': user.email, 'first_name':user.first_name, 'last_name':user.last_name, 'phone_no':user.phone_no, 'address':user.address, 'deleted':user.deleted} for user in users]
            return JsonResponse(user_data, safe=False)
        elif request.method=='POST':
            data = json.loads(request.body)
            user = CustomUser.objects.create_user(email=data['email'],first_name=data['first_name'], last_name=data['last_name'],phone_no=data['phone_no'], password=data['password'],address=data['address'])
            return JsonResponse({'id': user.id,'email': user.email, 'first_name':user.first_name, 'last_name':user.last_name, 'phone_no':user.phone_no, 'address':user.address}, status=201)
        else:
            return JsonResponse({'error': 'Method Not Allowed'}, status=405)
    
class CustomUserDetailView:
    @csrf_exempt
    def user_detail(request: HttpRequest, pk):
        if request.method=='GET':
            user = CustomUser.objects.get(pk=pk)
            user_data = {'id': user.id,'email': user.email, 'first_name':user.first_name, 'last_name':user.last_name, 'phone_no':user.phone_no, 'address':user.address}
            return JsonResponse(user_data)

        elif request.method=='PATCH':
            data = json.loads(request.body)
            user = CustomUser.objects.get(pk=pk)
            user.email=data['email']
            user.first_name=data['first_name']
            user.last_name=data['last_name']
            user.phone_no=data['phone_no']
            user.address=data['address']
            user.save()
            return JsonResponse({'id': user.id,'email': user.email, 'first_name':user.first_name, 'last_name':user.last_name, 'phone_no':user.phone_no, 'address':user.address})
    
        elif request.method=='DELETE':
            user = CustomUser.objects.get(pk=pk)
            user.delete()
            return JsonResponse({'message': 'User soft deleted successfully'}, status=204)
        else:
            return JsonResponse({'error': 'Method Not Allowed'}, status=405)

class CustomUserRestoreView:
    @csrf_exempt
    def user_restore(request: HttpRequest, pk):
        if request.method=='POST':
            user = CustomUser.objects.get(pk=pk)
            user.restore()
            return JsonResponse({'message': 'User restored successfully'}, status=200)
        else:
            return JsonResponse({'error': 'Method Not Allowed'}, status=405)


class CustomUserHardDeleteView:
    @csrf_exempt
    def user_hard_delete(request: HttpRequest, pk):
        if request.method=='DELETE':
            user = CustomUser.objects.get(pk=pk)
            user.delete(hard_delete=True) 
            return JsonResponse({'message': 'User hard deleted successfully'}, status=204)

class LoginView:
    @csrf_exempt
    def login_authentication(request: HttpRequest):
        if request.method=='POST':
            token= TokenRegeneration.check_token(request)
            if token is None:
                data = json.loads(request.body)
                email=data['email']
                password=data['password']
                user=CustomUser.objects.filter(email=email).first()
                if user is None:
                    raise AuthenticationFailed('User not found')
                if not user.check_password(password):
                    raise AuthenticationFailed('Incorrect Password')
                response=LoginView.token_Generation(request,user)
                return response
            else:
                return token 
        
    def token_Generation(request, user):
        access_token_payload={
                'type':'access_token',
                'id':user.id,
                'email':user.email,
                'exp': math.floor(time.time())+600,
                'iat': math.floor(time.time())
            }
        access_token=jwt.encode(access_token_payload,"secret",algorithm="HS256")
        refresh_token_payload={
            'type':'refresh_token',
            'id':user.id,
            'email':user.email,
            'exp': math.floor(time.time())+3600,
            'iat': math.floor(time.time())
        }
        refresh_token=jwt.encode(refresh_token_payload,"secret",algorithm="HS256")
        response=JsonResponse({'message':'success','access_token':access_token,'refresh_token':refresh_token},status=200,safe=False)
        response.set_cookie('access_token',access_token, httponly=True)
        response.set_cookie('refresh_token',refresh_token, httponly=True)
        print(response)
        return response
    @csrf_exempt
    def logout(request):
        response = JsonResponse({'message': 'Logout successful'})
        response.set_cookie('access_token', '', expires=0)
        response.set_cookie('refresh_token', '', expires=0)
        
        return response

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
                    'exp': math.floor(time.time())+60,
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

# class CustomUserList(APIView):
#     def get(self, request, format=None):
#         users = CustomUser.objects.all()
#         serializer = CustomUserSerializer(users, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = CustomUserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class CustomUserDetail(APIView):
#     def get_object(self, pk):
#         try:
#             return CustomUser.objects.get(pk=pk)
#         except CustomUser.DoesNotExist:
#             raise Http404

#     def get(self, request, pk, format=None):
#         user = self.get_object(pk)
#         serializer = CustomUserSerializer(user)
#         return Response(serializer.data)

#     def put(self, request, pk, format=None):
#         user = self.get_object(pk)
#         serializer = CustomUserSerializer(user, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk, format=None):
#         user = self.get_object(pk)
#         user.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# @method_decorator(csrf_exempt, name='dispatch')
# class CustomUserListView(View):
#     def get(self, request):
#         if 'deleted' in request.GET and request.GET['deleted'].lower() == 'true':
#             users = CustomUser.objects.filter(deleted=True)
#         else:
#             # users = CustomUser.objects.all()
#             users = CustomUser.objects.filter(deleted=False)
#         user_data = [{'id': user.id,'email': user.email, 'first_name':user.first_name, 'last_name':user.last_name, 'phone_no':user.phone_no, 'address':user.address, 'deleted':user.deleted} for user in users]
#         return JsonResponse(user_data, safe=False)
    
#     def post(self, request):
#         data = json.loads(request.body)
#         user = CustomUser.objects.create(email=data['email'],first_name=data['first_name'], last_name=data['last_name'],phone_no=data['phone_no'], password=data['password'],address=data['address'])
#         return JsonResponse({'id': user.id,'email': user.email, 'first_name':user.first_name, 'last_name':user.last_name, 'phone_no':user.phone_no, 'address':user.address}, status=201)
    
# @method_decorator(csrf_exempt, name='dispatch')
# class CustomUserDetailView(View):
#     def get(self, request, pk):
#         user = CustomUser.objects.get(pk=pk)
#         user_data = {'id': user.id,'email': user.email, 'first_name':user.first_name, 'last_name':user.last_name, 'phone_no':user.phone_no, 'address':user.address}
#         return JsonResponse(user_data)

#     def patch(self, request, pk):
#         data = json.loads(request.body)
#         user = CustomUser.objects.get(pk=pk)
#         user.email=data['email']
#         user.first_name=data['first_name']
#         user.last_name=data['last_name']
#         user.phone_no=data['phone_no']
#         user.address=data['address']
#         user.save()
#         return JsonResponse({'id': user.id,'email': user.email, 'first_name':user.first_name, 'last_name':user.last_name, 'phone_no':user.phone_no, 'address':user.address})
    
#     def delete(self, request, pk):
#         user = CustomUser.objects.get(pk=pk)
#         user.delete()
#         return JsonResponse({'message': 'User soft deleted successfully'}, status=204)

# @method_decorator(csrf_exempt, name='dispatch')
# class CustomUserRestoreView(View):
#     def post(self, request, pk):
#         user = CustomUser.objects.get(pk=pk)
#         user.restore()
#         return JsonResponse({'message': 'User restored successfully'}, status=200)

# @method_decorator(csrf_exempt, name='dispatch')
# class CustomUserHardDeleteView(View):
#     def delete(self, request, pk):
#         user = CustomUser.objects.get(pk=pk)
#         user.delete(hard_delete=True) 
#         return JsonResponse({'message': 'User hard deleted successfully'}, status=204)