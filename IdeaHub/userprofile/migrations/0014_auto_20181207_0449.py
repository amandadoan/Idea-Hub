# Generated by Django 2.1.3 on 2018-12-07 04:49

from django.db import migrations, models
import userprofile.models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0013_auto_20181124_1043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to=userprofile.models.user_directory_path),
        ),
    ]