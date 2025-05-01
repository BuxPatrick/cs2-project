from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from patients.models import Patient
from neurologists.models import Neurologist, Consultation
from alerts.models import Alert

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Please complete your profile.')
            return redirect('profile')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    # Get user's related data
    try:
        neurologist = Neurologist.objects.get(user=request.user)
        is_neurologist = True
    except Neurologist.DoesNotExist:
        neurologist = None
        is_neurologist = False

    context = {
        'user': request.user,
        'is_neurologist': is_neurologist,
        'neurologist': neurologist,
    }
    return render(request, 'profile.html', context)

@login_required
def dashboard(request):
    # Get counts for dashboard cards
    patients_count = Patient.objects.count()
    neurologists_count = Neurologist.objects.count()
    active_consultations_count = Consultation.objects.filter(status='IN_PROGRESS').count()
    active_alerts_count = Alert.objects.filter(status__in=['NEW', 'READ']).count()

    # Get recent consultations and alerts
    recent_consultations = Consultation.objects.select_related(
        'patient', 'neurologist__user'
    ).order_by('-created_at')[:5]

    recent_alerts = Alert.objects.order_by('-created_at')[:5]

    context = {
        'patients_count': patients_count,
        'neurologists_count': neurologists_count,
        'active_consultations_count': active_consultations_count,
        'active_alerts_count': active_alerts_count,
        'recent_consultations': recent_consultations,
        'recent_alerts': recent_alerts,
    }
    return render(request, 'dashboard.html', context)

@login_required
def patients_list(request):
    patients = Patient.objects.all()
    return render(request, 'patients/list.html', {'patients': patients})

@login_required
def patient_detail(request, pk):
    patient = Patient.objects.get(pk=pk)
    vital_signs = patient.vital_signs.all()
    lab_results = patient.lab_results.all()
    imaging_studies = patient.imaging_studies.all()
    nihss_scores = patient.nihss_scores.all()
    consultations = patient.consultations.all()

    context = {
        'patient': patient,
        'vital_signs': vital_signs,
        'lab_results': lab_results,
        'imaging_studies': imaging_studies,
        'nihss_scores': nihss_scores,
        'consultations': consultations,
    }
    return render(request, 'patients/detail.html', context)

@login_required
def neurologists_list(request):
    neurologists = Neurologist.objects.select_related('user').all()
    return render(request, 'neurologists/list.html', {'neurologists': neurologists})

@login_required
def neurologist_detail(request, pk):
    neurologist = Neurologist.objects.select_related('user').get(pk=pk)
    consultations = neurologist.consultations.select_related('patient').all()
    return render(request, 'neurologists/detail.html', {
        'neurologist': neurologist,
        'consultations': consultations
    })

@login_required
def consultations_list(request):
    consultations = Consultation.objects.select_related(
        'patient', 'neurologist__user'
    ).all()
    return render(request, 'consultations/list.html', {'consultations': consultations})

@login_required
def consultation_detail(request, pk):
    consultation = Consultation.objects.select_related(
        'patient', 'neurologist__user'
    ).get(pk=pk)
    treatment_orders = consultation.treatment_orders.all()
    test_orders = consultation.test_orders.all()
    return render(request, 'consultations/detail.html', {
        'consultation': consultation,
        'treatment_orders': treatment_orders,
        'test_orders': test_orders
    })

@login_required
def alerts_list(request):
    alerts = Alert.objects.select_related('created_by').all()
    return render(request, 'alerts/list.html', {'alerts': alerts})

@login_required
def alert_detail(request, pk):
    alert = Alert.objects.select_related('created_by').get(pk=pk)
    notification_logs = alert.notification_logs.select_related('recipient').all()
    return render(request, 'alerts/detail.html', {
        'alert': alert,
        'notification_logs': notification_logs
    }) 