# Generated by Django 3.1.4 on 2020-12-23 17:46

import colorfield.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DazFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('raw_path', models.CharField(max_length=255, verbose_name='path')),
            ],
            options={
                'verbose_name': 'dazfile',
                'verbose_name_plural': 'dazfiles',
            },
        ),
        migrations.CreateModel(
            name='DazPreset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('scene_object', models.CharField(blank=True, max_length=255, null=True, verbose_name='scene object')),
                ('dazfile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='production.dazfile', verbose_name='daz preset file')),
            ],
            options={
                'verbose_name': 'dazpreset',
                'verbose_name_plural': 'dazpresets',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='working title')),
                ('title', models.CharField(max_length=255, verbose_name='release title')),
                ('slug', models.SlugField(allow_unicode=True, verbose_name='slug')),
                ('artifacts_folder', models.CharField(help_text='Where to store generated files for this project', max_length=255, verbose_name='artifacts folder')),
            ],
            options={
                'verbose_name': 'project',
                'verbose_name_plural': 'projects',
            },
        ),
        migrations.CreateModel(
            name='Shot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('camera', models.CharField(blank=True, help_text='If blank, will use whatever camera is selected in the loaded scene file', max_length=255, null=True, verbose_name='camera')),
                ('presets', models.ManyToManyField(to='production.DazPreset', verbose_name='presets')),
                ('scene_file', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='production.dazfile', verbose_name='scene file')),
            ],
            options={
                'verbose_name': 'shot',
                'verbose_name_plural': 'shots',
            },
        ),
        migrations.CreateModel(
            name='Screenplay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('text_file', models.FileField(max_length=255, upload_to=None, verbose_name='screenplay file')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='production.project', verbose_name='project')),
            ],
            options={
                'verbose_name': 'screenplay',
                'verbose_name_plural': 'screenplays',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('dazfiles', models.ManyToManyField(to='production.DazFile', verbose_name='daz files')),
                ('dazpresets', models.ManyToManyField(to='production.DazPreset', verbose_name='daz presets')),
                ('projects', models.ManyToManyField(to='production.Project', verbose_name='projects')),
            ],
            options={
                'verbose_name': 'location',
                'verbose_name_plural': 'locations',
            },
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text="Character's short name or speaking label", max_length=255, verbose_name='name')),
                ('color', colorfield.fields.ColorField(blank=True, default=None, help_text='Custom color for the dialog label (optional)', max_length=18, null=True, verbose_name='accent color')),
                ('dazfiles', models.ManyToManyField(to='production.DazFile', verbose_name='daz files')),
                ('dazpresets', models.ManyToManyField(to='production.DazPreset', verbose_name='daz presets')),
                ('projects', models.ManyToManyField(to='production.Project', verbose_name='projects')),
            ],
            options={
                'verbose_name': 'character',
                'verbose_name_plural': 'characters',
            },
        ),
    ]
