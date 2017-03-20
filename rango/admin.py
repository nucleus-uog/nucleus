from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from .models import (
    TestCategory,
    Test,
    TestRun,
    TestRunDetail,
    User
)
from .forms import CustomUserChangeForm, CustomUserCreationForm

class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference the removed 'username' field
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('first_name', 'last_name', 'repository_url')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important Dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name', 'repository_url')
    ordering = ('email',)


# We don't have any special configuration for the admin of test categories.
class TestCategoryAdmin(admin.ModelAdmin):
    pass


# We configure the Tests in the Admin Panel so that we can't add them - the
# test runner does this.
class TestAdmin(admin.ModelAdmin):
    readonly_fields=('test', 'case',)

    def has_add_permission(self, request):
            return False

# We configure the Test Run in the Admin Panel so that we can't add them - the
# test runner does this.
class TestRunAdmin(admin.ModelAdmin):
    readonly_fields=('repository_url', 'date_run', 'test_version',
                     'log', 'time_taken', 'status', 'student',)

    def has_add_permission(self, request):
            return False


# We configure the Test Run Detail in the Admin Panel so that we can't add them - the
# test runner does this.
class TestRunDetailAdmin(admin.ModelAdmin):
    readonly_fields=('record', 'test', 'passed', 'log',)

    def has_add_permission(self, request):
            return False


admin.site.register(User, CustomUserAdmin)
admin.site.register(TestCategory, TestCategoryAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(TestRun, TestRunAdmin)
admin.site.register(TestRunDetail, TestRunDetailAdmin)
