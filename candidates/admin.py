from django.contrib import admin
from .models import Candidate, CandidateActions

class CandidatesAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'name',
                    'email',
                    'phone',
                    'blacklisted',
                    'noOfApplies',
                    'noOfOffers',
                    'reason'
                    )
    list_display_links = ('id',
                        'name',
                        'email',
                        'phone')
    list_filter = ('blacklisted','email','phone','noOfOffers','noOfApplies')
    list_editable = ('blacklisted',)
    search_fields = ('name','email','phone')
    list_per_page = 25


class CandidateActionAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'get_candidate',
                    'get_listing',
                    'resume',
                    'workflowLevel',
                    'candidateLeft',
                    'reason'
                    )

    

    list_display_links = ('id',)
    list_filter = ('workflowLevel','candidateLeft',
                    'applyDate','rejectDate','shortlistDate','selectionDate')
    list_editable = ('candidateLeft',)
    search_fields = ('candidate__id','listing__id')
    list_per_page = 25

    def get_candidate(self, obj):
        return obj.candidate.email
    get_candidate.short_description = 'Candidate' 

    def get_listing(self, obj):
        return obj.listing.gsmcJobId
    get_candidate.short_description = 'Listing' 

admin.site.register(Candidate, CandidatesAdmin)
admin.site.register(CandidateActions, CandidateActionAdmin)
