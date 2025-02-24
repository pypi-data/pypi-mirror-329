
# django-drf-blog-api


django-drf-blog-api is a Django blog API app



## Quick start


1. Add "Coy" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...,
        "django-drf-coy-apis",
    ]
```
2. Include the polls URLconf in your project urls.py like this::

    path("coy/", include("django-drf-coy-apis.urls")),

3. Run ``python manage.py migrate`` to create the models.

4. Start the development server and visit the admin to create a poll.
