from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Contact
from django.core.mail import send_mail


def contact(request):
    if request.method == 'POST':
        userType = request.POST['job_title']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        
        contact = Contact(userType=userType,
                        name=name,
                        email=email,
                        phone=phone,
                        message=message)
        
        contact.save()

        send_mail(
            subject=f'New Inquiry : {userType}',
            message=f'''There has been a new inquiry from {userType}. 
            User : {name}
            Email : {email}
            Phone : {phone}
            Message : {message}

            You may also sign into admin portal for all the info.
            ''',
            from_email = 'anant.keylogger@gmail.com',
            recipient_list=['anantkumarofficial@gmail.com', 'anant.srirangam@gmail.com'],
            fail_silently=False
        )

        messages.success(request, 'Your request has been submitted.')

        return redirect('about')

    else:
        return redirect('index')

