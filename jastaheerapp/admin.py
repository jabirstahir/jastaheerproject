from django.contrib import admin
from .models import ContactMessage, News, Post, Comment, Service, Director, StaffMember


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Service)
admin.site.register(Director)
admin.site.register(StaffMember)

# Customized admin for ContactMessage
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'submitted_at')
    list_filter = ('submitted_at',)
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'subject', 'message', 'submitted_at')

    def has_add_permission(self, request):
        return False # Prevent adding new messages manually

    def has_change_permission(self, request, obj=None):
        return False # Prevent editing messages

# Customized admin for News
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'summary')
    list_filter = ('created_at',)
    prepopulated_fields = {'slug': ('title',)} # Auto-generate slug from title
    date_hierarchy = 'created_at' # Adds a date-based drilldown navigation