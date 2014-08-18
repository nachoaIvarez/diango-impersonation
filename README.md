django-impersonation
==============

About
-----

This is a fork of django-loginas: https://github.com/stochastic-technologies/django-loginas

"Login as this user" for the Django admin.

Installing django-impersonation
-------------------------

* Add `impersonation` to your Python path, or install using pip: `pip install django-impersonation`

* Add the `impersonation` app to your `INSTALLED_APPS`:

```
# settings.py
INSTALLED_APPS = (... 'impersonation', ...)
```

* Add the impersonation URL to your `urls.py`:

```
# urls.py
urlpatterns += patterns('',
                        url(r"^login/(?P<user_model>[\w\.]+)/(?P<pk>\d+)$",
                            ImpersonateView.as_view(),
                            name="impersonate_user"),
)
```

* At this point, the only users who will be able to log in as other users are those with the `is_superuser` permission.
If you use custom User models, and haven't specified that permission, or if you want to change which users are
authorized to log in as others, you can define the `CAN_IMPERSONATE` setting, like so:

```
# If you want to impersonate a custom user model:

```
Define a string with "<name of the app with your custom model>.<name of your custom model>", case sensitive.
    settings.py:
    AUTH_USER_MODEL = 'accounts.CustomUserModel'

Else, don't. It will use django's default 'django.contrib.auth.get_user_model'

```
# Setup
```
settings.py:
This will only allow admins to log in as other users:
    CAN_IMPERSONATE = lambda request, target_user: request.user.is_admin

This will only allow admins to log in as other users, as long as those users are not admins themselves:
    CAN_IMPERSONATE = lambda request, target_user: request.user.is_admin and not target_user.is_admin
```

You'll also need to add the template to it so the button shows up:

```
# admin.py
class YourUserAdmin(ModelAdmin):
    change_form_template = 'impersonation/change_form.html'

admin.site.register(Admin, YourUserAdmin)

```

At this point, you should be good to go. Just visit the Django admin, navigate to a user and you should see the "Log
in as this user" button at the top right of the screen.

License
-------

This software is distributed under the BSD license.
