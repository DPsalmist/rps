from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('accounts.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('rps/', include('console.urls')),
    path('wallet/', include('wallet.urls')),
    path('subscription/', include('subscription.urls')),

    path('password-reset/', 
        auth_views.PasswordResetView.as_view(template_name=
            'forget_password.html'), name='password-reset'),
    path('password-reset/done/', 
        auth_views.PasswordResetDoneView.as_view(template_name=
            'password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>', 
        auth_views.PasswordResetConfirmView.as_view(template_name=
            'password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name=
            'password_reset_complete.html'), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

