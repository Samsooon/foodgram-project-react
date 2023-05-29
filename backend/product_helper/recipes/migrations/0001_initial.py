# Generated by Django 2.2.16 on 2023-05-26 13:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-add_date'],
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='ingredient name')),
                ('measurement_unit', models.CharField(max_length=200, verbose_name='measurement unit')),
            ],
        ),
        migrations.CreateModel(
            name='Recipes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='recipe name')),
                ('image', models.ImageField(blank=True, upload_to='')),
                ('text', models.TextField(verbose_name='description')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='add date')),
                ('cooking_time', models.PositiveIntegerField(blank=True)),
            ],
            options={
                'verbose_name': 'recipe',
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='RecipesIngredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(null=True, verbose_name='amount of ingredient in recipe')),
            ],
        ),
        migrations.CreateModel(
            name='RecipesTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='tag name')),
                ('color', models.CharField(choices=[('#0000FF', 'Blue'), ('#FF0000', 'Red'), ('#FFFF00', 'Yellow'), ('#008000', 'Green')], max_length=7, unique=True, verbose_name='color')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='slug')),
            ],
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='carts', to='recipes.Recipes', verbose_name='recipes')),
            ],
        ),
    ]
