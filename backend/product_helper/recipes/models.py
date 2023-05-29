from django.db import models
from users.models import User


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='ingredient name'
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='measurement unit'
    )


class Tag(models.Model):
    BLUE = '#0000FF'
    RED = '#FF0000'
    YELLOW = '#FFFF00'
    GREEN = '#008000'

    COLOR_CHOICES = [
        (BLUE, 'Blue'),
        (RED, 'Red'),
        (YELLOW, 'Yellow'),
        (GREEN, 'Green'),
    ]
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='tag name'
    )
    color = models.CharField(
        max_length=7,
        choices=COLOR_CHOICES,
        unique=True,
        verbose_name='color'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='slug'
    )


class Recipes(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="author",
    )
    name = models.CharField(
        max_length=200,
        verbose_name='recipe name'
    )
    image = models.ImageField(
        blank=True
    )
    text = models.TextField(
        verbose_name='description'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipesIngredient',
        related_name='recipes',
        blank=True
    )
    tags = models.ManyToManyField(
        Tag,
        through='RecipesTag',
        related_name='recipes',
        blank='True'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='add date'
    )
    cooking_time = models.PositiveIntegerField(blank=True)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'recipe'


class RecipesIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='ingredients in recipes'
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        verbose_name='recipe'
    )
    amount = models.PositiveIntegerField(
        null=True,
        verbose_name='amount of ingredient in recipe'
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('ingredient', 'recipe',),
                name='unique ingredient amount',
            ),
        )


class RecipesTag(models.Model):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='recipe tag'
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
    )


class Favorite(models.Model):
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        verbose_name='recipe'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    add_date = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-add_date']
        unique_together = ("recipe", 'user')


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='user'
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='recipes'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique shopping cart'
            )
        ]
