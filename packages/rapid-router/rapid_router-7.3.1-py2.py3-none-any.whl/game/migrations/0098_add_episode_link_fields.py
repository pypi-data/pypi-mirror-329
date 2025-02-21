# Generated by Django 3.2.25 on 2024-08-23 23:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0097_add_python_den_levels'),
    ]

    operations = [
        migrations.AddField(
            model_name='episode',
            name='lesson_plan_link',
            field=models.CharField(blank=True, default=None, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='episode',
            name='slides_link',
            field=models.CharField(blank=True, default=None, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='episode',
            name='video_link',
            field=models.CharField(blank=True, default=None, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='episode',
            name='worksheet_link',
            field=models.CharField(blank=True, default=None, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='episode',
            name='next_episode',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='game.episode'),
        ),
        migrations.AlterField(
            model_name='level',
            name='next_level',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='prev_level', to='game.level'),
        ),
    ]
