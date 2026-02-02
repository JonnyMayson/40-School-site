from django.shortcuts import render, get_object_or_404
from .models import PhotoBlock, HeroBlock, PrincipleBlock, TeamCategory, TeamMember, NewsArticle

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
