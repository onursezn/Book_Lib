# Generated by Django 3.0.5 on 2020-07-26 11:05

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import partial_date.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AbstractBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='authors')),
                ('name', models.CharField(max_length=255)),
                ('bio', models.TextField(blank=True, max_length=511)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isbn_10', models.CharField(blank=True, max_length=10)),
                ('isbn_13', models.CharField(max_length=13)),
                ('name', models.CharField(max_length=255)),
                ('release_date', partial_date.fields.PartialDateField(blank=True, null=True)),
                ('publisher', models.CharField(blank=True, max_length=255, null=True)),
                ('translator', models.CharField(blank=True, max_length=255, null=True)),
                ('page_number', models.IntegerField(blank=True, null=True)),
                ('description', models.CharField(blank=True, max_length=1023, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='books')),
                ('abstract_book', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child_books', to='api.AbstractBook')),
                ('authors', models.ManyToManyField(related_name='sub_books', to='api.Author')),
            ],
        ),
        migrations.CreateModel(
            name='BookList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='booklists')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, max_length=511)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(max_length=255)),
                ('spoiler', models.BooleanField(default=False)),
                ('booklist', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='api.BookList')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfileAPI',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='', max_length=255)),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('image', models.ImageField(blank=True, null=True, upload_to='users')),
                ('currently_reading', models.ManyToManyField(blank=True, related_name='current_readers', to='api.AbstractBook')),
                ('favorite_books', models.ManyToManyField(blank=True, related_name='bookLiker', to='api.AbstractBook')),
                ('followers', models.ManyToManyField(blank=True, related_name='followings', to='api.UserProfileAPI')),
                ('library', models.ManyToManyField(blank=True, related_name='owner', to='api.AbstractBook')),
                ('liked_lists', models.ManyToManyField(blank=True, related_name='listLiker', to='api.BookList')),
                ('my_books', models.ManyToManyField(blank=True, related_name='reader', to='api.AbstractBook')),
                ('read_list', models.ManyToManyField(blank=True, related_name='wisher', to='api.AbstractBook')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='userprofileapi', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField(max_length=1023)),
                ('spoiler', models.BooleanField(default=False)),
                ('abstract_book', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='api.AbstractBook')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='api.Author')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_reviews', to='api.UserProfileAPI')),
            ],
            options={
                'unique_together': {('user', 'abstract_book')},
                'index_together': {('user', 'abstract_book')},
            },
        ),
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('SPO', 'Spoiler'), ('INV', 'Invective'), ('VIO', 'Violence'), ('OTH', 'Other')], max_length=3)),
                ('text', models.TextField(blank=True, max_length=511, null=True, validators=[django.core.validators.MinLengthValidator(20)])),
                ('comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='complaints', to='api.Comment')),
                ('review', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='complaints', to='api.Review')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='complaints', to='api.UserProfileAPI')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='review',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='api.Review'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='api.UserProfileAPI'),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField(default='', max_length=255, unique=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='api.Category')),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.AddField(
            model_name='booklist',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='my_lists', to='api.UserProfileAPI'),
        ),
        migrations.AddField(
            model_name='author',
            name='followers',
            field=models.ManyToManyField(blank=True, to='api.UserProfileAPI'),
        ),
        migrations.AddField(
            model_name='abstractbook',
            name='authors',
            field=models.ManyToManyField(related_name='books', to='api.Author'),
        ),
        migrations.AddField(
            model_name='abstractbook',
            name='book_lists',
            field=models.ManyToManyField(blank=True, related_name='books', to='api.BookList'),
        ),
        migrations.AddField(
            model_name='abstractbook',
            name='category',
            field=models.ManyToManyField(related_name='books', to='api.Category'),
        ),
        migrations.AddField(
            model_name='abstractbook',
            name='pop_child_book',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='pop_of_parent', to='api.Book'),
        ),
        migrations.CreateModel(
            name='UpDownRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(choices=[(1, 'Up'), (-1, 'Down')])),
                ('book', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='api.Book')),
                ('bookList', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='api.BookList')),
                ('review', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='api.Review')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.UserProfileAPI')),
            ],
            options={
                'unique_together': {('user', 'review'), ('user', 'book'), ('user', 'bookList')},
                'index_together': {('user', 'review'), ('user', 'book'), ('user', 'bookList')},
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stars', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='api.AbstractBook')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_ratings', to='api.UserProfileAPI')),
            ],
            options={
                'unique_together': {('user', 'book')},
                'index_together': {('user', 'book')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='comment',
            unique_together={('user', 'review'), ('user', 'booklist')},
        ),
        migrations.AlterIndexTogether(
            name='comment',
            index_together={('user', 'review'), ('user', 'booklist')},
        ),
    ]
