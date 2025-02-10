from django.shortcuts import render, redirect
from .models import User,CodeSubmission
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login
from urllib.parse import unquote
from django.http import JsonResponse
import json
import requests
import pdfkit

# Configure pdfkit with wkhtmltopdf path
PDFKIT_CONFIG = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')


def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        admission_no = request.POST.get('admission_no')

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already taken'})

        # Save the user to the database
        User.objects.create(username=username, admission_no=admission_no)
        return redirect('login')  # Redirect to the login page

    return render(request, 'register.html')


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        admission_no = request.POST.get('admission_no')

        # Authenticate user by checking the database
        try:
            user = User.objects.get(username=username, admission_no=admission_no)
            request.session['username'] = user.username  # Store user session
            return redirect('home')
        except User.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')

QUESTIONS = {
    "question_1": "Write a Python program to find the factorial of a number.",
    "question_2": "Write a Python program to check if a string is a palindrome.",
    "question_3": "Write a Python program to generate Fibonacci series up to a given number."
}

def home_page(request):
    completed_questions = request.session.get('completed_questions', [])
    submissions = {}

    for key, question in QUESTIONS.items():
        submissions[key] = {
            'submitted': question in completed_questions,
            'pdf_generated': question in completed_questions
        }

    return render(request, 'home.html', {'submissions': submissions, 'questions': QUESTIONS})



def index(request):
    if request.session.get('malpractice_detected', False):
        return redirect('malpractice')

    user = User.objects.get(username=request.session.get('username'))
    question = request.POST.get('question') or request.session.get('question', '')

    # Save question in session for later
    if question:
        request.session['question'] = question

    submission = CodeSubmission.objects.filter(user=user, question=question).first()

    code = submission.code if submission else ''
    output = submission.output if submission else ''
    selected_mode = request.GET.get('mode', 'lab')

    # Prevent returning to index page after malpractice detection
    if request.session.get('malpractice_cycles', 0) >= 3 and selected_mode == "exam":
        request.session['malpractice_detected'] = True
        return redirect('malpractice')

    return render(request, 'index.html', {
        'selected_mode': selected_mode,
        'question': question,
        'code': code if selected_mode == "lab" else '',
        'output': output if selected_mode == "lab" else ''
    })



def save_code(request):
    """Save code without needing compilation."""
    user = User.objects.get(username=request.session.get('username'))
    question = request.session.get('question', '')

    if request.method == 'POST':
        code = request.POST.get('code', '')

        # Save code even if not compiled
        submission, created = CodeSubmission.objects.get_or_create(user=user, question=question)
        submission.code = code
        submission.save()

    return redirect('index')


def compile_code(request):
    user = User.objects.get(username=request.session.get('username'))
    selected_mode = request.POST.get('mode', 'lab')
    question = request.session.get('question', '')
    code = request.POST.get('code', '')

    submission, created = CodeSubmission.objects.get_or_create(user=user, question=question)
    submission.code = code

    if request.method == 'POST':
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
        submission.output = output
        submission.save()

    return render(request, 'index.html', {
        'code': code,
        'output': submission.output,
        'selected_mode': selected_mode,
        'question': question
    })

def view_pdf(request, code, output):
    decoded_code = unquote(code)
    decoded_output = unquote(output)
    question = request.session.get('question', '')

    return render(request, 'record.html', {
        'code': decoded_code,
        'output': decoded_output,
        'question': question,
        'hide_button': False
    })



def generate_pdf(request, code, output):
    user = User.objects.get(username=request.session.get('username'))
    question = request.session.get('question', '')

    decoded_code = unquote(code)
    decoded_output = unquote(output)

    html_content = render_to_string('record.html', {
        'code': decoded_code,
        'output': decoded_output,
        'question': question,
        'hide_button': True
    })

    pdf = pdfkit.from_string(html_content, False, configuration=PDFKIT_CONFIG)

    # Save PDF status in the session instead of the database
    if 'completed_questions' not in request.session:
        request.session['completed_questions'] = []
    if question not in request.session['completed_questions']:
        request.session['completed_questions'].append(question)
    request.session.modified = True

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="record.pdf"'

    return response


def malpractice(request):
    return render(request, 'malpractice.html')

def mark_complete(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        question = data.get('question')

        # Save the status in session for simplicity
        if 'completed_questions' not in request.session:
            request.session['completed_questions'] = []
        if question not in request.session['completed_questions']:
            request.session['completed_questions'].append(question)
        request.session.modified = True

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'}, status=400)