# Generated by Django 5.0.9 on 2024-09-27 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netbox_netauto_plugin', '0004_flexapplication_dst_address_string_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flexapplication',
            name='dst_address_string',
            field=models.CharField(blank=True, max_length=18, null=True),
        ),
        migrations.AlterField(
            model_name='flexapplication',
            name='http',
            field=models.CharField(default='http_xff_hsts', max_length=50),
        ),
        migrations.AlterField(
            model_name='flexapplication',
            name='persistence_profile',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='flexapplication',
            name='tcp_lan',
            field=models.CharField(default='tcp_lan', max_length=50),
        ),
        migrations.AlterField(
            model_name='flexapplication',
            name='tcp_wan',
            field=models.CharField(default='tcp_wan', max_length=50),
        ),
        migrations.AlterField(
            model_name='l4application',
            name='dst_address_string',
            field=models.CharField(blank=True, max_length=18, null=True),
        ),
        migrations.AlterField(
            model_name='l4application',
            name='persistence_profile',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='l4application',
            name='tcp_lan',
            field=models.CharField(default='tcp_lan', max_length=50),
        ),
        migrations.AlterField(
            model_name='l4application',
            name='tcp_wan',
            field=models.CharField(default='tcp_lan', max_length=50),
        ),
        migrations.AlterField(
            model_name='mtlsapplication',
            name='dst_address_string',
            field=models.CharField(blank=True, max_length=18, null=True),
        ),
        migrations.AlterField(
            model_name='mtlsapplication',
            name='http',
            field=models.CharField(default='http_xff', max_length=50),
        ),
        migrations.AlterField(
            model_name='mtlsapplication',
            name='persistence_profile',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='mtlsapplication',
            name='tcp_lan',
            field=models.CharField(default='tcp_lan', max_length=50),
        ),
        migrations.AlterField(
            model_name='mtlsapplication',
            name='tcp_wan',
            field=models.CharField(default='tcp_lan', max_length=50),
        ),
    ]
