from django.shortcuts import render, redirect
from .models import Project, ContactMessage
from .forms import ContactForm 
from django.core.mail import send_mail
from .forms import ProjectForm
import json
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required



def home(request):
    projects = Project.objects.all()
    messages = ContactMessage.objects.all()

    return render(request, "main/home.html", {"projects": projects,  "messages": messages})

@csrf_exempt  # needed because we’re using JavaScript fetch with DELETE
def delete_project(request, project_id):
    if request.method == "DELETE":
        try:
            project = Project.objects.get(pk=project_id)
            project.delete()
            return JsonResponse({"message": "Project deleted successfully."})
        except Project.DoesNotExist:
            return JsonResponse({"error": "Project not found."}, status=404)
    return HttpResponseNotAllowed(["DELETE"])



def project_list(request):
    projects = Project.objects.all()
    return render(request, 'main/projects.html', {'projects': projects})



def contact_view(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("contact")
    
    return render(request, "main/contact.html", {"form": form})

def contact(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Send or save logic
            send_mail(
                f"Message from {form.cleaned_data['name']}",
                form.cleaned_data['message'],
                form.cleaned_data['email'],
                ['youremail@example.com'],
            )
            return redirect('contact')
    return render(request, 'main/contact.html', {'form': form})

def project_list(request):
    projects = Project.objects.all()
    return render(request, 'main/projects.html', {'projects': projects})

def add_project(request):
    projects = Project.objects.all()  # Get all submitted projects

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save to the database
            return redirect('add_project')  # Reload to show new projects

    else:
        form = ProjectForm()

    return render(request, "main/add_project.html", {"form": form, "projects": projects})


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('register')

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Registration successful! Please log in.")
        return redirect('login')  # ✅ Redirect to login page

    return render(request, 'main/register.html')



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main/home')  # ✅ Redirect to home page
        
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')

    return render(request, 'main/login.html')

@login_required
def project_page(request):
    return render(request, 'main/project.html')

@login_required
def contact_page(request):
    return render(request, 'main/contact.html')

@login_required
def submit_project(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        link = request.POST.get("link")
        image = request.FILES.get("image")

        project = Project.objects.create(
            title=title,
            description=description,
            link=link,
            image=image,
            creator=request.user
        )

        return JsonResponse({
            "id": project.id,
            "title": project.title,
            "link": project.link,
            "image_url": project.image.url if project.image else ""
        })

    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
def projects(request):
    user_projects = Project.objects.filter(creator=request.user)  # Filter projects
    return render(request, 'main/projects.html', {'projects': user_projects})












