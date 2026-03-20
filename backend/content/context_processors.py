from .models import SiteSettings


def site_settings(request):
    """Inject SiteSettings into every template context."""
    return {'site_settings': SiteSettings.get()}
