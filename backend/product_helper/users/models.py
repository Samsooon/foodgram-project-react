from django.contrib.auth.models import AbstractUser
from django.db import models

MAX_LENGHT_FOR_EMAIL_CONST = 254
MAX_LENGHT_CONST = 150


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    email = models.EmailField(
        max_length=MAX_LENGHT_FOR_EMAIL_CONST,
        unique=True,
        verbose_name='email'
    )
    username = models.CharField(
        max_length=MAX_LENGHT_CONST,
        unique=True,
        verbose_name='username'
    )
    first_name = models.CharField(
        max_length=MAX_LENGHT_CONST,
        blank=True,
        verbose_name='first name'
    )
    last_name = models.CharField(
        max_length=MAX_LENGHT_CONST,
        blank=True,
        verbose_name='last name'
    )

    class Meta:
        verbose_name='User'

    def __str__(self):
        return f'{self.email}, {self.username}, {self.first_name}, {self.last_name}'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='user'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author',
        verbose_name='followed user'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'following'],
                                    name='unique_user_subscribers')
        ]
        verbose_name='Follow'

    def __str__(self):
        return f'{self.user}, {self.following}'