from django.shortcuts import render, redirect
from .models import Post, Like

from django.http.request import HttpRequest
# type 주석. vs코드에서 인식을 잘하라고 붙여주는 것. 자동완성이 잘 됨. request: HttpRequest...

from django.db.models import Q

def hello_world(request):
    return render(request, "posts/hello_world.html")

def posts_create(request, *args, **kwargs):
    # 생성할 때. get방식 아닐 때
    if request.method == "POST":
        print(request.POST)
        Post.objects.create(
                title=request.POST["title"],
                user=request.POST["user"],
                region=request.POST["region"],
                price=request.POST["price"],
                content=request.POST["content"],
            )
        return redirect("/")
    return render(request, "posts/posts_create.html")

def posts_list(request: HttpRequest, *args, **kwargs):

    # 오류 text = request.GET["text"]
    # 값이 없을 경우 None을 반환합니다.
    text = request.GET.get("text")
    min = request.GET.get("min_price")
    max = request.GET.get("max_price")

    posts = Post.objects.all()

    if text:
        # 장고 쿼리셋 lookup
        # get은 하나만 가져올 수 있지만 filter는 여러 개 가져올 수 있음
        # or만 q and는 ,로 연결 가능
        posts = posts.filter(Q(title__contains=text) | Q(content__contains=text))

    if min and max and min <= max:
        posts = posts.filter(price__gte=min, price__lte=max)
    elif min:
        posts = posts.filter(price__gte=min)
    elif max:
        posts = posts.filter(price__lte=max)

    # context 자리의 자료형은 dictionary
    return render(request, "posts/posts_list.html", {"posts":posts})

def posts_read(request, pk, *args, **kwargs):
    # args : 튜플 - 얘네는 앞에 들어오지 않은 매개변수들을 불러와 줌! 필수는 아님.
    # 예를 들어 naver.com?a=b=4c= : (값이) 필요없을 수도 있는 변수들(a,c)에 쉽게 대응하기 위해 적는 것.
    # kwargs : 딕셔너리. 만약 pk 매개변수에 안 넣어주면 여기에 pk가 들어감. 우리가 url에 int:pk 넣어줬기 때문에 존재하는데,
    # 들어갈 자리가 없네!! 그런데 key값과 value값이 있네!! 그러니 딕셔너리 자료형인 kwargs에 들어감.

    post = Post.objects.get(id=pk)
    print(post)

    # 현재 글에 이미 좋아요를 눌렀나? 이미 눌렀으면 like에 뭐가 들어있음.
    # 근데 안 눌렀으면 like에 None이 들어가 있을 것.
    # get을 안 쓰고 filter를 쓴 이유 : get은 아무것도 없으면 오류가 나서.
    like = Like.objects.filter(post_id=pk).first()

    if request.method == "POST":
        if like == None:
            Like.objects.create(post_id=pk)
        else:
            # 좋아요 해제
            like.delete()
        return redirect(f"/posts/{pk}")

    return render(request, "posts/posts_read.html",{"post":post, "like":like})

def posts_delete(request, pk, *args, **kwargs):
    # DELETE / PUT... -> REST API (공부)
    # 삭제해야 할 때 -> 삭제하기 버튼 눌러서 POST로 왔을 때
    if request.method == "POST":
        post = Post.objects.get(id=pk)
        post.delete()

    return redirect("/")

def posts_update(request, pk, *args, **kwargs):

    post = Post.objects.get(id=pk)

    if request.method ==  "POST":
        # 수정하는 부분
            post.title=request.POST["title"]
            post.user=request.POST["user"]
            post.region=request.POST["region"]
            post.price=request.POST["price"]
            post.content=request.POST["content"]
            post.save()
            return redirect(f"/posts/{post.id}") # 파이썬에서 문자열 안에 문자를 쓸려면 f 써줘야 함.

    return render(request, "posts/posts_update.html", {"post":post})

def posts_like(request, *args, **kwargs):

    likes = Like.objects.all()

    posts = []
    # likes : 좋아요 한 글들의 id의 쿼리셋
    # posts : 좋아요 한 글들의 리스트
    for like in likes:
        # like.post_id : 좋아요 한 글의 id
        posts.append(Post.objects.get(id=like.post_id))

    return render(request, "posts/posts_like.html", {"posts":posts})