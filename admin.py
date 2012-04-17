from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


# Let's say you have Staffers who are in your system, but can only edit their
# own profile... But NOT all of it. This snippet here does that by extending
# the UserAdmin class from Django and removing any sensitive fields from the
# fieldsets.
class MyUserAdmin(UserAdmin):

    def get_fieldsets(self, request, obj=None):
        """
        Determine what fieldsets show up, this is what really limits the form for
        users of only staff status.
        """
        if not obj:
            return self.add_fieldsets

        if not request.user.is_superuser:
            self.fieldsets = (
                (None, {'fields': ('username', 'password')}),
                ('Personal infos', {'fields': ('first_name', 'last_name', 'email')}),
                ('Permissions', {'fields': ('is_active',)}),
            )

        return super(MyUserAdmin, self).get_fieldsets(request, obj)

    def queryset(self, request):
        """
        We only want these users to be able to edit themselves, NOT any other 
        users.
        """
        qs = super(MyUserAdmin, self).queryset(request)

        if request.user.is_superuser:
            return qs

        return qs.filter(pk=request.user.id)


# Now, we need to UNregister the current User admin (otherwise Django gets mad)
# and then re-register it with our custom ModelAdmin which extends the original.
admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)