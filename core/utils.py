import random
from datetime import datetime, timedelta

def generate_simulated_patient_data():
    """Generate realistic simulated patient data for stroke cases."""
    
    # Common stroke-related complaints
    chief_complaints = [
        "Sudden weakness in right arm and leg",
        "Difficulty speaking and facial drooping",
        "Left-sided weakness and confusion",
        "Severe headache with vision problems",
        "Sudden loss of balance with dizziness"
    ]
    
    # Common medical history entries
    medical_histories = [
        "Hypertension, Type 2 Diabetes",
        "Atrial Fibrillation, Previous TIA",
        "Coronary Artery Disease, Hyperlipidemia",
        "History of smoking, Obesity",
        "Previous stroke, Hypertension"
    ]
    
    # Generate basic patient info
    first_names = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", "William", "Elizabeth"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
    
    data = {
        'name': f"{random.choice(first_names)} {random.choice(last_names)}",
        'age': random.randint(45, 85),
        'sex': random.choice(['M', 'F']),
        'chief_complaint': random.choice(chief_complaints),
        'medical_history': random.choice(medical_histories),
        
        # Vital Signs (realistic ranges for stroke patients)
        'blood_pressure_systolic': random.randint(140, 200),
        'blood_pressure_diastolic': random.randint(80, 110),
        'heart_rate': random.randint(60, 100),
        'respiratory_rate': random.randint(12, 20),
        'oxygen_saturation': random.randint(94, 100),
        
        # Lab Results (realistic ranges)
        'cbc_wbc': round(random.uniform(4.5, 11.0), 2),
        'cbc_hgb': round(random.uniform(12.0, 16.0), 2),
        'cbc_plt': round(random.uniform(150.0, 450.0), 2),
        'bmp_sodium': random.randint(135, 145),
        'bmp_potassium': round(random.uniform(3.5, 5.0), 1),
        'bmp_creatinine': round(random.uniform(0.6, 1.2), 2),
        'bmp_glucose': random.randint(70, 180)
    }
    
    return data
