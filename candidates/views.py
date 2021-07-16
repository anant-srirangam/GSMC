from django.shortcuts import render, redirect, get_object_or_404
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


def adminDashboard(request):
    if not request.user.is_authenticated or request.user.username != 'admin':
        return get_object_or_404(User, pk=0)

    requests = CandidateActions.objects.filter(workflowLevel='apply',listing__is_listed=True).order_by('applyDate')
    context = {
        'buttonid':3,
        'requestType':'apply',
        'requests':requests,
        'search':False,
        'linkUrl':'dashboard'
    }
    return render(request, 'candidates/admin_dashboard.html', context)


def candidateShortlist(request):
    if not request.user.is_authenticated or request.user.username != 'admin':
        return get_object_or_404(User, pk=0)

    requests = CandidateActions.objects.filter(workflowLevel='shortlist',listing__is_listed=True).order_by('shortlistDate')
    context = {
        'buttonid':3,
        'requestType':'shortlist',
        'requests':requests,
        'search':False,
        'linkUrl':'dashboard'
    }
    return render(request, 'candidates/admin_dashboard.html', context)


def candidateSelect(request):
    if not request.user.is_authenticated or request.user.username != 'admin':
        return get_object_or_404(User, pk=0)

    requests = CandidateActions.objects.filter(workflowLevel='select', candidateLeft=False).order_by('-selectionDate')
    context = {
        'buttonid':3,
        'requestType':'select',
        'requests':requests,
        'search':False,
        'linkUrl':'dashboard'
    }
    return render(request, 'candidates/admin_dashboard.html', context)


def candidateReject(request):
    if not request.user.is_authenticated or request.user.username != 'admin':
        return get_object_or_404(User, pk=0)

    requests = CandidateActions.objects.filter(workflowLevel='reject').order_by('rejectDate')
    context = {
        'buttonid':3,
        'requestType':'reject',
        'requests':requests,
        'search':False,
        'linkUrl':'dashboard'
    }
    return render(request, 'candidates/admin_dashboard.html', context)


def candidateListing(request, listing_id, action_id, status):
    if not request.user.is_authenticated or request.user.username != 'admin':
        return get_object_or_404(User, pk=0)

    candidate = get_object_or_404(CandidateActions, pk=action_id, workflowLevel=status)

    if 'HTTP_REFERER' in request.META:
        linkUrl = request.META['HTTP_REFERER']
    else:
        linkUrl = 'candidateAdminDashboard'
    

    context = {
        'candidate':candidate,
        'linkUrl':linkUrl,
        'statusCode':status
    }
    return render(request, 'candidates/candidate_listing.html', context)


def shortListCandidate(request, action_id):
    if not request.user.is_authenticated or request.user.username != 'admin' or request.method != 'POST':
        return get_object_or_404(User, pk=0)

    candidate = get_object_or_404(CandidateActions, pk=action_id)
    listing = get_object_or_404(Listing, pk=candidate.listing.id, is_listed=True)

    candidate.shortlistDate = datetime.now()
    candidate.workflowLevel = 'shortlist'
    candidate.save()

    listing.shortLists = listing.shortLists + 1
    listing.save()

    linkUrl = request.POST['linkUrl']

    return redirect(linkUrl)


def selectCandidate(request, action_id):
    if not request.user.is_authenticated or request.user.username != 'admin' or request.method != 'POST':
        return get_object_or_404(User, pk=0)

    candidate = get_object_or_404(CandidateActions, pk=action_id)
    listing = get_object_or_404(Listing, pk=candidate.listing.id, is_listed=True)

    candidate.selectionDate = datetime.now()
    candidate.workflowLevel = 'select'
    candidate.save()

    listing.selections = listing.selections + 1
    listing.save()

    linkUrl = request.POST['linkUrl']

    return redirect(linkUrl)


def rejectCandidate(request, action_id):
    if not request.user.is_authenticated or request.user.username != 'admin' or request.method != 'POST':
        return get_object_or_404(User, pk=0)

    candidate = get_object_or_404(CandidateActions, pk=action_id)
    listing = get_object_or_404(Listing, pk=candidate.listing.id, is_listed=True)

    candidate.rejectDate = datetime.now()
    candidate.workflowLevel = 'reject'
    candidate.reason = request.POST['reason']
    candidate.save()

    linkUrl = request.POST['linkUrl']

    return redirect(linkUrl)


def candidateLeft(request, action_id):
    if not request.user.is_authenticated or request.user.username != 'admin' or request.method != 'POST':
        return get_object_or_404(User, pk=0)

    candidate = get_object_or_404(CandidateActions, pk=action_id)
    listing = get_object_or_404(Listing, pk=candidate.listing.id, is_listed=True)

    candidate.rejectDate = datetime.now()

    if candidate.workflowLevel == 'select':
        listing.selections = listing.selections-1
        listing.candidateLeft = listing.candidateLeft+1
        listing.save()
        
    candidate.candidateLeft = True
    candidate.save()

    linkUrl = request.POST['linkUrl']

    return redirect(linkUrl)


def blackListCandidate(request, action_id):
    if not request.user.is_authenticated or request.user.username != 'admin' or request.method != 'POST':
        return get_object_or_404(User, pk=0)

    candidateAction = get_object_or_404(CandidateActions, pk=action_id)
    candidate = get_object_or_404(Candidate, pk=candidateAction.candidate.id)

    candidate.blacklisted=True
    candidate.save()

    linkUrl = request.POST['linkUrl']

    return redirect(linkUrl)


def searchCandidate(request, requestType):
    if not request.user.is_authenticated or request.user.username != 'admin':
        return get_object_or_404(User, pk=0)

    requests = CandidateActions.objects.filter(workflowLevel=requestType)

    if 'name' in request.GET:
        keywords = request.GET['name']
        if keywords:
            requests = requests.filter(candidate__name__icontains=keywords)
    if 'email' in request.GET:
        keywords = request.GET['email']
        if keywords:
            requests = requests.filter(candidate__email__icontains=keywords)
    if 'phone' in request.GET:
        keywords = request.GET['phone']
        if keywords:
            requests = requests.filter(candidate__phone__icontains=keywords)
    if 'jobId' in request.GET:
        keywords = request.GET['jobId']
        if keywords:
            requests = requests.filter(listing__gsmcJobId__icontains=keywords)
    if 'date' in request.GET:
        keywords = request.GET['date']
        if keywords:
            datetimeobj = datetime.strptime(keywords, '%Y-%m-%d')
            if requestType == 'apply':
                requests = requests.filter(applyDate=datetimeobj)
            elif requestType == 'shortlist':
                requests = requests.filter(shortlistDate=datetimeobj)
            elif requestType == 'select':
                requests = requests.filter(selectionDate__year=datetimeobj.year, selectionDate__month=datetimeobj.month,
                                            selectionDate__day=datetimeobj.day)
            elif requestType == 'reject':
                requests = requests.filter(rejectDate=datetimeobj)
    
    if requestType == 'apply':
        linkUrl = 'candidateAdminDashboard'
    elif requestType == 'shortlist':
        linkUrl = 'candidateShortlist'
    elif requestType == 'select':
        linkUrl = 'candidateSelect'
    elif requestType == 'reject':
        linkUrl = 'candidateReject'

    context = {
        'buttonid':3,
        'requestType':requestType,
        'requests':requests,
        'search':True,
        'candidateName':request.GET['name'],
        'candidateEmail':request.GET['email'],
        'candidateJobId':request.GET['jobId'],
        'candidateDate':request.GET['date'],
        'linkUrl':linkUrl
    }

    return render(request, 'candidates/admin_dashboard.html', context)
    


