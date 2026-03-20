import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.admin.views.decorators import staff_member_required
from .models import (
    PhotoBlock, HeroBlock, PrincipleBlock, TeamCategory, TeamMember,
    NewsArticle, SiteSettings, SectionOrder, ElementStyle
)

ALLOWED_MODELS = {
    'heroblock': (HeroBlock, ['image']),
    'photoblock': (PhotoBlock, ['image']),
    'teamcategory': (TeamCategory, ['image']),
    'teammember': (TeamMember, ['image']),
    'newsarticle': (NewsArticle, ['card_image']),
}

ALLOWED_TEXT_FIELDS = {
    'heroblock':      (HeroBlock,       ['title', 'description']),
    'photoblock':     (PhotoBlock,      ['title', 'description', 'tag', 'order']),
    'teamcategory':   (TeamCategory,    ['title', 'description', 'order']),
    'teammember':     (TeamMember,      ['name', 'position', 'description', 'order']),
    'principleblock': (PrincipleBlock,  ['title', 'description', 'order']),
    'newsarticle':    (NewsArticle,     ['title', 'subtitle', 'short_description', 'full_content']),
}

CREATABLE_MODELS = {
    'principleblock': PrincipleBlock,
    'photoblock':     PhotoBlock,
    'teamcategory':   TeamCategory,
}

DELETABLE_MODELS = {
    'principleblock': PrincipleBlock,
    'photoblock':     PhotoBlock,
    'teamcategory':   TeamCategory,
    'teammember':     TeamMember,
}

# ── Existing endpoints ─────────────────────────────────────────────────

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
    url = request.POST.get('url', '').strip()
    if not url.startswith('http'):
        return JsonResponse({'error': 'Invalid URL'}, status=400)
    hero = HeroBlock.objects.create(image=url, is_active=True)
    return JsonResponse({'success': True, 'id': hero.id, 'url': url})


@staff_member_required
@require_POST
def clear_image_url(request):
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
    settings = SiteSettings.get()
    for field in ['primary_color', 'accent_color', 'footer_color']:
        val = request.POST.get(field, '').strip()
        if val and val.startswith('#') and len(val) in (4, 7):
            setattr(settings, field, val)
    settings.save()
    return JsonResponse({'success': True})


# ── NEW: Section ordering ──────────────────────────────────────────────

@staff_member_required
@require_POST
def update_section_order(request):
    """Save section order. Expects JSON body: {sections: [{key, order}, ...]}"""
    try:
        data = json.loads(request.body)
        sections = data.get('sections', [])
        for s in sections:
            SectionOrder.objects.update_or_create(
                section_key=s['key'],
                defaults={'order': s['order']}
            )
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@staff_member_required
@require_POST
def update_section_bg(request):
    """Update background color for a section."""
    key = request.POST.get('section_key', '').strip()
    bg = request.POST.get('bg_color', '').strip()
    if not key:
        return JsonResponse({'error': 'Missing section_key'}, status=400)
    obj, _ = SectionOrder.objects.get_or_create(section_key=key)
    obj.bg_color = bg
    obj.save(update_fields=['bg_color'])
    return JsonResponse({'success': True})


@staff_member_required
@require_POST
def toggle_section(request):
    """Toggle visibility of a section."""
    key = request.POST.get('section_key', '').strip()
    if not key:
        return JsonResponse({'error': 'Missing section_key'}, status=400)
    obj, _ = SectionOrder.objects.get_or_create(section_key=key)
    obj.is_visible = not obj.is_visible
    obj.save(update_fields=['is_visible'])
    return JsonResponse({'success': True, 'is_visible': obj.is_visible})


# ── NEW: Element styles ────────────────────────────────────────────────

@staff_member_required
@require_POST
def update_element_style(request):
    """Update per-element CSS. Expects: element_id, color, font_family, font_size, font_weight, bg_color."""
    eid = request.POST.get('element_id', '').strip()
    if not eid:
        return JsonResponse({'error': 'Missing element_id'}, status=400)
    obj, _ = ElementStyle.objects.get_or_create(element_id=eid)
    for field in ['color', 'font_family', 'font_size', 'font_weight', 'bg_color']:
        val = request.POST.get(field)
        if val is not None:
            setattr(obj, field, val.strip())
    obj.save()
    return JsonResponse({'success': True, 'css': obj.to_css()})


# ── NEW: Create / Delete elements ──────────────────────────────────────

@staff_member_required
@require_POST
def create_element(request):
    """Create a new element of given model type."""
    model_name = request.POST.get('model', '').lower()
    if model_name not in CREATABLE_MODELS:
        return JsonResponse({'error': 'Model not creatable'}, status=400)
    model_class = CREATABLE_MODELS[model_name]
    max_order = model_class.objects.count()
    defaults = {'order': max_order}
    if model_name == 'principleblock':
        obj = model_class.objects.create(
            title='Жаңа қағида',
            description='Сипаттама қосыңыз',
            icon='fas fa-star',
            **defaults
        )
    elif model_name == 'photoblock':
        obj = model_class.objects.create(
            title='Жаңа жоба',
            description='Жоба сипаттамасы',
            image='',
            **defaults
        )
    elif model_name == 'teamcategory':
        obj = model_class.objects.create(
            title='Жаңа категория',
            **defaults
        )
    else:
        return JsonResponse({'error': 'Unknown'}, status=400)
    return JsonResponse({'success': True, 'id': obj.id})


@staff_member_required
@require_POST
def delete_element(request):
    """Delete an element by model and id."""
    model_name = request.POST.get('model', '').lower()
    object_id = request.POST.get('object_id')
    if model_name not in DELETABLE_MODELS:
        return JsonResponse({'error': 'Model not deletable'}, status=400)
    model_class = DELETABLE_MODELS[model_name]
    try:
        obj = model_class.objects.get(pk=object_id)
        obj.delete()
        return JsonResponse({'success': True})
    except model_class.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)


# ── Page views ─────────────────────────────────────────────────────────

def index(request):
    blocks = PhotoBlock.objects.all().order_by('order')
    hero_block = HeroBlock.objects.filter(is_active=True).first()
    principles = PrincipleBlock.objects.all().order_by('order')
    team_categories = TeamCategory.objects.all().order_by('order')

    try:
        site_settings = SiteSettings.get()
        section_orders = SectionOrder.get_ordered()
        element_styles = ElementStyle.get_all_dict()
    except Exception:
        site_settings = None
        section_orders = []
        element_styles = {}

    return render(request, 'index.html', {
        'blocks': blocks,
        'hero_block': hero_block,
        'principles': principles,
        'team_categories': team_categories,
        'site_settings': site_settings,
        'section_orders': json.dumps(section_orders),
        'element_styles': json.dumps(element_styles),
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
