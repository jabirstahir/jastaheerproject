from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .forms import ContactForm, BlogPostForm, CommentForm, CustomUserCreationForm, ProfileForm
from .models import Post, News, Like, Profile, Service, Director, StaffMember
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.utils.timezone import now
from django.urls import reverse_lazy
from datetime import datetime
from django.template.loader import render_to_string



class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset.html'
    email_template_name = 'registration/password_reset_email.txt' # fallback
    html_email_template_name = 'registration/password_reset_email.html' # your HTML file
    subject_template_name = 'registration/password_reset_subject.txt'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_year'] = datetime.now().year
        return context


def home(request):
    services = Service.objects.all()
    features = [
        {"name": "24/7 Support", "icon": "https://img.icons8.com/ios-filled/50/headset.png", "description": "We provide round-the-clock assistance to ensure your systems run smoothly."},
        {"name": "Scalable Solutions", "icon": "https://img.icons8.com/ios-filled/50/expand.png", "description": "Our services grow with your business, no matter the size."},
        {"name": "Experienced Team", "icon": "https://img.icons8.com/ios-filled/50/teamwork.png", "description": "Our developers, designers, and strategists bring years of experience."},
        {"name": "Client-Centric Approach", "icon": "https://img.icons8.com/ios-filled/50/handshake.png", "description": "We focus on your goals to build solutions that drive results."},
    ]
    directors = Director.objects.all()
    staff_members = StaffMember.objects.all()
    news_feed = News.objects.all().order_by('-created_at')[:3]

    return render(request, 'index.html', {
        'services': services,
        'features': features,
        'directors': directors,
        'staff_members': staff_members,
        'news_feed': news_feed,
    })
#services details
def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug)
    return render(request, 'services/service_detail.html', {'service': service})

def software_development(request):
    return render(request, 'services/software_development.html')

def website_development(request):
    return render(request, 'services/website_development.html')

def mobile_app_development(request):
    return render(request, 'services/mobile_app_development.html')

def ui_ux_design(request):
    return render(request, 'services/ui_ux_design.html')

def services(request):
    return render(request, 'services.html')

def portfolio(request):
    return render(request, 'portfolio.html')

def about(request):
    return render(request, 'about.html')

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully.")
            return redirect('contact')
    else: form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def news_detail(request, slug):
    news = get_object_or_404(News, slug=slug)
    return render(request, 'news_detail.html', {'news': news})

@login_required
@user_passes_test(lambda u: u.is_staff)
def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid(): post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('blog_list')
    else: form = BlogPostForm()
    return render(request, 'blog/create_post.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_staff)
def update_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog_list')
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'blog/create_post.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect('blog_list')

def blog_list(request):
    blog_posts = Post.objects.order_by('-created_at')

    login_form = AuthenticationForm()
    signup_form = CustomUserCreationForm()

    # Handle Login submission
    if request.method == 'POST' and 'login_submit' in request.POST:
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            auth_login(request, user)
            return redirect('blog_list')

    # Handle Signup submission
    elif request.method == 'POST' and 'signup_submit' in request.POST:
        signup_form = CustomUserCreationForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            auth_login(request, user)
            return redirect('blog_list')

    return render(request, 'blog/blog_list.html', {
        'blog_posts': blog_posts,
        'login_form': login_form,
        'signup_form': signup_form,
    })

def blog_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.order_by('-created_at')
    has_liked = request.user.is_authenticated and Like.objects.filter(post=post, user=request.user).exists()
    comment_form = CommentForm()
    context = { 'post': post, 'comments': comments, 'comment_form': comment_form, 'has_liked': has_liked, 'total_likes': post.total_likes()}
    return render(request, 'blog_detail.html', context)

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    existing_like = Like.objects.filter(post=post, user=request.user)
    if existing_like.exists(): existing_like.delete()
    else: Like.objects.create(post=post, user=request.user)
    return redirect('blog_detail', post_id=post.id)



@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
    return redirect('blog_detail', post_id=post.id)

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account was created successfully. Please log in.")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def profile_view(request):
    user = request.user
    context = {
        'post_count': user.blog_posts.count(),
        'comment_count': user.comments.count(),
        'like_count': user.likes.count(),
        'posts': user.blog_posts.all(), # Optional: list of the user’s posts
    }
    return render(request, 'profile.html', context)

@login_required
def edit_profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('edit_profile') # or any success page
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form})