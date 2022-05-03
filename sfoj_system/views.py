from django.db.models.fields import NullBooleanField
from django.http.response import HttpResponseBase
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.http import HttpResponse
from .forms import BoardForm,UserForm
from .models import *
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib import messages

"""
views.py Ground rule
1. rendering 함수는 모두 소문자로 설정한다.
2. 각 함수에서 생성하는 객체의 리스트는 객체_list 라고 명명한다
3. 렌더링함수에 설명이 필요한 부분은 주석처리를 한다.
"""

# main
def index(request):
    return render(request, 'sfoj_system/index.html')

# 문제 리스트 조회
def list(request):
    # parameter
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw','') # 검색어(keyword)
    so = request.GET.get('so','recent') # 정렬기준(sorting option), default = recent
    type = request.GET.get('search_type','all')


    # 정렬
    if so == 'old': # 오래된순
        board_list = Board.objects.order_by('reg_date')
    else: # 최신순
        board_list = Board.objects.order_by('-reg_date')

    # 검색
    if kw:
        if len(kw) > 1:
            if type == 'all': # 전체
                board_list = board_list.filter( Q(title__icontains=kw)|Q(content__icontains=kw)|Q(user_id__username__icontains=kw)).distinct()
            elif type == 'title': # 제목
                board_list = board_list.filter( Q(title__icontains=kw) ).distinct()
            elif type == 'title_content': # 제목+내용
                board_list = board_list.filter( Q(title__icontains=kw)|Q(content__icontains=kw) ).distinct()
            elif type == 'content': # 내용
                board_list = board_list.filter( Q(content__icontains=kw)).distinct()
            elif type == 'writer':  # 글쓴이
                board_list = board_list.filter( Q(user_id__username__icontains=kw) ).distinct()

        else: # error
            messages.error(request,'검색어는 2글자 이상 입력해주세요.')

    # 페이징 처리
    paginator = Paginator(board_list, 15)  # 한 페이지에 15개씩
    page_obj = paginator.get_page(page)

    context = {'board_list': page_obj,'page':page,'kw': kw, 'so':so, 'search_type': type }
    return render(request, 'sfoj_system/Board_list.html', context)

# 문제 상세
def detail(request, board_index):
    board = get_object_or_404(Board, pk=board_index)
    context = {'board': board}
    return render(request, 'sfoj_system/Board_detail.html', context)

# 문제 업로드
def uploads(request):
    # post ==> uploads화면에서 저장하기 버튼을 눌렀을 때
    # get ==> list화면에서 문제 업로드 버튼을 눌렀을때
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.user_id = request.user #request에서 로그인한 user를 가져옴
            board.Reg_date = timezone.now()
            board.save()
            return redirect('sfoj_system:list')
    else:
        form = BoardForm()
    context = {'form':form}
    return render(request,'sfoj_system/Board_uploads.html',context)

# 회원가입
def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('sfoj_system:index')
    else:
        form = UserForm()
    return render(request, 'common:signup', {'form': form})