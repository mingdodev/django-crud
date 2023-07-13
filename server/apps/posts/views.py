from django.shortcuts import render, redirect
from .models import Post

def hello_world(request):
    return render(request, "posts/hello_world.html")

def posts_list(request, *args, **kwargs):

    posts = Post.objects.all()
    print(posts)

    # context 자리의 자료형은 dictionary
    return render(request, "posts/posts_list.html", {"posts":posts})

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

def posts_read(request, pk, *args, **kwargs):
    # args : 튜플 - 얘네는 앞에 들어오지 않은 매개변수들을 불러와 줌! 필수는 아님.
    # 예를 들어 naver.com?a=b=4c= : (값이) 필요없을 수도 있는 변수들(a,c)에 쉽게 대응하기 위해 적는 것.
    # kwargs : 딕셔너리. 만약 pk 매개변수에 안 넣어주면 여기에 pk가 들어감. 우리가 url에 int:pk 넣어줬기 때문에 존재하는데,
    # 들어갈 자리가 없네!! 그런데 key값과 value값이 있네!! 그러니 딕셔너리 자료형인 kwargs에 들어감.

    post = Post.objects.get(id=pk)
    print(post)

    return render(request, "posts/posts_read.html",{"post":post})

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