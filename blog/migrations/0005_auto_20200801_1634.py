# Generated by Django 3.0.8 on 2020-08-01 16:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20200801_1501'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='readnum',
            options={'verbose_name': '阅读量', 'verbose_name_plural': '阅读量'},
        ),
        migrations.RenameField(
            model_name='readnum',
            old_name='views',
            new_name='read_num',
        ),
    ]
