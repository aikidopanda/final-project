# Generated by Django 4.2 on 2023-04-30 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_faction_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='image',
            field=models.CharField(default='images/<django.db.models.fields.CharField>.webp', max_length=100, null=True),
        ),
    ]
