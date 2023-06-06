from django.db import models
from users.models import User

MAX_LENGHT_CONT = 200
MAX_LENGHT_FOR_COLOR = 7


class Ingredient(models.Model):
    name = models.CharField(
        max_length=MAX_LENGHT_CONT,
        verbose_name='ingredient name'
    )
    measurement_unit = models.CharField(
        max_length=MAX_LENGHT_CONT,
        verbose_name='measurement unit'
    )

    class Meta:
        verbose_name = 'Ingredient'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


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
        max_length=MAX_LENGHT_CONT,
        unique=True,
        verbose_name='tag name'
    )
    color = models.CharField(
        max_length=MAX_LENGHT_FOR_COLOR,
        choices=COLOR_CHOICES,
        unique=True,
        verbose_name='color'
    )
    slug = models.SlugField(
        max_length=MAX_LENGHT_CONT,
        unique=True,
        verbose_name='slug'
    )

    class Meta:
        verbose_name = 'Tag'

    def __str__(self):
        return f'{self.name}, {self.color}, {self.slug}'


class Recipes(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="author",
    )
    name = models.CharField(
        max_length=MAX_LENGHT_CONT,
        verbose_name='recipe name'
    )
    image = models.ImageField(
        blank=True,
        verbose_name='image'
    )
    text = models.TextField(
        verbose_name='description'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipesIngredient',
        related_name='recipes',
        blank=True,
        verbose_name='Ingredients'
    )
    tags = models.ManyToManyField(
        Tag,
        through='RecipesTag',
        related_name='recipes',
        blank='True',
        verbose_name='tags'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='add date'
    )
    cooking_time = models.PositiveIntegerField(
        blank=True,
        verbose_name='cooking time'
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'recipe'

    def __str__(self):
        return f'{self.author}, {self.name}, {self.text}'


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
        verbose_name = 'amount ingredient in recipe'

    def __str__(self):
        return f'{self.ingredient}, {self.recipe}, {self.amount}'


class RecipesTag(models.Model):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='recipe tag'
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        verbose_name='recipe'
    )

    class Meta:
        verbose_name = 'tags in recipe'

    def __str__(self):
        return f'{self.tag}, {self.recipe}'


class Favorite(models.Model):
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        verbose_name='recipe'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='user'
    )
    add_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='add date'
    )

    class Meta:
        ordering = ['-add_date']
        unique_together = ("recipe", 'user')
        verbose_name = 'favorite'

    def __str__(self):
        return f'{self.recipe}, {self.add_date}'


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
        verbose_name = 'shopping cart'

    def __str__(self):
        return f'{self.user}, {self.recipe}'
