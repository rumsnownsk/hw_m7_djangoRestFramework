from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone


# Create your models here.
class UserManager(BaseUserManager):
    """Менеджер пользователя, где username не нужен — только email."""

    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("У пользователя должен быть email")
        user = self.model(
            email=self.normalize_email(email),
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Суперпользователь должен иметь is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="ник(username)",
        unique=False,
        help_text="Необязательное имя пользователя",
    )
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

    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["email"]

    def __str__(self):
        return f"Пользователь #{self.email}"


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ("cash", "Наличные"),
        ("transfer", "Перевод на счет"),
    ]

    STATUS_CHOICES = [
        ("pending", "Ожидает оплаты"),
        ("paid", "Оплачен"),
        ("canceled", "Отменён"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Пользователь",
        related_name="payments",
    )
    paid_course = models.ForeignKey(
        "lms.Course",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Оплаченный курс",
        related_name="payments",
    )
    paid_lesson = models.ForeignKey(
        "lms.Lesson",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Оплаченный урок",
        related_name="payments",
    )
    payment_date = models.DateTimeField(
        default=timezone.now,
        verbose_name="Дата оплаты",
        help_text="Дата и время оплаты",
    )
    amount = models.PositiveIntegerField(
        verbose_name="Сумма оплаты", help_text="Сумма оплаты в рублях"
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        verbose_name="Способ оплаты",
    )
    session_id = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="ID сессии",
        help_text="Укажите ID сессии",
    )

    link = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Ссылка на оплату",
        help_text="Укажите ссылку на оплату",
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name="Статус",
    )

    def get_paid_object(self):
        return self.paid_course or self.paid_lesson

    class Meta:
        verbose_name = "Платёж"
        verbose_name_plural = "Платежи"
        ordering = ["-payment_date"]

    def __str__(self):
        return f"{self.user} — {self.amount} руб. ({self.get_payment_method_display()})"
