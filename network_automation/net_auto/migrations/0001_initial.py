# Generated by Django 2.2.4 on 2019-09-02 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.CharField(max_length=255)),
                ('hostname', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('ssh_port', models.IntegerField(default=22)),
                ('vendor', models.CharField(choices=[('cisco', 'Cisco'), ('mikrotik', 'Mikrotik')], max_length=255)),
            ],
        ),
    ]
