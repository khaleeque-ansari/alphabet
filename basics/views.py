from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    context = {}
    return render(request, 'basics/index.html', context)


def resume(request):
    context = {}
    return render(request, 'basics/resume.html', context)


def resume_pdf(request):
    resume_data = open("static/basics/downloads/Khaleeque_Ansari_Resume.pdf", "rb").read()
    return HttpResponse(resume_data, content_type="application/pdf")