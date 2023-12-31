# Generated by Django 4.2.6 on 2023-10-31 10:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import main.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('body', models.TextField()),
                ('published_date', models.DateField(auto_now_add=True)),
                ('subforum', models.PositiveSmallIntegerField(choices=[(1, 'General'), (2, 'Films'), (3, 'Games'), (4, 'Pol')], default=1)),
                ('picture', models.ImageField(blank=True, null=True, upload_to=main.models.subfolder_manage)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='threads', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SavedThread',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thread', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saved', to='main.thread')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saved', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('published_date', models.DateField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('thread', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='main.thread')),
            ],
        ),
    ]
