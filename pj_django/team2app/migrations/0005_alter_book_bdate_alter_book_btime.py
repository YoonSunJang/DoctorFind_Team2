# Generated by Django 4.0.6 on 2022-08-10 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team2app', '0004_book_event_myevent_review_rename_member1_member_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='bdate',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='book',
            name='btime',
            field=models.TextField(),
        ),
    ]
