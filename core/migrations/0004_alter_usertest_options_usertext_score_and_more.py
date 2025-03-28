# Generated by Django 5.1 on 2025-03-27 19:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_uservideo_options_alter_userchapter_score_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usertest',
            options={'ordering': ('test__order',), 'verbose_name': 'User test', 'verbose_name_plural': 'User tests'},
        ),
        migrations.AddField(
            model_name='usertext',
            name='score',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='Score (%)'),
        ),
        migrations.AddField(
            model_name='uservideo',
            name='score',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='Score (%)'),
        ),
        migrations.AlterField(
            model_name='usertest',
            name='test',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_test', to='core.test', verbose_name='Test'),
        ),
        migrations.AlterField(
            model_name='usertest',
            name='user_lesson',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_test', to='core.userlesson', verbose_name='User lesson'),
        ),
        migrations.AlterField(
            model_name='usertext',
            name='text',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_text', to='core.text', verbose_name='Text'),
        ),
        migrations.AlterField(
            model_name='usertext',
            name='user_lesson',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_text', to='core.userlesson', verbose_name='User lesson'),
        ),
        migrations.AlterField(
            model_name='uservideo',
            name='user_lesson',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_video', to='core.userlesson', verbose_name='User lesson'),
        ),
        migrations.AlterField(
            model_name='uservideo',
            name='video',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_video', to='core.video', verbose_name='Video'),
        ),
    ]
