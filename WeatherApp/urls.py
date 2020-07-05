from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from weather import urls
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404, handler403


urlpatterns = [
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset/success', auth_views.PasswordResetDoneView.as_view(
        template_name='password_resetsucces.html'), name='password_reset_done'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='password_reset.html'), name='password_reset'),
    path('profile/editing/', user_views.editprofile, name='profile/editing'),
    path('profile/', user_views.profile, name='profile'),
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='loginpage.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logoutpage.html'), name='logout'),
    path('', include('weather.urls'), name='startpage'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)


handler404 = user_views.response_custom404page
handler403 = user_views.response_custom403page
