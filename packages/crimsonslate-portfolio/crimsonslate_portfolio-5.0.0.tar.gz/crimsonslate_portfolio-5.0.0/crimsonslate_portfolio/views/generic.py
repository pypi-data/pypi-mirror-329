from django.contrib.auth.views import LoginView as LoginViewBase
from django.contrib.auth.views import LogoutView as LogoutViewBase
from django.urls import reverse_lazy

from crimsonslate_portfolio.forms import PortfolioAuthenticationForm
from crimsonslate_portfolio.views.base import HtmxTemplateView, PortfolioProfileMixin


class ContactView(PortfolioProfileMixin, HtmxTemplateView):
    content_type = "text/html"
    extra_context = {"title": "Contact"}
    http_method_names = ["get", "post"]
    partial_template_name = "portfolio/partials/_contact.html"
    template_name = "portfolio/contact.html"


class LoginView(LoginViewBase, HtmxTemplateView):
    content_type = "text/html"
    extra_context = {"title": "Login"}
    form_class = PortfolioAuthenticationForm
    http_method_names = ["get", "post"]
    partial_template_name = "portfolio/partials/_login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy("gallery")
    template_name = "portfolio/login.html"


class LogoutView(LogoutViewBase, HtmxTemplateView):
    content_type = "text/html"
    extra_context = {"title": "Logout"}
    http_method_names = ["get", "post"]
    partial_template_name = "portfolio/partials/_logout.html"
    success_url = reverse_lazy("gallery")
    template_name = "portfolio/logout.html"
