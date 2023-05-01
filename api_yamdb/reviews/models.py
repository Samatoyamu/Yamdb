from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api.validators import validate_regex


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = [
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (USER, 'Пользователь'),
    ]
    email = models.EmailField(
        'Электронная почта',
        max_length=254,
        unique=True,
    )
    bio = models.TextField(
        'Биография',
        null=True,
        blank=True,
    )
    role = models.CharField(
        'Роль пользователя',
        blank=True,
        max_length=100,
        choices=ROLES,
        default=USER,
    )
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
        validators=[validate_regex]
    )
    confirmation_code = models.CharField(
        'Код авторизации',
        max_length=10000000,
        blank=True,
        null=True
    )

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    class Meta:
        verbose_name = 'Пользователи'
        ordering = ['username']

    def __str__(self) -> str:
        return self.username


class Genre(models.Model):
    """Жанр произведения. Содержит название и slug"""
    name = models.CharField(verbose_name='Название жанра', max_length=256)
    slug = models.SlugField(verbose_name='Slug имя жанра',
                            max_length=50,
                            unique=True)

    class Meta:
        ordering = ['slug']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Category(models.Model):
    """Категория (тип) произведения. Например, 'фильм', 'книга' """
    name = models.CharField(verbose_name='Название категории', max_length=256)
    slug = models.SlugField(verbose_name='Slug имя категории',
                            max_length=50,
                            unique=True)

    class Meta:
        ordering = ['slug']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведение"""
    name = models.CharField(verbose_name='Название произведения',
                            max_length=256)
    year = models.PositiveSmallIntegerField(
        verbose_name='Год выпуска произведения', db_index=True)
    description = models.TextField(verbose_name='Описание произведения',
                                   blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True, related_name='titles')
    genre = models.ManyToManyField(Genre, related_name='titles')

    class Meta:
        ordering = ['name']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='произведение'
    )
    text = models.CharField(
        max_length=200
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='автор'
    )
    score = models.IntegerField(
        'оценка',
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10)
        ),
        error_messages={'validators': 'Оценка от 1 до 10!'},
    )
    pub_date = models.DateTimeField(
        'дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author', ),
                name='unique review'
            )]
        ordering = ('pub_date',)

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='отзыв'
    )
    text = models.CharField(
        'текст комментария',
        max_length=200
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='автор'
    )
    pub_date = models.DateTimeField(
        'дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
