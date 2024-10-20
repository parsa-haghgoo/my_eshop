from django.db import models


# Create your models here.

class ContactUs(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    email = models.EmailField(max_length=300, verbose_name='ایمیل')
    full_name = models.CharField(max_length=100, verbose_name='نام و نام خانوادگی')
    message = models.TextField(verbose_name='پیام شما')
    is_read_by_admin = models.BooleanField(default=False, verbose_name='دیده شده توسط ادمین')
    created_date = models.DateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)
    response = models.TextField(verbose_name='پاسخ پیام شما')

    class Meta:
        verbose_name = 'تماس با ما'
        verbose_name_plural = "تماس با ما"

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    image = models.ImageField(upload_to='images')
