from django.shortcuts import render, HttpResponse, redirect
from care_all.models import Elder, Youngster, CareRequest, Reviews
from accounts.models import User
from django.views.generic import FormView, UpdateView, ListView, DetailView
from django.views import View
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from care_all.forms import ContactUsForm, WriteReviewForm

# Create your views here.

# ****************************  ****************************  **************************** 
#     **************************** General Functionalities **************************** 
# ****************************  ****************************  **************************** 


def home_view(request):
    return render(request, 'care_all/home_page.html')


def show_profile_view(request, *args, **kwargs):
    #Profile functionality
    user = request.user

    if user.role == 'Elder':
        profile = Elder.objects.get(user=user)
    #Listing Review functionality
        reviews = Reviews.objects.filter(review_written_for_elder = profile)

    else:
        profile = Youngster.objects.get(user=user)
    #Listing Review functionality
        reviews = Reviews.objects.filter(review_written_for_youngster = profile)
 

    #Writing Review functionality
    if request.method == 'GET':
        review_form = WriteReviewForm()
    else:
        review_form = WriteReviewForm(request.POST)
        if review_form.is_valid():
            review_form.save()
            messages.success(request, 'Your review has been posted. Thanks !')

        else:
            messages.error(request, 'You need to write Subject, Comment and give the Rating to submit your review. All three are required')
            # print(review_form.errors)

    return render(request, 'care_all/show_profile_page.html', context = {"profile":profile, "reviews":reviews}) 



def make_donation_view(request):
    return HttpResponse("<h1>Donation Payment Gateway</h1>")



def privacy_policy_view(request):
    return HttpResponse("<h1>Privacy Policy Page</h1>")



class contact_us_view(FormView):
    form_class = ContactUsForm
    template_name = "care_all/contact_us.html"
    success_url = reverse_lazy("thank_you_page")
    


def thank_you_view(request): 
    return HttpResponse("<h1>Thank you for contacting us, we will get back to you shortly.</h1>")



# ****************************  ****************************  **************************** 
#     **************************** Elder Functionalities **************************** 
# ****************************  ****************************  **************************** 

class edit_elder_profile_view(UpdateView):
    model = Elder
    template_name = "care_all/edit_profile_page.html"
    fields = ['profile_photo', 'name', 'age', 'status', 'bio']



def care_request_queue_view(request):
    user = request.user
    elder_obj = Elder.objects.get(user = user)
    requests = CareRequest.objects.filter(requested_for = elder_obj)

    # To show the elder in whose care he/she is (if and when the care request is approved)
    if elder_obj.in_care:
        care_giver = elder_obj.care_giver
    else:
        care_giver = ''
                
    return render(request, 'care_all/elder_care_request_queue_page.html', context = {'requests':requests, 'care_giver':care_giver })



def care_request_sender_profile_view(request, *args, **kwargs):
    youngster_id = kwargs['pk']
    youngster = Youngster.objects.get(id=youngster_id)

    elder = Elder.objects.get(user = request.user)
    
    #Listing Review functionality
    reviews = Reviews.objects.filter(review_written_for_youngster=youngster)

    #Writing Review functionality
    if request.method == 'GET':
        review_form = WriteReviewForm()
    else:
        review_form = WriteReviewForm(request.POST)
        
        if review_form.is_valid():
            review_form.save()

            #Getting review writer and review written for OBJECTS
            youngster_obj = youngster
            elder_obj = elder

            #Fetching the current review to further update its values
            current_review_subject = review_form.cleaned_data['review_subject']
            current_review = Reviews.objects.get(review_subject=current_review_subject)

            #Updating the review writer and review written for
            current_review.review_writer_elder = elder_obj
            current_review.review_written_for_youngster = youngster_obj
            current_review.save()
            
            messages.success(request, 'Your review has been posted. Thanks !')

        else:
            messages.error(request, 'You need to write Subject, Comment and give the Rating to submit your review. All three are required')
            # print(review_form.errors)

    return render(request, 'care_all/care_request_sender_profile_page.html', context={'youngster':youngster, 'elder':elder, 'reviews':reviews})



class approve_care_request_view(View):

    def get(self, request, **kwagrs):

    # Check if a youngster is having max 4 elders in care at a time or not
        user_id = kwagrs.get('pk')
        youngster_obj = Youngster.objects.get(id=user_id)

        if youngster_obj.elders_in_care >= 4 :
            messages.warning(request, 'Max Limit Exceeds ! Youngster can only take care of 4 elders at a time')

            return redirect(reverse('care_request_sender_profile_page' , args=(user_id,)))

        else:
    #Pre-checks before approving the request. If pre-checks failed then deny access to approve request
            elder_obj = Elder.objects.get(user=request.user)

        # Check if elder is available and not in someone's care before approving the request.
            if elder_obj.in_care:
                messages.warning(request, 'You are in-care of a youngster already. You cannot accept the care from more than one person at a time')
                
                return redirect(reverse('care_request_sender_profile_page' , args=(user_id,)))
            
        # Check if elder is un-available.
            elif elder_obj.status == 'Un-Available':
                messages.warning(request, 'Your status is showing Un-Available. Please change your status from the profile page and then you can approve')
            
                return redirect(reverse('care_request_sender_profile_page' , args=(user_id,)))
            
        # If pre-checks are passed then approve the request and do the below modifications
            else:
                #1 change the status of elder 
                elder_obj.change_status()
                elder_obj.care_giver = youngster_obj
                elder_obj.save()
                
                #2 increase the elder in care of youngster
                youngster_obj.change_elder_in_care_value()
                youngster_obj.save()

                #3. Once a care request is approved, remove it from the database
                care_request = CareRequest.objects.get(sender=youngster_obj, requested_for=elder_obj)
                care_request.delete()
                
                return redirect(reverse_lazy('care_request_queue_page'))



class set_funds_view(UpdateView):
    model = Elder
    template_name = "care_all/set_funds_page.html"
    fields = ['funds']



# ****************************  ****************************  ****************************
#   **************************** Youngster Functionalities **************************** 
# ****************************  ****************************  ****************************

class edit_youngster_profile_view(UpdateView):
    model = Youngster
    template_name = "care_all/edit_profile_page.html"
    fields = ['profile_photo', 'name', 'age', 'elders_in_care', 'bio']



class show_available_elders_view(ListView):
    model = Elder
    queryset = Elder.objects.filter(status='Available')
    context_object_name = 'elders'
    template_name = 'care_all/show_available_elders_page.html'



class show_un_available_elders_view(ListView):
    model = Elder
    queryset = Elder.objects.filter(status='Un-Available')
    context_object_name = 'elders'
    template_name = 'care_all/show_available_elders_page.html'



def available_elders_profile_view(request, *args, **kwargs):
    #Profile functionality
    elder_id = kwargs['pk']
    elder = Elder.objects.get(id=elder_id)

    #Listing Review functionality
    reviews = Reviews.objects.filter(review_written_for_elder=elder)
    
    if request.method == 'GET':
        review_form = WriteReviewForm()
        
    #Writing Review functionality
    else:
        review_form = WriteReviewForm(request.POST)
        
        if review_form.is_valid():
            review_form.save()

            #Getting review writer and review written for OBJECTS
            youngster_obj = Youngster.objects.get(user=request.user)
            elder_obj = elder

            #Fetching the current review to further update its values
            current_review_subject = review_form.cleaned_data['review_subject']
            current_review = Reviews.objects.get(review_subject=current_review_subject)

            #Updating the review writer and review written for
            current_review.review_writer_youngster = youngster_obj
            current_review.review_written_for_elder = elder_obj
            current_review.save()
            
            messages.success(request, 'Your review has been posted. Thanks !')

        else:
            messages.error(request, 'You need to write Subject, Comment and give the Rating to submit your review. All three are required')
            # print(review_form.errors)

    return render(request, 'care_all/available_elders_profile_page.html', context = {"elder":elder, "reviews":reviews, "review_form":review_form}) 



class send_care_request_view(View):
    def get(self, request, **kwargs):
           
        requested_for_id = (kwargs.get('pk'))
        
        sender = Youngster.objects.get(user = request.user)
        requested_for = Elder.objects.get(id = requested_for_id)
        
        try:
            care_request_exist = CareRequest.objects.get(sender = sender, requested_for=requested_for)
            messages.warning(request, 'You have already sent a Care Request to this individual')
            
        except:
            if sender.elders_in_care >= 4 :
                messages.warning(request, 'Youngster can only take care of 4 elders at a time')

            elif requested_for.status == 'Un-Available':
                messages.warning(request, 'Elder is Un-Available at this moment. Please checkback later')
            
            else:
                care_request = CareRequest.objects.create(sender = sender, requested_for = requested_for)
                messages.warning(request, 'Care Request Sent !')
                
        return redirect(reverse_lazy('show_available_elders_page'))



def elder_in_care_view(request):
    user = request.user
    youngster_obj = Youngster.objects.get(user=user)
    elders = Elder.objects.filter(care_giver=youngster_obj)
    
    return render(request, 'care_all/elder_in_care_page.html', context = {'elders':elders , 'youngster':youngster_obj})



def my_earnings_view(request):
    user = request.user
    youngster_obj = Youngster.objects.get(user=user)

    elder_obj = Elder.objects.filter(care_giver=youngster_obj)

    #Calculation youngster Earnings
    my_earnings = 0
    for elder in elder_obj:
        my_earnings += elder.funds

    return render(request, 'care_all/my_earnings_page.html' , context={'my_earnings': my_earnings, 'youngster': youngster_obj})