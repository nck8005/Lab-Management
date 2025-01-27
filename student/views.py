from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from urllib.parse import unquote
import requests
import pdfkit

# Configure pdfkit with wkhtmltopdf path
PDFKIT_CONFIG = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

def index(request):
    # Check if the user has committed malpractice
    if request.session.get('malpractice_detected', False):
    #request.session['malpractice_detected'] = True

        return redirect('malpractice')
    
    return render(request, 'index.html')

def compile_code(request):
    code = ""
    output = ""

    if request.method == 'POST':
        code = request.POST.get('code', '')

        # JDoodle API credentials
        client_id = 'a73de56372fd3216cb181a6c34802bf2'
        client_secret = 'dec03d572ded614e118ced5f1dd4f38e3b6f6b60343b525984a4474de3750298'
        
        url = "https://api.jdoodle.com/v1/execute"
        payload = {
            "script": code,
            "language": "python3",
            "versionIndex": "3",
            "clientId": client_id,
            "clientSecret": client_secret
        }

        response = requests.post(url, json=payload)
        result = response.json()

        output = result.get('output', result.get('error', 'Error executing code'))

    return render(request, 'index.html', {'code': code, 'output': output})

def view_pdf(request, code, output):
    decoded_code = unquote(code)
    decoded_output = unquote(output)

    return render(request, 'record.html', {
        'code': decoded_code,
        'output': decoded_output,
        'hide_button': False
    })

def generate_pdf(request, code, output):
    decoded_code = unquote(code)
    decoded_output = unquote(output)

    html_content = render_to_string('record.html', {
        'code': decoded_code,
        'output': decoded_output,
        'hide_button': True
    })

    pdf = pdfkit.from_string(html_content, False, configuration=PDFKIT_CONFIG)

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="record.pdf"'
    return response

# New view for malpractice page
def malpractice(request):
    return render(request, 'malpractice.html')
