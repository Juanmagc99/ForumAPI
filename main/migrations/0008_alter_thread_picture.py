# Generated by Django 4.2.6 on 2023-10-27 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_thread_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thread',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='thread_pictures/<django.db.models.fields.related.ForeignKey>'),
        ),
    ]
