from typing import Any

from django.template import Library

from crimsonslate_portfolio.models import Media

register = Library()


@register.inclusion_tag("portfolio/media/display.html")
def display(
    media: Media, force_image: bool = False, css_class: str | None = None
) -> dict[str, Any]:
    return {
        "title": media.title,
        "class": css_class,
        "image": force_image if force_image else media.is_image,
        "src": media.source.url,
        "detail_url": media.get_absolute_url(),
    }
