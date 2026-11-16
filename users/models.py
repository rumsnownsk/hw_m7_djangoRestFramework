from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name="Email", help_text="Укажите почту"
    )

    phone = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="Телефон"
    )
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name="Город")
    avatar = models.ImageField(
        upload_to="users/avatars/",
        # upload_to=get_user_avatar_path,
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Ваше фото",
    )

    USERNAME_FIELD = "email"  # ← авторизация теперь по email
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["email"]

    def __str__(self):
        return f"Пользователь #{self.email}"


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="Пользователь",
        related_name='payments',
    )
    paid_course = models.ForeignKey(
        'lms.Course',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Оплаченный курс",
        related_name='payments'
    )
    paid_lesson = models.ForeignKey(
        'lms.Lesson',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Оплаченный урок",
        related_name='payments'
    )
    payment_date = models.DateTimeField(
        auto_now_add=False, verbose_name='Дата оплаты', help_text="Дата и время оплаты"
    )
    amount = models.PositiveIntegerField(
        verbose_name='Сумма оплаты', help_text='Сумма оплаты в рублях'
    )
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name='Способ оплаты',
    )

    class Meta:
        verbose_name = "Платёж"
        verbose_name_plural = "Платежи"
        ordering = ['-payment_date']

    def __str__(self):
        return f'{self.user} — {self.amount} руб. ({self.get_payment_method_display()})'
