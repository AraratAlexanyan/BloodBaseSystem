# Generated by Django 4.2.2 on 2023-07-01 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blood', '0002_blooddonate'),
    ]

    operations = [
        migrations.AddField(
            model_name='blooddonate',
            name='donor_name',
            field=models.CharField(max_length=30, null=True),
        ),
    ]