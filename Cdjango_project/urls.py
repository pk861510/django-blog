"""
URL configuration for Cdjango_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings # Both for media apeare in profile or anewhere
from django.conf.urls.static import static #
from users import views as user_views
from django.contrib.auth import views as auth_views


urlpatterns = ([
    path('admin/', admin.site.urls),
    path('register/',user_views.register,name='Register'),
    path('profile/', user_views.profile, name='Profile'),
    path("accounts/", include("allauth.urls")),
 
    path('login/',user_views.CustomLoginView.as_view(template_name="users/login.html"),name='Login'),
    path('verify-2fa/', user_views.verify_2fa, name='verify_2fa'),  # 2FA verification
    path('enable-2fa-confirm/', user_views.enable_2fa_confirm, name='enable_2fa_confirm'),

    
    path('logout/', auth_views.LogoutView.as_view(template_name = 'users/logout.html'), name='Logout'),

    path('password-reset/',auth_views.PasswordResetView.as_view(template_name = 'users/password_reset.html'),
         name = 'Password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view
        (template_name = 'users/password_reset_done.html'),
         name = 'password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete',auth_views.PasswordResetCompleteView.as_view
        (template_name = 'users/password_reset_complete.html'),
         name = 'password_reset_complete'),

    path('',include('blog.urls')),#we can access the blog home page by http://127.0.0.1:8000/blog/ if we do not use /blog then it will give 404(remove blog from urls)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
               + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))

# urlpatterns += static(settings.STATIC_URL,document_root= settings.STATIC_ROOT)  # FOR VERSAL STATIC SAME CODE FOR ABOVE .MEDIA_ROOT

# if settings.DEBUG:  #which means we are currently in debug mode
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  #now this should allow aur media to the browser and profile pic apeare