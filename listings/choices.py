from .models import Listing


def getCompanyList():
    return  Listing.objects.filter(is_listed=True).order_by('employer__profile__company__companyName').values('employer__profile__company__id', 'employer__profile__company__companyName').distinct()


def getJobTitleList():
    return Listing.objects.filter(is_listed=True).order_by('jobTitle').values_list('jobTitle', flat=True).distinct()


def getMinExpList():
    return Listing.objects.filter(is_listed=True).order_by('minExp').values_list('minExp', flat=True).distinct()


def getMaxExpList():
    return Listing.objects.filter(is_listed=True).order_by('maxExp').values_list('maxExp', flat=True).distinct()

def experience(_limit):
    exp = {}
    for i in range(1,_limit+1):
        exp[i]=i
    return exp


def min_experience():
    return experience(30)


def max_experience():
    return experience(60)

