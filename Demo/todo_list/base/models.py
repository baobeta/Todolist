from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Task(models.Model):
    #Set khoa ngoai voi User
    user= models.ForeignKey(
        User,on_delete=models.CASCADE, null=True, blank=True)
    # Tieu de voi noi dung khong qua 200
    title=models.CharField(max_length=200)
    # Mo ta dang dang Text field
    description=models.TextField(null=True, blank=True)
    # Thoi gian hoan thanh mac dinh la False
    complete=models.BooleanField(default=False)
    # Tu dong chon thoi gian tao bang thoi gian hien tai
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title  #Hien thi Title trong Database

    class Meta:
        ordering= ['complete']




