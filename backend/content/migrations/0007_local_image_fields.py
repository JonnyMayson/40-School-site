from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0006_alter_heroblock_image_alter_newsarticle_card_image_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="heroblock",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="hero/",
                verbose_name="Басты сурет / Главное изображение",
            ),
        ),
        migrations.AlterField(
            model_name="newsarticle",
            name="card_image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="news_images/",
                verbose_name="Карточка суреті (Card Image)",
            ),
        ),
        migrations.AlterField(
            model_name="photoblock",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="blocks/",
                verbose_name="Сурет / Изображение",
            ),
        ),
        migrations.AlterField(
            model_name="teamcategory",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="team_categories/",
                verbose_name="Сурет / Изображение",
            ),
        ),
        migrations.AlterField(
            model_name="teammember",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="team/",
                verbose_name="Фото",
            ),
        ),
    ]
