from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from .utils import generate_simulated_patient_data

@api_view(['GET'])
@login_required
def simulate_patient_data(request):
    """API endpoint to generate simulated patient data."""
    data = generate_simulated_patient_data()
    return Response(data)
