# Django OIDC Addmin

`django-oidc-admin` is a Django app that adds a custom login button to the Django admin login page using `django-mozilla-oidc`.
It does not allow direct authentication on the first SSO login but instead creates an **inactive user**.
The administrator must activate the user in the Django admin interface.

After activation, the user can log in using the SSO login button.

## Quick Start

1. Add `django_oidc_admin"` to your `INSTALLED_APPS` setting.  
   It must be **before** `"django.contrib.admin"`.

   ```python
   INSTALLED_APPS = [
       ...,
       "django_oidc_admin",
       "django.contrib.admin",
       ...,
   ]
   ```

2. Add the following settings to your `settings.py` file:

   ```python

   # Required settings
   AUTHENTICATION_BACKENDS = (
       "django_oidc_admin.authentication.DjangoOIDCAdminBackend",  # Authentication OIDC
       "django.contrib.auth.backends.ModelBackend",  # Classic authentication
   )

   # Add the admin_navbar context processor to templates settings
   TEMPLATES = [
       {
           "DIRS": [],
           "APP_DIRS": True,
           "OPTIONS": {
               "context_processors": [
                   "django_oidc_admin.context_processors.admin_navbar",
               ],
           },
       },
   ]

   # Mozilla Django OIDC mandatory settings
   OIDC_RP_CLIENT_ID = os.environ["OIDC_RP_CLIENT_ID"]
   OIDC_RP_CLIENT_SECRET = os.environ["OIDC_RP_CLIENT_SECRET"]
   OIDC_RP_SCOPES = "openid email profile"
   OIDC_OP_AUTHORIZATION_ENDPOINT = os.environ["OIDC_OP_AUTHORIZATION_ENDPOINT"]
   OIDC_OP_TOKEN_ENDPOINT = os.environ["OIDC_OP_TOKEN_ENDPOINT"]
   OIDC_OP_USER_ENDPOINT = os.environ["OIDC_OP_USER_ENDPOINT"]
   OIDC_OP_JWKS_ENDPOINT = os.environ["OIDC_OP_JWKS_ENDPOINT"]
   OIDC_RP_SIGN_ALGO = os.environ.get("OIDC_RP_SIGN_ALGO", "RS256")
   
   # Not mandatory, but if needed, to add the user in a group (group will be created if not existing)
   DOIDCADMIN_NEW_USER_GROUP_NAME = "users"
   # Custom settings
   LOGIN_REDIRECT_URL = "admin:index"
   # The login will fail as the user is not automatically set to active, we need to redirect to the admin.
   LOGIN_REDIRECT_URL_FAILURE = "admin:index" 

   # Override the OIDC callback class to use the custom one
   OIDC_CALLBACK_CLASS = "django_oidc_admin.authentication.DjangoOIDCAdminCallbackView"
   ```

3. Include the app's URL configuration in `urls.py`:

   ```python
   from django.urls import path, include

   urlpatterns = [
       path("oidc/", include("django_oidc_admin.urls")),
   ]
   ```

4. Start the development server and visit the admin login page to test the SSO login button.

## License
See the [LICENSE](LICENSE) file for license rights and limitations (MIT).
