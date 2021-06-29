# Generated by Django 3.0 on 2021-05-21 16:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0006_auto_20210518_1300'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoleRqst',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uname', models.CharField(max_length=30)),
                ('roletype', models.PositiveIntegerField(choices=[(1, 'owner'), (2, 'customer')])),
                ('proof', models.ImageField(null=True, upload_to='')),
                ('is_checked', models.BooleanField(default=0)),
                ('uid', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
