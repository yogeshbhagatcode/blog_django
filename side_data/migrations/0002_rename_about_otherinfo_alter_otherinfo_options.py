# Generated by Django 5.0 on 2024-01-09 18:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('side_data', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='About',
            new_name='OtherInfo',
        ),
        migrations.AlterModelOptions(
            name='otherinfo',
            options={'verbose_name_plural': 'About'},
        ),
    ]
