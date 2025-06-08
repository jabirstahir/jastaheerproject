from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView, LoginView
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from .views import CustomPasswordResetView

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('news/<slug:slug>/', views.news_detail, name='news_detail'),

    # Blog
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/new/', views.create_post, name='create_post'),
    path('blog/edit/<int:post_id>/', views.update_post, name='update_post'),
    path('blog/delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('blog/<int:post_id>/', views.blog_detail, name='blog_detail'),
    path('blog/<int:post_id>/like/', views.like_post, name='like_post'),
    path('blog/<int:post_id>/comment/', views.add_comment, name='add_comment'),

    # Auth
    path('signup/', views.signup_view, name='signup'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    # Password Reset
    path('password-reset/', auth_views.PasswordResetView.as_view(
    template_name='registration/password_reset.html',
    email_template_name='registration/password_reset_email.html'
    ), name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),

    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name="registration/password_reset_confirm.html"
    ), name="password_reset_confirm"),

    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(
        template_name="registration/password_reset_complete.html"
    ), name="password_reset_complete"),

    #services
    path('services/software-development/', views.software_development, name='software_development'),
    path('services/website-development/', views.website_development, name='website_development'),
    path('services/mobile-app-development/', views.mobile_app_development, name='mobile_app_development'),
    path('services/ui-ux-design/', views.ui_ux_design, name='ui_ux_design'),
    path('services/<slug:slug>/', views.service_detail, name='service_detail'),
    # terms and privacy
    path('terms/', TemplateView.as_view(template_name='legal/terms.html'), name='terms'),
    path('privacy/', TemplateView.as_view(template_name='legal/privacy.html'), name='privacy'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)