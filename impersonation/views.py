from django.views.generic.base import RedirectView
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import load_backend, login
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect
from django.utils.importlib import import_module
from django.utils import six


def _load_module(path):
    """
    Code to load create user module. Copied off django-browserid.
    """

    i = path.rfind('.')
    module, attr = path[:i], path[i + 1:]

    try:
        mod = import_module(module)
    except ImportError:
        raise ImproperlyConfigured('Error importing CAN_IMPERSONATE'
                                   ' function.')
    except ValueError:
        raise ImproperlyConfigured('Error importing CAN_IMPERSONATE'
                                   ' function. Try CAN_IMPERSONATE = '
                                   'lambda request, target_user: '
                                   'request.user.is_staff '
                                   'and not target_user.is_staff')

    try:
        CAN_IMPERSONATE = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured('Module {0} does not define a {1} '
                                   'function.'.format(module, attr))
    return CAN_IMPERSONATE


class ImpersonateView(RedirectView):
    url = getattr(settings,
                  "LOGIN_REDIRECT_URL",
                  "/")

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')

        try:
            from django.db.models.loading import get_model

            # 'accounts.User' -> ['accounts', 'User']
            full_path = kwargs.get('user_model').split('.')

            # 'accounts'
            app_name = full_path[0]

            # 'User'
            model_name = full_path[1]

            model = get_model(app_name, model_name)

        except ImportError:
            from django.contrib.auth import get_user_model

            model = get_user_model()

        user = get_object_or_404(model, pk=pk)

        CAN_IMPERSONATE = getattr(settings,
                                  "CAN_IMPERSONATE",
                                  lambda r, y: r.user.is_superuser)

        if isinstance(CAN_IMPERSONATE, six.string_types):
            CAN_IMPERSONATE = _load_module(CAN_IMPERSONATE)
        elif hasattr(CAN_IMPERSONATE, "__call__"):
            CAN_IMPERSONATE = CAN_IMPERSONATE
        else:
            raise ImproperlyConfigured("The CAN_IMPERSONATE setting is "
                                       "neither a valid module nor callable.")

        if not CAN_IMPERSONATE(request, user):
            messages.error(request, "Permission denied.")
            return redirect(request.META.get("HTTP_REFERER", "/"))

        # Find a suitable backend.
        if not hasattr(user, 'backend'):
            for backend in settings.AUTHENTICATION_BACKENDS:
                if user == load_backend(backend).get_user(pk):
                    user.backend = backend
                    break

        # Log the user in.
        if hasattr(user, 'backend'):
            login(request, user)

        return super(ImpersonateView, self).get(self, request, *args,
                                                **kwargs)
