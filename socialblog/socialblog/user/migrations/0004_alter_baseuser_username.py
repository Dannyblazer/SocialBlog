# Generated by Django 4.2.13 on 2024-06-30 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_follow'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseuser',
            name='username',
            field=models.CharField(max_length=50, unique=True, verbose_name='username'),
        ),
    ]
