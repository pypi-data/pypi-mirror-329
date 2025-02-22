from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm

from crimsonslate_portfolio.models import Media


class PortfolioAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for name in self.fields:
            self.fields[name].widget.attrs.update(
                {"class": "p-2 rounded bg-white", "placeholder": name.title()}
            )


class MediaCreateForm(ModelForm):
    class Meta:
        model = Media
        fields = [
            "source",
            "thumb",
            "title",
            "subtitle",
            "desc",
            "is_hidden",
            "tags",
            "date_created",
        ]


class MediaUpdateForm(ModelForm):
    class Meta:
        model = Media
        fields = [
            "source",
            "thumb",
            "title",
            "subtitle",
            "desc",
            "is_hidden",
            "tags",
            "date_created",
        ]
