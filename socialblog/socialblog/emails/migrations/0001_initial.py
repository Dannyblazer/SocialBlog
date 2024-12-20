# Generated by Django 4.2.13 on 2024-09-07 10:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('READY', 'Ready'), ('SENDING', 'Sending'), ('SENT', 'Sent'), ('FAILED', 'Failed')], db_index=True, default='READY', max_length=50)),
                ('to', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=255)),
                ('html', models.TextField()),
                ('plain_text', models.TextField()),
                ('sent_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
