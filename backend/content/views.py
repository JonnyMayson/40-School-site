from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.admin.views.decorators import staff_member_required
from .models import PhotoBlock, HeroBlock, PrincipleBlock, TeamCategory, TeamMember, NewsArticle

ALLOWED_MODELS = {
    'heroblock': (HeroBlock, ['image']),
    'photoblock': (PhotoBlock, ['image']),
    'teamcategory': (TeamCategory, ['image']),
    'teammember': (TeamMember, ['image']),
    'newsarticle': (NewsArticle, ['card_image']),
}

@staff_member_required
@require_POST
def update_image_url(request):
    model_name = request.POST.get('model', '').lower()
    object_id  = request.POST.get('object_id')
    field_name = request.POST.get('field')
    uploaded_image = request.FILES.get('image')

    if model_name not in ALLOWED_MODELS:
        return JsonResponse({'error': 'Unknown model'}, status=400)

    model_class, allowed_fields = ALLOWED_MODELS[model_name]
    if field_name not in allowed_fields:
        return JsonResponse({'error': 'Field not allowed'}, status=400)

    if not uploaded_image:
        return JsonResponse({'error': 'Image file is required'}, status=400)

    try:
        obj = model_class.objects.get(pk=object_id)
        old_file = getattr(obj, field_name, None)
        old_name = old_file.name if old_file else None

        setattr(obj, field_name, uploaded_image)
        obj.save(update_fields=[field_name])

        new_file = getattr(obj, field_name, None)
        if old_name and new_file and old_name != new_file.name:
            old_file.storage.delete(old_name)

        return JsonResponse({'success': True, 'url': new_file.url if new_file else ''})
    except model_class.DoesNotExist:
        return JsonResponse({'error': 'Object not found'}, status=404)

@staff_member_required
@require_POST
def create_hero_block(request):
    """Create a new HeroBlock with uploaded image (used when no hero exists)."""
    uploaded_image = request.FILES.get('image')
    if not uploaded_image:
        return JsonResponse({'error': 'Image file is required'}, status=400)
    hero = HeroBlock.objects.create(image=uploaded_image, is_active=True)
    return JsonResponse({'success': True, 'id': hero.id, 'url': hero.image.url if hero.image else ''})

@staff_member_required
@require_POST
def clear_image_url(request):
    """Clear image file for a model field."""
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
        old_file = getattr(obj, field_name, None)
        old_name = old_file.name if old_file else None

        setattr(obj, field_name, None)
        obj.save(update_fields=[field_name])

        if old_name and old_file:
            old_file.storage.delete(old_name)

        return JsonResponse({'success': True})
    except model_class.DoesNotExist:
        return JsonResponse({'error': 'Object not found'}, status=404)

def index(request):
    blocks = PhotoBlock.objects.all().order_by('order')  # Fetch all blocks ordered by 'order'
    
    # Get active hero block
    hero_block = HeroBlock.objects.filter(is_active=True).first()
    
    principles = PrincipleBlock.objects.all().order_by('order')
    
    # Fetch categories for the team section
    team_categories = TeamCategory.objects.all().order_by('order')

    return render(request, 'index.html', {
        'blocks': blocks, 
        'hero_block': hero_block,
        'principles': principles,
        'team_categories': team_categories,
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
