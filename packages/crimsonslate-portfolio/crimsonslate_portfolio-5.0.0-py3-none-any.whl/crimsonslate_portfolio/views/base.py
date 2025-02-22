from typing import Any

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db.models import QuerySet
from django.http import HttpRequest
from django.views.generic import TemplateView
from django.views.generic.base import ContextMixin
from django.views.generic.edit import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin

if not hasattr(settings, "PORTFOLIO_PROFILE"):
    raise ImproperlyConfigured("'PORTFOLIO_PROFILE' setting is required.")


class PortfolioProfileMixin(ContextMixin):
    """Adds :confval:`PORTFOLIO_PROFILE` to the view context."""

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["profile"] = settings.PORTFOLIO_PROFILE
        return context


class HtmxTemplateView(TemplateView):
    """A template view that enables htmx features."""

    content_type = "text/html"
    partial_template_name: str | None = None
    """
    A partial template rendered by htmx.

    :type: :py:obj:`str` | :py:obj:`None`
    :value: :py:obj:`None`

    """

    def setup(self, request: HttpRequest, *args, **kwargs) -> None:
        """
        Sets :py:attr:`template_name` to :py:attr:`partial_template_name` if it is present.

        The request must be an HTMX request and not `boosted`_.

        .. _boosted: https://htmx.org/attributes/hx-boost/
        """
        htmx_request = bool(request.headers.get("HX-Request"))
        boosted = bool(request.headers.get("HX-Boosted"))

        if htmx_request and self.partial_template_name and not boosted:
            self.template_name = self.partial_template_name
        return super().setup(request, *args, **kwargs)


class PortfolioSingleObjectMixin(SingleObjectMixin):
    def get_queryset(self) -> QuerySet:
        queryset = self.queryset.all()

        if self.request.user and self.request.user.is_staff:
            return queryset
        return queryset.exclude(is_hidden=True)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        self.object = self.get_object()
        return super().get_context_data(**kwargs)


class PortfolioMultipleObjectMixin(MultipleObjectMixin):
    def get_queryset(self) -> QuerySet:
        queryset = self.queryset.all()

        if self.request.user and self.request.user.is_staff:
            return queryset
        return queryset.exclude(is_hidden=True)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        self.object_list = self.get_queryset()
        return super().get_context_data(**kwargs)
