from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.utils import timezone
from .models import User, Patient, VitalSigns, LabResult, Imaging, NIHSSScore, Consultation, Alert
from .forms import (
    UserRegistrationForm, UserLoginForm, PatientForm, VitalSignsForm,
    LabResultForm, ImagingForm, NIHSSScoreForm, ConsultationForm,
    PatientRegistrationForm
)

def role_selection(request):
    return render(request, 'core/role_selection.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome {user.username}!')
            if user.is_technician():
                return redirect('core:technician_dashboard')
            else:
                return redirect('core:neurologist_dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'core/register.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('core:login')

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back {user.username}!')
                if user.is_technician():
                    return redirect('core:technician_dashboard')
                else:
                    return redirect('core:neurologist_dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    return render(request, 'core/login.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'core/profile.html')

@login_required
def technician_dashboard(request):
    if not request.user.is_technician():
        raise PermissionDenied
    patients = Patient.objects.filter(created_by=request.user).order_by('-created_at')
    return render(request, 'core/technician_dashboard.html', {'patients': patients})

@login_required
def neurologist_dashboard(request):
    if not request.user.is_neurologist():
        raise PermissionDenied
    
    # Get all patients and those with critical alerts
    patients = Patient.objects.all().order_by('-created_at')
    critical_patients = Patient.objects.filter(has_critical_alert=True).order_by('-updated_at')
    
    # Get today's consultations count
    today = timezone.now().date()
    consultations_today = Consultation.objects.filter(
        created_at__date=today
    ).count()
    
    context = {
        'patients': patients,
        'critical_patients': critical_patients,
        'consultations_today': consultations_today,
    }
    
    return render(request, 'core/neurologist_dashboard.html', context)

@login_required
def patient_list(request):
    if not request.user.is_technician() and not request.user.is_neurologist():
        raise PermissionDenied
    patients = Patient.objects.all()
    return render(request, 'core/patient_list.html', {'patients': patients})

@login_required
def patient_detail(request, patient_id):
    if not request.user.is_technician() and not request.user.is_neurologist():
        raise PermissionDenied
    patient = get_object_or_404(Patient, id=patient_id)
    vitals = VitalSigns.objects.filter(patient=patient).order_by('-timestamp')
    labs = LabResult.objects.filter(patient=patient).order_by('-timestamp')
    imaging = Imaging.objects.filter(patient=patient).order_by('-timestamp')
    nihss = NIHSSScore.objects.filter(patient=patient).order_by('-timestamp')
    consultations = Consultation.objects.filter(patient=patient).order_by('-created_at')
    alerts = Alert.objects.filter(patient=patient, is_active=True).order_by('-created_at')
    
    context = {
        'patient': patient,
        'vitals': vitals,
        'labs': labs,
        'imaging': imaging,
        'nihss': nihss,
        'consultations': consultations,
        'alerts': alerts,
    }
    return render(request, 'core/patient_detail.html', context)

@login_required
def patient_register(request):
    if not request.user.is_technician():
        raise PermissionDenied
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            # Create Patient
            patient = Patient.objects.create(
                name=form.cleaned_data['name'],
                age=form.cleaned_data['age'],
                sex=form.cleaned_data['sex'],
                chief_complaint=form.cleaned_data['chief_complaint'],
                medical_history=form.cleaned_data['medical_history'],
                created_by=request.user
            )
            
            # Create Vital Signs
            VitalSigns.objects.create(
                patient=patient,
                blood_pressure_systolic=form.cleaned_data['blood_pressure_systolic'],
                blood_pressure_diastolic=form.cleaned_data['blood_pressure_diastolic'],
                heart_rate=form.cleaned_data['heart_rate'],
                respiratory_rate=form.cleaned_data['respiratory_rate'],
                oxygen_saturation=form.cleaned_data['oxygen_saturation'],
                recorded_by=request.user
            )
            
            # Create lab results with the current user as recorder
            lab_tests = [
                {
                    'test_name': 'CBC - WBC',
                    'result_value': str(form.cleaned_data['cbc_wbc']),
                    'unit': 'K/µL',
                    'reference_range': '4.5-11.0'
                },
                {
                    'test_name': 'CBC - Hemoglobin',
                    'result_value': str(form.cleaned_data['cbc_hgb']),
                    'unit': 'g/dL',
                    'reference_range': '12.0-16.0'
                },
                {
                    'test_name': 'CBC - Platelets',
                    'result_value': str(form.cleaned_data['cbc_plt']),
                    'unit': 'K/µL',
                    'reference_range': '150-450'
                },
                {
                    'test_name': 'BMP - Sodium',
                    'result_value': str(form.cleaned_data['bmp_sodium']),
                    'unit': 'mEq/L',
                    'reference_range': '135-145'
                },
                {
                    'test_name': 'BMP - Potassium',
                    'result_value': str(form.cleaned_data['bmp_potassium']),
                    'unit': 'mEq/L',
                    'reference_range': '3.5-5.0'
                },
                {
                    'test_name': 'BMP - Creatinine',
                    'result_value': str(form.cleaned_data['bmp_creatinine']),
                    'unit': 'mg/dL',
                    'reference_range': '0.6-1.2'
                },
                {
                    'test_name': 'BMP - Glucose',
                    'result_value': str(form.cleaned_data['bmp_glucose']),
                    'unit': 'mg/dL',
                    'reference_range': '70-140'
                }
            ]
            
            for test in lab_tests:
                LabResult.objects.create(
                    patient=patient,
                    recorded_by=request.user,  # Add the current user as recorder
                    **test
                )
            
            messages.success(request, 'Patient registered successfully with vital signs and lab results.')
            return redirect('core:patient_detail', patient_id=patient.id)
    else:
        form = PatientRegistrationForm()
    return render(request, 'core/patient_form.html', {'form': form, 'title': 'Register Patient'})

@login_required
def record_vitals(request, patient_id):
    if not request.user.is_technician():
        raise PermissionDenied
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        form = VitalSignsForm(request.POST)
        if form.is_valid():
            vitals = form.save(commit=False)
            vitals.patient = patient
            vitals.recorded_by = request.user
            vitals.save()
            
            # Check for critical conditions
            critical_conditions = []
            
            # Check blood pressure
            if vitals.blood_pressure_systolic > 180 or vitals.blood_pressure_diastolic > 110:
                critical_conditions.append(f'Blood Pressure {vitals.blood_pressure_systolic}/{vitals.blood_pressure_diastolic} mmHg is critical')
            
            # Check heart rate
            if vitals.heart_rate > 120 or vitals.heart_rate < 40:
                critical_conditions.append(f'Heart Rate {vitals.heart_rate} bpm is critical')
            
            # Check oxygen saturation
            if vitals.oxygen_saturation < 92:
                critical_conditions.append(f'Oxygen Saturation {vitals.oxygen_saturation}% is critical')
            
            # Check respiratory rate
            if vitals.respiratory_rate < 10 or vitals.respiratory_rate > 24:
                critical_conditions.append(f'Respiratory Rate {vitals.respiratory_rate} breaths/min is critical')
            
            if critical_conditions:
                # Create alert
                Alert.objects.create(
                    patient=patient,
                    message='\n'.join(critical_conditions),
                    severity='HIGH',
                    is_active=True
                )
                
                # Update patient's critical status
                patient.has_critical_alert = True
                patient.save()
            
            messages.success(request, 'Vital signs recorded successfully.')
            return redirect('core:patient_detail', patient_id=patient.id)
    else:
        form = VitalSignsForm()
    return render(request, 'core/vitals_form.html', {'form': form, 'patient': patient})

@login_required
def record_nihss(request, patient_id):
    if not request.user.is_technician():
        raise PermissionDenied
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        form = NIHSSScoreForm(request.POST)
        if form.is_valid():
            nihss = form.save(commit=False)
            nihss.patient = patient
            nihss.recorded_by = request.user
            nihss.save()
            
            # Check for alerts
            if nihss.score > 15:
                Alert.objects.create(
                    patient=patient,
                    message='High NIHSS score detected',
                    severity='HIGH'
                )
            
            messages.success(request, 'NIHSS score recorded successfully.')
            return redirect('core:patient_detail', patient_id=patient.id)
    else:
        form = NIHSSScoreForm()
    return render(request, 'core/nihss_form.html', {'form': form, 'patient': patient})

@login_required
def add_consultation(request, patient_id):
    if not request.user.is_neurologist():
        raise PermissionDenied
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        form = ConsultationForm(request.POST)
        if form.is_valid():
            consultation = form.save(commit=False)
            consultation.patient = patient
            consultation.neurologist = request.user
            consultation.save()
            messages.success(request, 'Consultation added successfully.')
            return redirect('core:patient_detail', patient_id=patient.id)
    else:
        form = ConsultationForm()
    return render(request, 'core/consultation_form.html', {'form': form, 'patient': patient})

@login_required
def resolve_alert(request, alert_id):
    if not request.user.is_neurologist():
        raise PermissionDenied
    
    if request.method != 'POST':
        raise PermissionDenied
    
    alert = get_object_or_404(Alert, id=alert_id)
    patient = alert.patient
    
    # Resolve the alert
    alert.is_active = False
    alert.resolved_at = timezone.now()
    alert.resolved_by = request.user
    alert.save()
    
    # Check if patient has any remaining active alerts
    if not Alert.objects.filter(patient=patient, is_active=True).exists():
        patient.has_critical_alert = False
        patient.save()
    
    messages.success(request, 'Alert resolved successfully.')
    
    # Redirect back to the page that submitted the form
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('core:patient_detail', patient_id=patient.id)

@login_required
def delete_patient(request, patient_id):
    if not request.user.is_technician() and not request.user.is_neurologist():
        raise PermissionDenied
    
    patient = get_object_or_404(Patient, id=patient_id)
    
    if request.method == 'POST':
        patient.delete()
        messages.success(request, 'Patient data deleted successfully.')
        return redirect('core:patient_list')
    
    return render(request, 'core/delete_patient.html', {'patient': patient})
    
    messages.success(request, 'Alert resolved successfully.')
    return redirect('core:patient_detail', patient_id=alert.patient.id)
