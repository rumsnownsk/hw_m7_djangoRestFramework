from django.db import models


# Create your models here.
class Course(models.Model):
    title = models.CharField(
        max_length=50, verbose_name="Название", help_text="Введите название"
    )
    preview = models.ImageField(
        upload_to="lms/courses", blank=True, null=True, verbose_name="Картинка"
    )
    description = models.TextField(
        verbose_name="Описание курса", help_text="Введите описание курса"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата изменения",
    )

    def __str__(self):
        return f"курс: {self.title}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="lessons",
        verbose_name="курс",
    )

    title = models.CharField(
        max_length=50, verbose_name="Название", help_text="Введите название"
    )
    preview = models.ImageField(
        upload_to="lms/lessons", blank=True, null=True, verbose_name="Картинка "
    )
    description = models.TextField(
        verbose_name="Описание курса", help_text="Введите описание курса"
    )
    video_url = models.URLField(verbose_name="Ссылка на видео", blank=True, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата изменения",
    )

    def __str__(self):
        return f"Урок: {self.title}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
