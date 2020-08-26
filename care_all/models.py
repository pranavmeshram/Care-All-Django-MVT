from django.db import models
from accounts.models import User
from django.urls import reverse_lazy, reverse
# Create your models here.


class Youngster(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)    
    profile_photo = models.ImageField(upload_to='profile/user_profile_photo/', blank=True)
    name = models.CharField(max_length=150, blank=True, default='Anonymous')
    age = models.PositiveIntegerField(blank=True, null=True)
    elders_in_care = models.IntegerField(blank=True, null=True)
    bio = models.TextField(blank=True)


    def get_absolute_url(self):
        return reverse('show_profile_page', args=[self.id])


    def change_elder_in_care_value(self):
        self.elders_in_care += 1


    def __str__(self):
        if self.name:
            return self.name + " (Youngster-Profile)"
        return "Profile No." +" "+ str(self.id) 



class Elder(models.Model):

    statuses = [('Available','Available'), ('Un-Available','Un-Available')]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='profile/user_profile_photo/', blank=True)
    name = models.CharField(max_length=150, blank=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=statuses, default='Available')
    funds = models.IntegerField(blank=True, null=True)
    bio = models.TextField(blank=True)
    in_care = models.BooleanField(blank=True, default=False)
    care_giver = models.ForeignKey(Youngster, on_delete=models.SET_NULL, blank=True, null=True)
 

    def get_absolute_url(self):
        return reverse('show_profile_page', args=[self.id])


    def change_status(self):
        self.status = 'Un-Available'
        self.in_care = True


    def __str__(self):
        if self.name:
            return self.name + " (Elder-Profile)"
        return "Profile No." +" "+ str(self.id)



class CareRequest(models.Model):

    sender = models.ForeignKey(Youngster, on_delete=models.CASCADE)
    requested_for = models.ForeignKey(Elder, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Care Request'
        verbose_name_plural = 'Care Requests'

    def monthly_earnings(self):
        return self.requested_for.funds

    def __str__(self):
        return str(self.sender) + " ** sent request to ** " + str(self.requested_for)



class Reviews(models.Model):

    review_writer_youngster = models.ForeignKey(Youngster, on_delete=models.CASCADE, blank=True, null=True)
    review_written_for_elder = models.ForeignKey(Elder, on_delete=models.CASCADE, blank=True, null=True, related_name='for_elder')

    review_writer_elder = models.ForeignKey(Elder, on_delete=models.CASCADE, blank=True, null=True)
    review_written_for_youngster = models.ForeignKey(Youngster, on_delete=models.CASCADE, null=True, blank=True, related_name='for_youngster')

    review_subject = models.CharField(max_length=50)
    review_message = models.CharField(max_length=255, blank=True)
    review_rating = models.IntegerField(default=1)

    statuses = [('New','New'), ('True','True'), ('False','False')]

    review_status = models.CharField(max_length=5, choices=statuses, default='New')
    review_created_date = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'


    def __str__(self):
        if self.review_writer_youngster:
            return str(self.review_writer_youngster) + ' **written for** ' + str(self.review_written_for_elder)
        elif self.review_writer_elder:
            return str(self.review_writer_elder) + ' **written for** ' + str(self.review_written_for_youngster)
        else:
            return str(self.review_subject) + " ** ** " + str(self.review_rating) + " ** ** " + str(self.review_status)

