from django.db import models

class PhotoBlock(models.Model):
    title = models.CharField(max_length=200, verbose_name="Тақырып / Заголовок")
    description = models.TextField(verbose_name="Сипаттама / Описание")
    image = models.URLField(verbose_name="Сурет URL / URL изображения")
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
    image = models.URLField(verbose_name="Басты сурет URL / URL главного изображения")
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
    image = models.URLField(verbose_name="Сурет URL / URL изображения", blank=True, null=True)
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
    image = models.URLField(verbose_name="Фото URL")
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
    card_image = models.URLField(verbose_name="Карточка суреті URL (Card Image URL)")
    publish_date = models.DateField(default=timezone.now, verbose_name="Жарияланған күні (Publish Date)")
    full_content = models.TextField(verbose_name="Толық мазмұны (Full Content)", help_text="Мақаланың негізгі мәтіні")
    is_published = models.BooleanField(default=True, verbose_name="Жариялау (Is Published)")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Жаңалық (News)"
        verbose_name_plural = "Жаңалықтар (News)"
        ordering = ['-publish_date']


class SiteSettings(models.Model):
    primary_color = models.CharField(
        max_length=20, default='#1e7a45',
        verbose_name="Негізгі түс (Primary Color)"
    )
    accent_color = models.CharField(
        max_length=20, default='#2e90fa',
        verbose_name="Акцент түсі (Accent Color)"
    )
    footer_color = models.CharField(
        max_length=20, default='#0f3d23',
        verbose_name="Футер фоны (Footer Color)"
    )

    def __str__(self):
        return "Сайт настройкалары"

    class Meta:
        verbose_name = "Сайт настройкалары"
        verbose_name_plural = "Сайт настройкалары"

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class SectionOrder(models.Model):
    """Stores display order, background color and visibility of each page section."""
    section_key = models.CharField(max_length=50, unique=True)
    order = models.IntegerField(default=0)
    bg_color = models.CharField(max_length=20, blank=True, default='')
    is_visible = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Секция реті"
        verbose_name_plural = "Секция реті"

    def __str__(self):
        return f"{self.section_key} (order={self.order})"

    @classmethod
    def get_ordered(cls):
        """Return dict of section_key -> {order, bg_color, is_visible}."""
        defaults = [
            ('header', -1), ('hero', 0), ('stats', 1), ('principles', 2),
            ('projects', 3), ('team', 4), ('footer', 99),
        ]
        existing = {s.section_key: s for s in cls.objects.all()}
        for key, default_order in defaults:
            if key not in existing:
                cls.objects.create(section_key=key, order=default_order)
        sections = cls.objects.all().order_by('order')
        return list(sections.values('section_key', 'order', 'bg_color', 'is_visible'))


class ElementStyle(models.Model):
    """Stores per-element CSS styles (text color, font, size, weight, bg) and text content."""
    element_id = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=20, blank=True, default='')
    font_family = models.CharField(max_length=100, blank=True, default='')
    font_size = models.CharField(max_length=20, blank=True, default='')
    font_weight = models.CharField(max_length=20, blank=True, default='')
    bg_color = models.CharField(max_length=20, blank=True, default='')
    text_content = models.TextField(blank=True, default='')

    class Meta:
        verbose_name = "Элемент стилі"
        verbose_name_plural = "Элемент стильдері"

    def __str__(self):
        return self.element_id

    def to_css(self):
        """Return inline CSS string."""
        parts = []
        if self.color:
            parts.append(f"color:{self.color}")
        if self.font_family:
            parts.append(f"font-family:'{self.font_family}',sans-serif")
        if self.font_size:
            parts.append(f"font-size:{self.font_size}")
        if self.font_weight:
            parts.append(f"font-weight:{self.font_weight}")
        if self.bg_color:
            parts.append(f"background-color:{self.bg_color}")
        return ';'.join(parts)

    @classmethod
    def get_all_dict(cls):
        """Return dict of element_id -> {css, text}."""
        return {
            e.element_id: {'css': e.to_css(), 'text': e.text_content}
            for e in cls.objects.all()
        }
