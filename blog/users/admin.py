from django.contrib import admin
from django import forms
from .models import CoachNutritionist, Client  # Ensure you import the Client model

# Form for CoachNutritionist with password hashing
class CoachNutriAdminForm(forms.ModelForm):
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput(), required=False)

    class Meta:
        model = CoachNutritionist
        fields = '__all__'

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])  # Hash the password if provided
        if commit:
            user.save()
        return user

class CoachNutriAdmin(admin.ModelAdmin):
    # Display fields with a custom client list and enhanced permissions display
    list_display = ('id', 'username', 'email', 'is_coach', 'is_nutritionist', 'client_list')
    list_filter = ('is_staff', 'is_active', 'is_coach', 'is_nutritionist', 'client_id')  # Enhanced filtering options
    search_fields = ('username', 'email', 'client_id__first_name')  # Search by client first_name too
    filter_horizontal = ('client_id',)  # Improved display for selecting client_id

    # Custom method to list client_id with a tooltip for a better display of associated client_id
    def client_list(self, obj):
        client_id = obj.client_id.all()
        client_names = [client.first_name for client in client_id]
        if len(client_names) > 3:  # Limit the display, show 'and more' if too many client_id
            display_names = ", ".join(client_names[:3]) + " and more..."
        else:
            display_names = ", ".join(client_names)
        return display_names
    client_list.short_description = 'client_id'

    # Organize fields in the form with custom labels and helper text
    fieldsets = (
        (None, {
            'fields': ('email', 'username', 'password', 'photo'),
            'description': "Primary account information for the coach/nutritionist."
        }),
        ('Personal Information', {
            'fields': ('bio', 'certifications', 'client_id'),
            'description': "Provide additional personal details and client associations."
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_coach', 'is_nutritionist'),
            'description': "Define the user's permissions and roles within the platform."
        }),
    )

    # Fields for adding a new user with clearer labels and permissions
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password', 'is_staff', 'is_active', 'is_coach', 'is_nutritionist', 'client_id'),
            'description': "Fill in the basic information and assign client_id if needed."
        }),
    )

    # Custom ordering and CSS classes for better UX
    ordering = ('username',)
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)  # Custom CSS for improved layout and readability
        }


    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['password'].widget.attrs['autocomplete'] = 'new-password'
        return form

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)  # Save the user first
        if form.cleaned_data['password']:  # If a password is provided
            obj.set_password(form.cleaned_data['password'])  # Hash the password
            obj.save()  # Save the user again

# Register the CoachNutritionist model
admin.site.register(CoachNutritionist, CoachNutriAdmin)


# Form for Client with password hashing
class ClientAdminForm(forms.ModelForm):
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput(), required=False)

    class Meta:
        model = Client
        fields = '__all__'

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])  # Hash the password if provided
        if commit:
            user.save()
        return user

class ClientAdmin(admin.ModelAdmin):
    # Title of the model
    fieldsets = (
        (None, {
            'fields': ('email', 'username', 'password')
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'age', 'weight', 'height', 'goal_weight', 'activity_level', 'profile_picture')
        }),
        ('Programs', {
            'fields': ('program_nutrition', 'program_fitness')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_client')
        }),
    )
    list_display = ('username', 'email', 'age', 'weight', 'height', 'goal_weight', 'activity_level', 'is_active','program_fitness','program_nutrition')

    # Allows using the password in plain text in the edit form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password', 'is_active')
        }),
    )

    # For filtering active users
    list_filter = ('is_active',)
    search_fields = ('username', 'email')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['password'].widget.attrs['autocomplete'] = 'new-password'
        return form

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)  # Save the user first
        if form.cleaned_data['password']:  # If a password is provided
            obj.set_password(form.cleaned_data['password'])  # Hash the password
            obj.save()  # Save the user again

# Register the Client model
admin.site.register(Client, ClientAdmin)
