from typing import Any, Iterable
from django.db import models
from django.utils.text import slugify
import uuid
from shortuuid.django_fields import ShortUUIDField
from django.conf import settings
from django.utils import timezone
# from django.contrib.contenttypes.models import ContentType
# from django.contrib.contenttypes.fields import GenericForeignKey


class BusinessManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_approved=True)
        return queryset

class BusinessProfile(models.Model):
    id = ShortUUIDField(
        length=22,
        max_length=40,
        alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-",
        primary_key=True,
        editable=False
    )
    owner = models.ForeignKey("accounts.BusinessAccount", on_delete=models.CASCADE, related_name='business_profile')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='branches')
    name = models.CharField(max_length=255, unique=True, null=True, blank=True, help_text="The brand name of the business.")
    slug = models.SlugField(max_length=255, unique=True, editable=False, db_index=True, null=True, blank=True)
    categories = models.ManyToManyField('BusinessCategory', related_name='businesses', blank=True)
    description = models.TextField()    
    
    address = models.CharField(max_length=255, help_text="The street address of the business location.", blank=True, null=True)
    city = models.CharField(max_length=100, help_text="The city or town where the business is located.")
    state = models.CharField(max_length=100, help_text="State, District or province where the business is located.")
    postal_code = models.CharField(max_length=20, help_text="The postal code of the business location.", blank=True, null=True)
    country = models.CharField(max_length=100, help_text="Country Where your business is located at")
    
    # average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    # total_reviews = models.PositiveIntegerField(default=0)

    is_verified = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    
    have_branches = models.BooleanField(default=False)
    
    def get_average_rating(self):
        return self.objects.reviews.filter()
    
    @property
    def get_location(self):
        return f"{self.city} {self.state}, {self.country}"
        
    @property
    def reviews_count(self):
        return self.reviews.count()

    # approved = BusinessManager()
    objects = models.Manager()


    def save(self, *args, **kwargs):
        if self.name and self.city and self.state and self.country:
            self.slug = slugify((self.name, self.city, self.state, self.country))
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Business profile'
        verbose_name_plural = 'Business profiles'
        # unique_together = ('name', 'review')

    def __str__(self):
        if self.name:
            return self.name

class BusinessSubscription(models.Model):
    business = models.OneToOneField(BusinessProfile, on_delete=models.CASCADE, related_name='subscription')
    subscribed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.business.name} - {'Subscribed' if self.subscribed else 'Unsubscribed'}"

class BusinessServices(models.Model):
    business = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=155)
    
    
    def __str__(self) -> str:
        return f"{self.name} ({self.business.name})"
    
    def save(self, *args, **kwargs):
        if not self.business.subscription.subscribed:
            service_count = BusinessServices.objects.filter(business=self.business).count()
            if service_count >= 5:
                raise ValueError("Unsubscribed businesses can only have up to 5 services.")
        super(BusinessServices, self).save(*args, **kwargs)
    
    

# class BusinessShortMessage(models.Model):
#     business = models.OneToOneField(BusinessProfile, on_delete=models.CASCADE, related_name='short_message')
#     message = models.CharField(max_length=160, help_text='A short message about the business. This message is displayed on the business profile page.')

#     def __str__(self):
#         return f'{self.business.name} short message'


class BusinessMedia(models.Model):
    business = models.OneToOneField(BusinessProfile, on_delete=models.CASCADE, related_name='media')
    logo = models.ImageField(upload_to='business/logos/', blank=True, null=True)
    banner = models.ImageField(upload_to='business/banners/', blank=True, null=True)

    def __str__(self):
        return f'{self.business.name} media'

class BusinessContact(models.Model):
    business = models.OneToOneField(BusinessProfile, on_delete=models.CASCADE, related_name='contact')

    phone = models.CharField(max_length=20, help_text='A valid phone number, please. This phone number is used for contact purposes if there is any enquiry.')
    email = models.EmailField(max_length=255, help_text='A valid email address, please. This email is used for contact purposes if there is any enquiry.')
    website = models.URLField(max_length=255, blank=True, null=True, help_text='A valid URL make sure to include http:// or https://.')
    
    def __str__(self) -> str:
        return f"{self.business.name} contacts"


class BusinessSocialMedia(models.Model):
    business = models.ForeignKey(BusinessProfile, related_name='social_media', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, help_text='The name of the social media platform.')
    url = models.URLField(max_length=255, help_text='A valid URL make sure to include http:// or https://.')

    def __str__(self):
        return f'{self.name}'   

class BusinessMapLocation(models.Model):
    business = models.OneToOneField(BusinessProfile, on_delete=models.CASCADE, related_name='location')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return f'{self.address}, {self.city}, {self.state}, {self.postal_code}, {self.country}'
    
class BusinessCategory(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)
    # slug = models.SlugField(blank=True)
    svg_icon = models.FileField(upload_to='category_icons/', null=True, blank=True)

    class Meta:
        unique_together = ('name', 'parent')

    def __str__(self):
        return self.name

    # def save(self):
    #     if self.name:
    #         self.slug = slugify((self.name))
    #     return super().save()

    def get_full_path(self):
        """
        Returns the full path of categories from root to the current category.
        """
        if self.parent:
            return f'{self.parent.get_full_path()} > {self.name}'
        return self.name
    
class BusinessHours(models.Model):

    DAYS = (
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    )

    business = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='hours')
    day = models.CharField(max_length=10, choices=DAYS)
    opening = models.TimeField()
    closing = models.TimeField()

    def __str__(self):
        return f'{self.business.name} hours'


class BusinessQuestionManager(models.Manager):
    pass
    
class BusinessQuestions(models.Model):
    asker = models.ForeignKey('accounts.PersonalAccount', on_delete=models.CASCADE, related_name='asked_questions')
    business = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='questions')
    question = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f"Question by {self.user.get_full_name()} on {self.business.name}"
    
class BusinessAnswer(models.Model):
    # answ
    question = models.ForeignKey('BusinessQuestions', on_delete=models.CASCADE, related_name="answer")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Answer by {self.user.get_full_name()} on {self.question.text[:30]}"
    
    
    
    
# Reviews and Ratings
class BusinessReview(models.Model):
    id = ShortUUIDField(
        length=32,
        max_length=40,
        alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-",
        primary_key=True,
        editable=False
    )
    business = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('accounts.PersonalAccount', on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(help_text="Rate the business from 1 to 5 stars.", default=0)
    title = models.CharField(max_length=100, help_text="Title your review")
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('-created_at',)
        
        
    @classmethod
    def get_weighted_average(cls, business):
        reviews = cls.objects.filter(business=business)
        weighted_sum = 0
        total_weight = 0
        
        for review in reviews:
            time_weight = cls.get_time_weight(review.created_at)
            user_weight = cls.get_user_weight(review.user)
            
            weight = (time_weight + user_weight) / 2
            
            weighted_sum += review.rating * weight
            total_weight += weight
        
        return weighted_sum / total_weight if total_weight else 0
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if is_new:
            self.user.profile.calculate_reputation()
        return super().save()

    
    
    
        # static Methods
    @staticmethod
    def get_time_weight(review_date):
        age = timezone.now() - review_date
        if age <= timezone.timedelta(days=30):
            return 1.5
        elif age <= timezone.timedelta(days=90):
            return 1.2
        elif age <= timezone.timedelta(days=180):
            return 1.0
        else:
            return 0.8

    @staticmethod
    def get_user_weight(user):
        if user.profile.reputation >= 1000:
            return 1.5
        elif user.profile.reputation >= 500:
            return 1.2
        elif user.profile.reputation >= 100:
            return 1.0
        else:
            return 0.8
    
    
    @property 
    def helpful_count(self):
        return self.reactions.filter(helpful=True).count()
    
    @property
    def reviews_count(self):
        return self.reviews.count()
    
    def __str__(self):
        return f"Review by {self.user.get_full_name()} for {self.business.name}"

class ReplyReview(models.Model):
    review = models.ForeignKey(BusinessReview, on_delete=models.CASCADE, related_name='replies')
    owner = models.ForeignKey('accounts.BusinessAccount', on_delete=models.CASCADE)
    reply = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Reply by {self.owner.get_full_name()} to review {self.review.id}"
    
    def save(self, *args, **kwargs):
        if self.owner != self.review.business.owner:
            raise PermissionError('Only the business owner can reply to they business profile reviews.')
        else:
            return super().save(*args, **kwargs)


class ReviewHelpful(models.Model):
    user = models.ForeignKey('accounts.PersonalAccount', on_delete=models.CASCADE, related_name='reactions')
    review = models.ForeignKey(BusinessReview, on_delete=models.CASCADE, related_name='reactions')
    helpful = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'review')
        
    def __str__(self):
        return f"{self.user.get_full_name()} reacted on {self.review}"
    
# class Event(models.Model):
#     business = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     start_time = models.DateTimeField()
#     end_time = models.DateTimeField()
#     location = models.CharField(max_length=255)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     image = models.ImageField(upload_to='event_images/', blank=True, null=True)

# class Promotion(models.Model):
#     business = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE)
#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     discount = models.DecimalField(max_digits=5, decimal_places=2)
#     start_date = models.DateField()
#     end_date = models.DateField()
#     terms_and_conditions = models.TextField(blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

    
# class ReportReviewOrReply(models.Model):
#     id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
#     review = models.ForeignKey(BusinessReview, on_delete=models.CASCADE, related_name='reports')
#     reply = models.ForeignKey(ReplyReview, on_delete=models.CASCADE, related_name='reports')
#     reason = models.TextField()
#     created = models.DateTimeField(auto_now_add=True)