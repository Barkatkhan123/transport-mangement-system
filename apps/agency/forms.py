from django import forms
from .models import Agency, Driver, Bus

INPUT_CLASS = 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent'
SELECT_CLASS = 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white'


class AgencyRegistrationForm(forms.ModelForm):
    class Meta:
        model = Agency
        fields = ['name', 'registration_number', 'email', 'phone', 'address', 'city', 'logo']
        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Agency Name'}),
            'registration_number': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Registration Number'}),
            'email': forms.EmailInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Agency Email'}),
            'phone': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Phone Number'}),
            'address': forms.Textarea(attrs={'class': INPUT_CLASS, 'rows': 3, 'placeholder': 'Full Address'}),
            'city': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'City'}),
            'logo': forms.FileInput(attrs={'class': 'w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100'}),
        }


class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['full_name', 'license_number', 'license_expiry_date', 'phone_number',
                  'photo', 'date_of_birth', 'address', 'experience_years', 'status']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Full Name'}),
            'license_number': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'License Number'}),
            'license_expiry_date': forms.DateInput(attrs={'class': INPUT_CLASS, 'type': 'date'}),
            'phone_number': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Phone Number'}),
            'photo': forms.FileInput(attrs={'class': 'w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-blue-50 file:text-blue-700'}),
            'date_of_birth': forms.DateInput(attrs={'class': INPUT_CLASS, 'type': 'date'}),
            'address': forms.Textarea(attrs={'class': INPUT_CLASS, 'rows': 2, 'placeholder': 'Address'}),
            'experience_years': forms.NumberInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Years of Experience', 'min': 0}),
            'status': forms.Select(attrs={'class': SELECT_CLASS}),
        }


class BusForm(forms.ModelForm):
    wifi = forms.BooleanField(required=False, label='WiFi')
    charging = forms.BooleanField(required=False, label='Charging Ports')
    tv = forms.BooleanField(required=False, label='TV / Entertainment')
    toilet = forms.BooleanField(required=False, label='Toilet')

    class Meta:
        model = Bus
        fields = ['registration_number', 'bus_type', 'total_seats', 'seat_layout',
                  'model_name', 'year_of_manufacture', 'photo', 'status']
        widgets = {
            'registration_number': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'e.g. ABC-123'}),
            'bus_type': forms.Select(attrs={'class': SELECT_CLASS}),
            'total_seats': forms.NumberInput(attrs={'class': INPUT_CLASS, 'placeholder': 'e.g. 40', 'min': 1}),
            'seat_layout': forms.Select(attrs={'class': SELECT_CLASS}),
            'model_name': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Bus Model (optional)'}),
            'year_of_manufacture': forms.NumberInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Year (optional)', 'min': 1990}),
            'photo': forms.FileInput(attrs={'class': 'w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-blue-50 file:text-blue-700'}),
            'status': forms.Select(attrs={'class': SELECT_CLASS}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            amenities = self.instance.amenities or {}
            self.fields['wifi'].initial = amenities.get('wifi', False)
            self.fields['charging'].initial = amenities.get('charging', False)
            self.fields['tv'].initial = amenities.get('tv', False)
            self.fields['toilet'].initial = amenities.get('toilet', False)

    def save(self, commit=True):
        bus = super().save(commit=False)
        bus.amenities = {
            'wifi': self.cleaned_data.get('wifi', False),
            'charging': self.cleaned_data.get('charging', False),
            'tv': self.cleaned_data.get('tv', False),
            'toilet': self.cleaned_data.get('toilet', False),
        }
        if commit:
            bus.save()
        return bus
