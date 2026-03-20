import json
from .models import SiteSettings, SectionOrder, ElementStyle


def site_settings(request):
    """Inject SiteSettings, section orders, and element styles into every template context."""
    try:
        settings = SiteSettings.get()
    except Exception:
        settings = None

    try:
        section_orders = json.dumps(SectionOrder.get_ordered())
    except Exception:
        section_orders = '[]'

    try:
        element_styles = json.dumps(ElementStyle.get_all_dict())
    except Exception:
        element_styles = '{}'

    return {
        'site_settings': settings,
        'section_orders': section_orders,
        'element_styles': element_styles,
    }
