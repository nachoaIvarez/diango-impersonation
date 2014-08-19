from django import template
from django.conf import settings
from django.core.urlresolvers import reverse

register = template.Library()


@register.simple_tag
def impersonate_url(pk):
    model = getattr(settings, "IMPERSONABLE_MODEL", "user")
    return reverse('impersonate_user', kwargs={'pk': pk,
                                               'user_model': model})
