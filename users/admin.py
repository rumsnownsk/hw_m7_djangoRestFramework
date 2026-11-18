from django.contrib import admin

from lms.models import Lesson, Course
from .models import Payment, User
# Register your models here.


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment_date', 'amount', 'payment_method', 'paid_course', 'paid_lesson')
    list_filter = ('payment_method',)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'city')

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    # pass
    list_display = ('id', 'title', 'preview', 'description', 'video_url', 'course_id', 'created_at', 'updated_at')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    # pass
    list_display = ('id', 'title', 'preview', 'description', 'created_at', 'updated_at')