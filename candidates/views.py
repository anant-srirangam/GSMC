from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from datetime import datetime
from .models import Candidate, CandidateActions
from listings.models import Listing


def applyListing(request, listing_id):
    if request.method == 'POST':
        fileTypes = [
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/pdf'
        ]

        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        resume = request.FILES['resume']

        if Candidate.objects.filter(email=email, blacklisted=True).exists():
            messages.error(request, 'You are a blacklisted candidate. Please contact admin')
            return redirect('listing',listing_id)
        elif resume.content_type not in fileTypes:
            messages.error(request, 'Invalid file type')
            return redirect('listing',listing_id)
        elif resume.size/1024 > 500:
            messages.error(request, 'File too big')
            return redirect('listing',listing_id)
        elif CandidateActions.objects.filter(listing__id=listing_id, candidate__email=email).exclude(workflowLevel='rejected').exists():
            messages.error(request, 'You already applied for this job')
            return redirect('listing',listing_id)

        listing = Listing.objects.get(pk=listing_id)
        candidate, created = Candidate.objects.get_or_create(email=email,
                                                            defaults={
                                                                'name':name,
                                                                'phone':phone
                                                            })

        candidateAction = CandidateActions.objects.create(candidate=candidate,
                                                            listing=listing,
                                                            resume=resume)

        

        listing.noOfApplies = listing.noOfApplies+1
        listing.save()

        messages.success(request, 'Successfully applied...')


        return redirect('listing',listing_id)
    else:
        redirect('index')

