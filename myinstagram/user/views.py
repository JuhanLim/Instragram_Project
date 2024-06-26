import os
from uuid import uuid4
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from myinstagram.settings import MEDIA_ROOT
from .models import User
from django.contrib.auth.hashers import make_password


# Create your views here.
class Join(APIView):
    def get(self,request):
        return render(request,"user/join.html")
    
    def post(self,request):
        #TODO 회원가입
        email = request.data.get('email', None)
        nickname = request.data.get('nickname',None)
        name = request.data.get('name',None)
        password = request.data.get('password',None)
        
        User.objects.create(email=email, 
                            nickname=nickname, 
                            name=name, 
                            password=make_password(password),
                            profile_image="default_profile.jpg") # 입력한 데이터를 db 로 전송
        return Response(status=200)

class Login(APIView):
    def get(self,request):
        return render(request,"user/login.html")
    
    def post(self, request):
        # TODO 로그인
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = User.objects.filter(email=email).first()

        if user is None:
            return Response(status=400, data=dict(message="회원정보가 잘못되었습니다."))

        if user.check_password(password):
            # TODO 로그인을 했다. 세션 or 쿠키
            request.session['email'] = email
            return Response(status=200)
        else:
            return Response(status=400, data=dict(message="회원정보가 잘못되었습니다."))
        
        # if user is not None:
        #     request.session['email'] = email  # 세션에 사용자 ID 저장
        #     return Response(status=200)
        # else:
            
        #     return Response(status=401, data={'message': '유효하지 않습니다.'}) 

class LogOut(APIView):
    def get(self, request):
        request.session.flush()
        return render(request, "user/login.html")
    

    
class UploadProfile(APIView):
    def post(self, request):

        # 일단 파일 불러와
        file = request.FILES['file']
        email = request.data.get('email')

        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, uuid_name)

        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        profile_image = uuid_name

        user = User.objects.filter(email=email).first() # 업로드한 이미지를 보낼때 이멜도 같이 보내므로 그 이메일과 같은 이메일 사용자의 프로필 변경

        user.profile_image = profile_image
        user.save()

        return Response(status=200)