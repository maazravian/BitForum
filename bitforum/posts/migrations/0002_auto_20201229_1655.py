# Generated by Django 3.1.4 on 2020-12-29 11:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='upvote',
            name='userId',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='upvote', to='posts.user'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.CreateModel(
            name='Followings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followingId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to='posts.user')),
                ('topicId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topic', to='posts.topic')),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='posts.user')),
            ],
        ),
        migrations.CreateModel(
            name='Followers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followerId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to='posts.user')),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='currentUser', to='posts.user')),
            ],
        ),
        migrations.CreateModel(
            name='Downvote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='downvote', to='posts.post')),
                ('userId', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='downvote', to='posts.user')),
            ],
        ),
    ]