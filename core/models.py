from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class User(AbstractUser):
    ROLE_CHOICES = [
        ('TECHNICIAN', 'Technician'),
        ('NEUROLOGIST', 'Neurologist'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_technician(self):
        return self.role == 'TECHNICIAN'
    
    def is_neurologist(self):
        return self.role == 'NEUROLOGIST'

class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]

    name = models.CharField(max_length=100)
    age = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(150)])
    sex = models.CharField(max_length=1, choices=GENDER_CHOICES)
    chief_complaint = models.TextField()
    medical_history = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patients')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    has_critical_alert = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.age})"

class VitalSigns(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='vital_signs')
    blood_pressure_systolic = models.IntegerField()
    blood_pressure_diastolic = models.IntegerField()
    heart_rate = models.IntegerField()
    respiratory_rate = models.IntegerField()
    oxygen_saturation = models.DecimalField(max_digits=4, decimal_places=1)
    recorded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recorded_vitals')
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # First save the vital signs
        super().save(*args, **kwargs)
        # Then check for critical conditions
        self.check_critical_thresholds()

    def check_critical_thresholds(self):
        """Check vital signs against critical thresholds and create alerts if needed."""
        critical_conditions = []
        
        # Check blood pressure
        if self.blood_pressure_systolic > 180 or self.blood_pressure_diastolic > 110:
            critical_conditions.append(f'Blood Pressure {self.blood_pressure_systolic}/{self.blood_pressure_diastolic} mmHg is critical')
        
        # Check heart rate
        if self.heart_rate > 120 or self.heart_rate < 40:
            critical_conditions.append(f'Heart Rate {self.heart_rate} bpm is critical')
        
        # Check oxygen saturation
        if self.oxygen_saturation < 92:
            critical_conditions.append(f'Oxygen Saturation {self.oxygen_saturation}% is critical')
        
        # Check respiratory rate
        if self.respiratory_rate < 10 or self.respiratory_rate > 24:
            critical_conditions.append(f'Respiratory Rate {self.respiratory_rate} breaths/min is critical')
        
        if critical_conditions:
            # Update patient's critical alert status
            self.patient.has_critical_alert = True
            self.patient.save()
            
            # Create alert
            Alert.objects.create(
                patient=self.patient,
                message='\n'.join(critical_conditions),
                severity='HIGH',
                is_active=True
            )
        
        return bool(critical_conditions)

    class Meta:
        ordering = ['-timestamp']

class LabResult(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='lab_results')
    test_name = models.CharField(max_length=100)
    result_value = models.CharField(max_length=100)
    unit = models.CharField(max_length=50)
    reference_range = models.CharField(max_length=100)
    recorded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recorded_labs')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

class Imaging(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='imaging_studies')
    study_type = models.CharField(max_length=100)  # e.g., CT, MRI
    findings = models.TextField()
    image_url = models.URLField()
    recorded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recorded_imaging')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'Imaging Studies'

class NIHSSScore(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='nihss_scores')
    score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(42)])
    notes = models.TextField(blank=True)
    recorded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recorded_nihss')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'NIHSS Score'
        verbose_name_plural = 'NIHSS Scores'

class Consultation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='consultations')
    neurologist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='provided_consultations')
    diagnosis = models.TextField()
    treatment_plan = models.TextField()
    additional_orders = models.TextField(blank=True, help_text='Additional orders such as medications, tests, or imaging studies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

class Alert(models.Model):
    SEVERITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High')
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='alerts')
    message = models.TextField()
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='resolved_alerts')

    class Meta:
        ordering = ['-created_at']
