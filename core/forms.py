from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Patient, VitalSigns, LabResult, Imaging, NIHSSScore, Consultation

class UserRegistrationForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES)
    phone = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role', 'phone']

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'age', 'sex', 'chief_complaint', 'medical_history']
        widgets = {
            'chief_complaint': forms.Textarea(attrs={'rows': 3}),
            'medical_history': forms.Textarea(attrs={'rows': 3}),
        }

class PatientRegistrationForm(forms.Form):
    # Patient Information
    name = forms.CharField(max_length=255)
    age = forms.IntegerField(min_value=0, max_value=150)
    sex = forms.ChoiceField(choices=Patient.GENDER_CHOICES)
    chief_complaint = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    medical_history = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    
    # Vital Signs
    blood_pressure_systolic = forms.IntegerField(label='Systolic BP (mmHg)', min_value=0, max_value=300)
    blood_pressure_diastolic = forms.IntegerField(label='Diastolic BP (mmHg)', min_value=0, max_value=200)
    heart_rate = forms.IntegerField(label='Heart Rate (bpm)', min_value=0, max_value=300)
    respiratory_rate = forms.IntegerField(label='Respiratory Rate (breaths/min)', min_value=0, max_value=100)
    oxygen_saturation = forms.IntegerField(label='O2 Saturation (%)', min_value=0, max_value=100)
    
    # Lab Results
    cbc_wbc = forms.DecimalField(label='WBC Count (K/µL)', max_digits=5, decimal_places=2, required=False)
    cbc_hgb = forms.DecimalField(label='Hemoglobin (g/dL)', max_digits=5, decimal_places=2, required=False)
    cbc_plt = forms.DecimalField(label='Platelet Count (K/µL)', max_digits=6, decimal_places=2, required=False)
    bmp_sodium = forms.IntegerField(label='Sodium (mEq/L)', required=False)
    bmp_potassium = forms.DecimalField(label='Potassium (mEq/L)', max_digits=3, decimal_places=1, required=False)
    bmp_creatinine = forms.DecimalField(label='Creatinine (mg/dL)', max_digits=4, decimal_places=2, required=False)
    bmp_glucose = forms.IntegerField(label='Glucose (mg/dL)', required=False)

class VitalSignsForm(forms.ModelForm):
    class Meta:
        model = VitalSigns
        fields = ['blood_pressure_systolic', 'blood_pressure_diastolic', 'heart_rate', 
                'respiratory_rate', 'oxygen_saturation']
        labels = {
            'blood_pressure_systolic': 'Systolic BP (mmHg)',
            'blood_pressure_diastolic': 'Diastolic BP (mmHg)',
            'heart_rate': 'Heart Rate (bpm)',
            'respiratory_rate': 'Respiratory Rate (breaths/min)',
            'oxygen_saturation': 'O2 Saturation (%)',
        }

class LabResultForm(forms.ModelForm):
    class Meta:
        model = LabResult
        fields = ['test_name', 'result_value', 'unit', 'reference_range']

class ImagingForm(forms.ModelForm):
    class Meta:
        model = Imaging
        fields = ['study_type', 'findings', 'image_url']
        widgets = {
            'findings': forms.Textarea(attrs={'rows': 3}),
        }

class NIHSSScoreForm(forms.ModelForm):
    class Meta:
        model = NIHSSScore
        fields = ['score', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ['diagnosis', 'treatment_plan', 'additional_orders']
        widgets = {
            'diagnosis': forms.Textarea(attrs={'rows': 3}),
            'treatment_plan': forms.Textarea(attrs={'rows': 3}),
            'additional_orders': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter additional orders (medications, tests, imaging studies)'}),
        }
