from django.shortcuts import render, redirect
from .forms import ContactForm
from django.contrib import messages

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  
            messages.success(request, 'Your message has been successfully saved and sent.')
            return redirect('contact')  
        else:
            messages.error(request, 'The form is not valid. please check the fields.')
    else:
        form = ContactForm()
    return render(request, 'contact/contact.html', {'form': form})
