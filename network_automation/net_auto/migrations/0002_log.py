# Generated by Django 2.2.4 on 2019-09-02 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('net_auto', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target', models.CharField(max_length=255)),
                ('action', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=255)),
                ('time', models.DateTimeField(null=True)),
                ('messages', models.CharField(blank=True, max_length=255)),
            ],
        ),
    ]