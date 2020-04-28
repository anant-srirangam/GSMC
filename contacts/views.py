from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Contact
from django.core.mail import send_mail


def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']
        
        if request.user.is_authenticated:
            user_id = request.POST['user_id']
            if Contact.objects.filter(user_id=user_id,
                                    listing_id=listing_id).exists():
                messages.error(request, 'You have already made an enquiry for this property')
                return redirect(f'/listings/{listing_id}')                    
        elif Contact.objects.filter(email=email,
                                    listing_id=listing_id).exists():
                messages.error(request, f'An enquiry for this property has already been placed using this email id - {email}')
                return redirect(f'/listings/{listing_id}') 
        
        contact = Contact(listing=listing,
                        listing_id=listing_id,
                        name=name,
                        email=email,
                        phone=phone,
                        message=message,
                        user_id=user_id)
        
        contact.save()

        send_mail(
            subject=f'BTRE Property Inquiry : {listing}',
            message=f'''There has been an inquiry for {listing}. 
            User : {name}
            Email : {email}
            Phone : {phone}
            Message : {message}

            You may also sign into admin portal for all the info.
            ''',
            from_email = 'anant.keylogger@gmail.com',
            recipient_list=[realtor_email, 'anant.srirangam@gmail.com'],
            fail_silently=False
        )

        messages.success(request, 'Your request has been submitted.')

        return redirect('listings')

