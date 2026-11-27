from django.contrib import admin
from django.utils.html import format_html

from lms.models import Course, Lesson

from .models import Payment, User

# Register your models here.


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "payment_date",
        "amount",
        "payment_method",
        "paid_course",
        "paid_lesson",
    )
    list_filter = ("payment_method",)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ("is_staff", "is_superuser", "city")
    list_display = ("id", "email", "phone", "city", "user_role")
    ordering = ("-id",)
    search_fields = ("email", "phone")

    def user_role(self, obj):
        if obj.is_superuser:
            return format_html(
                '<span style="{}">СуперЮзер</span>', "color: red; font-weight: bold;"
            )
        elif obj.is_staff:
            return format_html(
                '<span style="{}">Администратор</span>',
                "color: orange; font-weight: bold;",
            )
        else:
            return "Пользователь"

    user_role.short_description = "Роль"
    user_role.admin_order_field = (
        "is_staff"  # Позволяет кликать и сортировать по этому столбцу
    )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    # pass
    list_display = (
        "id",
        "title",
        "preview",
        "description",
        "video_url",
        "course_id",
        "created_at",
        "updated_at",
    )


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    # pass
    list_display = ("id", "title", "preview", "description", "created_at", "updated_at")
