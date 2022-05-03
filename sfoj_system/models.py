from django.contrib.auth.models import User
from django.db import models
"""
models.py Ground rule
1. 모델명은 각 단어의 첫문자를 대문자로 설정한다
2. 각 모델의 속성은 소문자와 언더바를 활용한다
"""

class Board(models.Model):
    index = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE) #uploads 렌더링함수에서 사용
    title = models.CharField(max_length=100)
    content = models.TextField()
    hit = models.IntegerField(default=0)
    #Success_per = models.IntegerField(null=True)
    reg_date = models.DateTimeField(null=True)


class Judge_State(models.Model):
    submit_idx = models.IntegerField()
    UserID = models.CharField(max_length=15)
    States = models.CharField(max_length=5) #perhaps true false?
    Memory_use = models.IntegerField()
    Time_Complex = models.IntegerField()
    Submission_Time = models.DateTimeField()

class Users(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    useremail = models.CharField(max_length=128)
    reg_date = models.DateTimeField(auto_now_add = True)

class Code_History(models.Model):
    index = models.AutoField(primary_key=True)
    UserID = models.CharField(max_length=15)
    Board_idx = models.IntegerField()
    answer = models.TextField()