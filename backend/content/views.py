from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.admin.views.decorators import staff_member_required
from .models import PhotoBlock, HeroBlock, PrincipleBlock, TeamCategory, TeamMember, NewsArticle, SiteSettings

ALLOWED_MODELS = {
    'heroblock': (HeroBlock, ['image']),
    'photoblock': (PhotoBlock, ['image']),
    'teamcategory': (TeamCategory, ['image']),
    'teammember': (TeamMember, ['image']),
    'newsarticle': (NewsArticle, ['card_image']),
}

ALLOWED_TEXT_FIELDS = {
    'heroblock':    (HeroBlock,    ['title', 'description']),
    'photoblock':   (PhotoBlock,   ['title', 'description', 'tag', 'order']),
    'teamcategory': (TeamCategory, ['title', 'description', 'order']),
    'teammember':   (TeamMember,   ['name', 'position', 'description', 'order']),
    'principleblock': (PrincipleBlock, ['title', 'description', 'order']),
    'newsarticle':  (NewsArticle,  ['title', 'subtitle', 'short_description', 'full_content']),
}

@staff_member_required
@require_POST
def update_image_url(request):
    model_name = request.POST.get('model', '').lower()
    object_id  = request.POST.get('object_id')
    field_name = request.POST.get('field')
    url        = request.POST.get('url', '').strip()

    if model_name not in ALLOWED_MODELS:
        return JsonResponse({'error': 'Unknown model'}, status=400)

    model_class, allowed_fields = ALLOWED_MODELS[model_name]
    if field_name not in allowed_fields:
        return JsonResponse({'error': 'Field not allowed'}, status=400)

    if not url.startswith('http'):
        return JsonResponse({'error': 'Invalid URL'}, status=400)

    try:
        obj = model_class.objects.get(pk=object_id)
        setattr(obj, field_name, url)
        obj.save(update_fields=[field_name])
        return JsonResponse({'success': True, 'url': url})
    except model_class.DoesNotExist:
        return JsonResponse({'error': 'Object not found'}, status=404)

@staff_member_required
@require_POST
def create_hero_block(request):
    """Create a new HeroBlock with the given image URL (used when no hero exists)."""
    url = request.POST.get('url', '').strip()
    if not url.startswith('http'):
        return JsonResponse({'error': 'Invalid URL'}, status=400)
    hero = HeroBlock.objects.create(image=url, is_active=True)
    return JsonResponse({'success': True, 'id': hero.id, 'url': url})

@staff_member_required
@require_POST
def clear_image_url(request):
    """Clear the image URL for a model field (set to empty string)."""
    model_name = request.POST.get('model', '').lower()
    object_id  = request.POST.get('object_id')
    field_name = request.POST.get('field')

    if model_name not in ALLOWED_MODELS:
        return JsonResponse({'error': 'Unknown model'}, status=400)

    model_class, allowed_fields = ALLOWED_MODELS[model_name]
    if field_name not in allowed_fields:
        return JsonResponse({'error': 'Field not allowed'}, status=400)

    try:
        obj = model_class.objects.get(pk=object_id)
        setattr(obj, field_name, '')
        obj.save(update_fields=[field_name])
        return JsonResponse({'success': True})
    except model_class.DoesNotExist:
        return JsonResponse({'error': 'Object not found'}, status=404)


@staff_member_required
@require_POST
def update_text(request):
    """Update a text field for any allowed model."""
    model_name = request.POST.get('model', '').lower()
    object_id  = request.POST.get('object_id')
    field_name = request.POST.get('field')
    value      = request.POST.get('value', '').strip()

    if model_name not in ALLOWED_TEXT_FIELDS:
        return JsonResponse({'error': 'Unknown model'}, status=400)

    model_class, allowed_fields = ALLOWED_TEXT_FIELDS[model_name]
    if field_name not in allowed_fields:
        return JsonResponse({'error': 'Field not allowed'}, status=400)

    try:
        obj = model_class.objects.get(pk=object_id)
        setattr(obj, field_name, value)
        obj.save(update_fields=[field_name])
        return JsonResponse({'success': True})
    except model_class.DoesNotExist:
        return JsonResponse({'error': 'Object not found'}, status=404)


@staff_member_required
@require_POST
def update_site_settings(request):
    """Update global site colors."""
    settings = SiteSettings.get()
    for field in ['primary_color', 'accent_color', 'footer_color']:
        val = request.POST.get(field, '').strip()
        if val and val.startswith('#') and len(val) in (4, 7):
            setattr(settings, field, val)
    settings.save()
    return JsonResponse({'success': True})

def index(request):
    blocks = PhotoBlock.objects.all().order_by('order')
    hero_block = HeroBlock.objects.filter(is_active=True).first()
    principles = PrincipleBlock.objects.all().order_by('order')
    team_categories = TeamCategory.objects.all().order_by('order')
    site_settings = SiteSettings.get()

    return render(request, 'index.html', {
        'blocks': blocks,
        'hero_block': hero_block,
        'principles': principles,
        'team_categories': team_categories,
        'site_settings': site_settings,
    })

def team_detail(request, category_id):
    category = get_object_or_404(TeamCategory, id=category_id)
    members = category.members.all().order_by('order')
    
    return render(request, 'team_detail.html', {
        'category': category,
        'members': members,
    })

def news_list(request):
    news_items = NewsArticle.objects.filter(is_published=True).order_by('-publish_date')
    return render(request, 'news_list.html', {'news_items': news_items})

def news_detail(request, news_id):
    news_item = get_object_or_404(NewsArticle, id=news_id)
    return render(request, 'news_detail.html', {'news_item': news_item})
