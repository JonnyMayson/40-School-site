from django.db import models

class PhotoBlock(models.Model):
    title = models.CharField(max_length=200, verbose_name="Тақырып / Заголовок")
    description = models.TextField(verbose_name="Сипаттама / Описание")
    image = models.ImageField(upload_to='blocks/', verbose_name="Сурет / Изображение")
    tag = models.CharField(max_length=100, blank=True, null=True, verbose_name="Тег / Тэг")
    link = models.URLField(blank=True, null=True, verbose_name="Сілтеме / Ссылка")
    order = models.IntegerField(default=0, verbose_name="Реттік нөмірі / Порядок")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Фото блок (Проект)"
        verbose_name_plural = "Проекты (Слайдер)"
        ordering = ['order']

class HeroBlock(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True, verbose_name="Тақырып / Заголовок (опционально)")
    description = models.TextField(blank=True, null=True, verbose_name="Сипаттама / Описание (опционально)")
    image = models.ImageField(upload_to='hero/', verbose_name="Басты сурет / Главное изображение")
    is_active = models.BooleanField(default=False, verbose_name="Белсенді / Активен")

    def __str__(self):
        return self.title or "Hero Block"

    class Meta:
        verbose_name = "Басты экран (Hero)"
        verbose_name_plural = "Басты экрандар"

class PrincipleBlock(models.Model):
    title = models.CharField(max_length=200, verbose_name="Тақырып / Заголовок")
    description = models.TextField(verbose_name="Сипаттама / Описание")
    icon = models.CharField(max_length=50, default="fas fa-star", help_text="FontAwesome class (e.g., 'fas fa-heart')", verbose_name="Иконка (FontAwesome)")
    order = models.IntegerField(default=0, verbose_name="Реттік нөмірі / Порядок")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Қағида (Принцип)"
        verbose_name_plural = "Қағидалар (Принципы)"
        ordering = ['order']

class TeamCategory(models.Model):
    title = models.CharField(max_length=200, verbose_name="Команда аты / Название команды")
    image = models.ImageField(upload_to='team_categories/', verbose_name="Сурет / Изображение", blank=True, null=True)
    description = models.TextField(verbose_name="Сипаттама / Описание", blank=True, null=True)
    order = models.IntegerField(default=0, verbose_name="Реттік нөмірі / Порядок")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Команда категориясы"
        verbose_name_plural = "Команда категориялары"
        ordering = ['order']

class TeamMember(models.Model):
    category = models.ForeignKey(TeamCategory, on_delete=models.CASCADE, related_name='members', verbose_name="Категория", null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name="Аты-жөні / ФИО")
    position = models.CharField(max_length=100, verbose_name="Лауазымы / Должность")
    description = models.TextField(verbose_name="Сипаттама / Описание", blank=True, null=True)
    image = models.ImageField(upload_to='team/', verbose_name="Фото")
    order = models.IntegerField(default=0, verbose_name="Реттік нөмірі / Порядок")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Команда мүшесі"
        verbose_name_plural = "Команда мүшелері"
        ordering = ['order']

from django.utils import timezone

class NewsArticle(models.Model):
    title = models.CharField(max_length=200, verbose_name="Тақырып (Title)")
    subtitle = models.CharField(max_length=100, verbose_name="Подзаголовок/Тег (Subtitle/Tag)", help_text="Мысалы: #Мақала")
    short_description = models.TextField(verbose_name="Қысқаша сипаттама (Short Description)", help_text="Карточкада көрсетілетін қысқа мәтін")
    card_image = models.ImageField(upload_to='news_images/', verbose_name="Карточка суреті (Card Image)")
    publish_date = models.DateField(default=timezone.now, verbose_name="Жарияланған күні (Publish Date)")
    full_content = models.TextField(verbose_name="Толық мазмұны (Full Content)", help_text="Мақаланың негізгі мәтіні")
    is_published = models.BooleanField(default=True, verbose_name="Жариялау (Is Published)")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Жаңалық (News)"
        verbose_name_plural = "Жаңалықтар (News)"
        ordering = ['-publish_date']
