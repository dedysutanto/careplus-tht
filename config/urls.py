from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.contrib import admin
from django.conf import settings
from invoice.views import print_invoice, html_invoice
import os.path

from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from django.views.generic.base import RedirectView


urlpatterns = [
    path('django-admin/', admin.site.urls),

    path('login/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('', RedirectView.as_view(url='/login/')),
    path('invoice/print/<str:invoice_number>/', print_invoice, name='print-invoice'),
    path('invoice/view/<str:invoice_number>/', html_invoice, name='html-invoice'),

    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's serving mechanism
    re_path(r'', include(wagtail_urls)),
]


if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns() # tell gunicorn where static files are in dev mode
    urlpatterns += static(settings.MEDIA_URL + 'images/', document_root=os.path.join(settings.MEDIA_ROOT, 'images'))
    urlpatterns += [
        path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'myapp/images/favicon.ico'))
    ]