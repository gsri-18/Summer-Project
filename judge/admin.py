from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Problem, TestCase, Submission

# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(Problem)
admin.site.register(TestCase)
admin.site.register(Submission)


