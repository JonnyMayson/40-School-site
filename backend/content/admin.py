from django.contrib import admin
from django.utils.html import format_html
from .models import PhotoBlock, HeroBlock, PrincipleBlock, TeamMember, TeamCategory, NewsArticle

@admin.register(PhotoBlock)
class PhotoBlockAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'preview_image')
    list_editable = ('order',)
    readonly_fields = ('preview_image',)

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;"/>', obj.image.url)
        return "-"

@admin.register(HeroBlock)
class HeroBlockAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'preview_image')
    list_editable = ('is_active',)
    readonly_fields = ('preview_image',)

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;"/>', obj.image.url)
        return "-"

@admin.register(PrincipleBlock)
class PrincipleBlockAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'icon')
    list_editable = ('order',)

@admin.register(TeamCategory)
class TeamCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'preview_image')
    list_editable = ('order',)
    readonly_fields = ('preview_image',)

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;"/>', obj.image.url)
        return "-"

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'category', 'order')
    list_filter = ('category',)
    search_fields = ('name', 'position')

@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish_date', 'subtitle', 'is_published')
    list_filter = ('is_published', 'publish_date')
    search_fields = ('title', 'short_description')
    readonly_fields = ('preview_image',)

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;"/>', obj.image.url)
