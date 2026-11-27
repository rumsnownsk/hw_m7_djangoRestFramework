from django.db import models

from config import settings


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

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Автор",
        help_text="Указать автора",
        related_name="courses",
    )

    def __str__(self):
        return f"курс: {self.title}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["id"]


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
    video_url = models.URLField(
        verbose_name="Ссылка на видео",
        blank=True,
        null=True,
        help_text="Обязательно Youtube.com",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата изменения",
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Автор",
        help_text="Указать автора",
        related_name="lessons",
    )

    def __str__(self):
        return f"Урок: {self.title}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["id"]


class Subscription(models.Model):
    """Подписка пользователя на обновления курса."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="пользователь",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="курс",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="дата подписки")

    class Meta:
        verbose_name = "подписка"
        verbose_name_plural = "подписки"
        constraints = [
            # защита от двойной подписки на уровне базы
            models.UniqueConstraint(
                fields=("user", "course"), name="unique_user_course_subscription"
            )
        ]

    def __str__(self):
        return f"{self.user} → {self.course}"
