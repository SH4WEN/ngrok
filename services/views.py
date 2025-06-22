from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import ChatMessage, SharedFile, EmailMessage
from .forms import FileUploadForm, EmailForm

@login_required
def home(request):
    return render(request, 'services/home.html')

@login_required
def chatroom(request):
    messages = ChatMessage.objects.order_by('-timestamp')[:50]
    return render(request, 'services/chatroom.html', {'messages': messages})

@login_required
def file_share(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.user = request.user
            file.save()
            return redirect('file_share')
    else:
        form = FileUploadForm()
    
    files = SharedFile.objects.order_by('-uploaded_at')
    return render(request, 'services/file_share.html', {'form': form, 'files': files})

@login_required
def mail(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.save(commit=False)
            email.sender = request.user
            email.save()
            return redirect('mail_inbox')
    else:
        form = EmailForm()
    
    return render(request, 'services/mail_compose.html', {'form': form})

@login_required
def mail_inbox(request):
    received_emails = EmailMessage.objects.filter(recipient=request.user).order_by('-sent_at')
    return render(request, 'services/mail_inbox.html', {'emails': received_emails})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
