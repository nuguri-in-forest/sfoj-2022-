from django import forms
from sfoj_system.models import Board
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# form 이란 model 처럼 속성들을 저장할 수 있는 틀.
# form 을 사용하는 이유는 parameter 가 유효하게 전달됐는지 등을 확인하기 위함.

class BoardForm(forms.ModelForm):
    class Meta:
        model = Board  # 사용할 모델
        fields = ['title','content']  # BoardForm에서 사용할 Board 모델의 속성

        labels = {
            'title' : '제목',
            'content' : '내용',
        }

class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email")