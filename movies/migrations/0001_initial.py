# Generated by Django 2.2.1 on 2019-05-28 09:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actors', models.CharField(blank=True, max_length=200, null=True)),
                ('awards', models.CharField(blank=True, max_length=100, null=True)),
                ('box_office', models.CharField(blank=True, max_length=20, null=True)),
                ('countries', models.CharField(blank=True, max_length=100, null=True)),
                ('directors', models.CharField(blank=True, max_length=100, null=True)),
                ('dvd', models.DateField(blank=True, null=True)),
                ('genres', models.CharField(blank=True, max_length=100, null=True)),
                ('imdb_rating', models.FloatField(blank=True, null=True)),
                ('imdb_id', models.CharField(max_length=20, unique=True)),
                ('imdb_votes', models.CharField(blank=True, max_length=10, null=True)),
                ('languages', models.CharField(blank=True, max_length=100, null=True)),
                ('metascore', models.IntegerField(blank=True, null=True)),
                ('plot', models.CharField(blank=True, max_length=500, null=True)),
                ('poster', models.URLField(blank=True, null=True)),
                ('production', models.CharField(blank=True, max_length=100, null=True)),
                ('rated', models.CharField(blank=True, max_length=5, null=True)),
                ('released', models.DateField(blank=True, null=True)),
                ('response', models.CharField(max_length=5)),
                ('runtime', models.CharField(blank=True, max_length=10, null=True)),
                ('title', models.CharField(max_length=200)),
                ('type', models.CharField(blank=True, max_length=20, null=True)),
                ('website', models.URLField(blank=True, null=True)),
                ('writers', models.CharField(blank=True, max_length=300, null=True)),
                ('year', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MovieRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=10)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='movies.Movie')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=500)),
                ('created', models.DateTimeField(auto_now=True)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='movies.Movie')),
            ],
        ),
    ]