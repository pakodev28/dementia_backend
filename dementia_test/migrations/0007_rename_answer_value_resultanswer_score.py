# Generated by Django 3.2.9 on 2022-04-25 11:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dementia_test', '0006_auto_20220425_1223'),
    ]

    operations = [
        migrations.RenameField(
            model_name='resultanswer',
            old_name='answer_value',
            new_name='score',
        ),
    ]
