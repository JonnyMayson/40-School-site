from .models import SiteSettings


def site_settings(request):
    """Inject SiteSettings into every template context."""
    try:
        return {'site_settings': SiteSettings.get()}
    except Exception:
        return {'site_settings': None}
