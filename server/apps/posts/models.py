from django.db import models

class Post(models.Model):
    # title, user, content, region, price
    title = models.CharField(max_length=64)
    user = models.CharField(max_length=32)
    # DB의 용량을 줄이고 돈도 아끼기 위해 필요한 것만 TextField로!
    content = models.TextField()
    region = models.CharField(max_length=16)
    price = models.IntegerField()
    # subtitle = models.~ 이러고 migration하면 오류 뜸! 원래 객체에는 없어서 해결해야 함 -> 다음 세션

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)