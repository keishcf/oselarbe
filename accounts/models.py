from django.db import models
from django.utils import timezone

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.text import slugify
from shortuuid.django_fields import ShortUUIDField
from authemail.models import EmailAbstractUser, EmailUserManager
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.functional import cached_property



class MyUserManager(EmailUserManager):
    
    def _create_user(self, email, password, is_staff, is_superuser,
                     is_verified, **extra_fields):
        """
        Creates and saves a User with a given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, is_staff=is_staff, is_active=True, is_superuser=is_superuser, is_verified=is_verified,last_login=now, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_business_account(self, email, password=None, **extra_fields):
        business_account = self._create_user(email, password, True, False, False,**extra_fields, is_business=True, is_personal=False)
        return business_account
        
    def create_personal_account(self, email, password=None, **extra_fields):
        personal_account = self._create_user(email, password, False, False, False,**extra_fields, is_personal=True, is_business=False)
        PersonalProfile.objects.create(user=personal_account)
        PersonalLocation.objects.create(user=personal_account)
        return personal_account

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, True,
                                 **extra_fields)

class User(EmailAbstractUser):
    id = ShortUUIDField(
        length=15,
        max_length=40,
        alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
        primary_key=True,
    )
    is_business = models.BooleanField(default=False)
    is_personal = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True, editable=False)
    
    objects = MyUserManager()


class PersonalManager(models.Manager):
    def create_user(self , email , password = None):
        if not email or len(email) <= 0 : 
            raise  ValueError("Email field is required !")
        if not password :
            raise ValueError("Password is must !")
        email  = email.lower()
        user = self.model(
            email = email
        )
        user.set_password(password)
        user.save(using = self._db)
        # PersonalProfile.objects
        return user
      
    def get_queryset(self , *args,  **kwargs):
        queryset = super().get_queryset(*args , **kwargs)
        queryset = queryset.filter(is_personal = True)
        return queryset
    
          


class PersonalAccount(User):
    class Meta:
        verbose_name = 'Personal account'
        verbose_name_plural = 'Personal accounts'
        proxy = True
        
    objects = PersonalManager()
    

class PersonalProfile(models.Model):
    user = models.OneToOneField(PersonalAccount, on_delete=models.CASCADE, related_name='profile', primary_key=True, editable=False, db_index=True)
    profile_picture = models.ImageField('Profile picture', upload_to='profile_pictures/', null=True, blank=True, help_text='Upload a profile picture')
    bio = models.TextField('Bio', null=True, blank=True, help_text='A short description about yourself')
    date_of_birth = models.DateField('Date of birth', null=True, blank=True, help_text='Your date of birth')
    nickname = models.CharField('Nickname', max_length=30, null=True, blank=True, help_text='Your nickname')
    headline = models.CharField('Headline', max_length=100, null=True, blank=True, help_text='A short headline about yourself')
    hometown = models.CharField('Hometown', max_length=100, null=True, blank=True, help_text='Your hometown')
    primary_language = models.CharField('Primary language', max_length=100, null=True, blank=True)
    web_url = models.URLField('Web URL', null=True, blank=True, help_text='Your website URL')
    country = models.CharField('Country', max_length=100, null=True, blank=True, help_text='Your country')
    
    # favoriting = models.ManyToManyField("business.BusinessProfile", related_name='Favorite', blank=True)
    
    @property
    def display_name(self):
        if self.user.first_name and self.user.last_name:
            return f'{self.user.get_full_name()}'
    
    @property
    def thumbsup_count(self):
        self.user.thumbsup_reviews.count()
    
    class Meta:
        verbose_name = 'Personal profile'
        verbose_name_plural = 'Personal profiles'
        
    
    def __str__(self):
        return self.user.email + ' Profile'



# class Favorite(models.Model):
#     from_personal = models.ForeignKey('accounts.PersonalAccount', on_delete=models.CASCADE, related_name='favorites')
#     to_business = models.ForeignKey("business.BusinessProfile", on_delete=models.CASCADE, related_name='favorited')
#     date_added = models.DateTimeField(auto_now_add=True)
    
#     class Meta:
#         unique_together = ('from_personal', 'to_business')
        
#     def save(self, *args, **kwargs):
#         if not isinstance(self.follower, PersonalAccount):
#             raise ValidationError("Only personal accounts can follow business profiles.")
#         if not isinstance(self.following.business_account, BusinessAccount):
#             raise ValidationError("Can only follow business profiles associated with business accounts.")
#         super().save(*args, **kwargs)
    
#     def __str__(self):
#         return f"{self.from_personal.email} favorite {self.to_business.name}"



class PersonalSocial(models.Model):
    user = models.ForeignKey(PersonalAccount, on_delete=models.CASCADE, related_name='social')
    name = models.CharField('Name', max_length=100, null=True, blank=True, help_text='Name of the social media')
    url = models.URLField('URL', null=True, blank=True, help_text='URL of the social media')

    class Meta:
        verbose_name = 'Personal profile social'
        verbose_name_plural = 'Personal profiles social'
    
    def __str__(self):
        return self.user.email + 'social'
    

class PersonalLocation(models.Model):
    user = models.OneToOneField(PersonalAccount, on_delete=models.CASCADE, related_name='location', primary_key=True, editable=False)
    name = models.CharField('Name', max_length=100, null=True, blank=True, help_text='Name of the location')
    city = models.CharField('City', max_length=100, null=True, blank=True, help_text='Your city')
    state = models.CharField('State', max_length=100, null=True, blank=True, help_text='Your state')
    country = models.CharField('Country', max_length=100, null=True, blank=True, help_text='Your country')
    zip_code = models.CharField('Zip code', max_length=100, null=True, blank=True, help_text='Your zip code')
    address = models.CharField('Address', max_length=100, null=True, blank=True, help_text='Your address')
    
    @property
    def get_full_address(self):
        if self.address and self.city and self.state and self.country and self.zip_code:
            return f'{self.address}, {self.city}, {self.state}'
    
    class Meta:
        verbose_name = 'Personal profile location'
        verbose_name_plural = 'Personal profiles location'
    
    def __str__(self):
        if self.user.get_full_name():
            return self.user.get_full_name() + 'location'
        return self.user.email +  ' Location'
            

# class PersonalCollection(models.Model):
#     user = models.ForeignKey(PersonalAccount, on_delete=models.CASCADE, related_name='collection', primary_key=True, editable=False)
#     name = models.CharField('Name', max_length=100, null=True, blank=True, help_text='Name of the collection')
#     description = models.TextField('Description', null=True, blank=True, help_text='Description of the collection')
#     date_created = models.DateTimeField('Date created', auto_now_add=True)
    
#     class Meta:
#         verbose_name = 'Personal profile collection'
#         verbose_name_plural = 'Personal profiles collection'
    
#     def __str__(self):
#         return self.user.username + 'collection'



# Business Account

class BusinessManager(models.Manager):
    def create_user(self , email , password = None):
        if not email or len(email) <= 0 : 
            raise  ValueError("Email field is required !")
        if not password :
            raise ValueError("Password is must !")
        email  = email.lower()
        user = self.model(
            email = email
        )
        user.set_password(password)
        user.save(using = self._db)
        return user
      
    def get_queryset(self , *args,  **kwargs):
        queryset = super().get_queryset(*args , **kwargs)
        queryset = queryset.filter(is_business = True)
        return queryset
    
    # def get_owner_profiles(self, owner_id, *args, **kwargs):
    #     queryset = self.model.business_profile.all()
    #     queryset = queryset.filter(owner__id=owner_id)
    #     return queryset
    


class BusinessAccount(User):

    objects = BusinessManager()

    class Meta:
        verbose_name = "Business Account"
        verbose_name_plural = "Business Accounts"
        proxy = True
    
    def __str__(self) -> str:
        return super().__str__()



# class CollectionManager(models.Manager):
#     def get_queryset(self, *args, **kwargs):
#         queryset = super().get_queryset(*args, **kwargs)
#         queryset = queryset.filter(public=True)
#         return queryset
    
#     def get_user_collections(self, user):
#         return self.filter(user=user)
    
#     def get_private_collections(self, user):
#         return self.filter(user=user, public=False)

# class Collection(models.Model):
#     id = ShortUUIDField(
#         length=18,
#         max_length=40,
#         alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-",
#         primary_key=True,
#         editable=False,
#     )
#     user = models.ForeignKey(PersonalAccount, on_delete=models.CASCADE, related_name='collection', editable=False)
#     slug = models.SlugField('Slug', max_length=255, unique=True, editable=False, db_index=True, null=True, blank=True)
#     name = models.CharField('Name', max_length=100, null=True, blank=True, help_text='Name of the collection')
#     description = models.TextField('Description', null=True, blank=True, help_text='Description of the collection')
#     date_created = models.DateTimeField('Date created', auto_now_add=True)
#     public = models.BooleanField('Public', default=True, help_text='Public or private collection')
#     businesses = models.ManyToManyField(BusinessProfile, related_name='collections', blank=True)
    
#     class Meta:
#         verbose_name = 'Collection'
#         verbose_name_plural = 'Collections'
#         indexes = [
#             models.Index(fields=['slug']),
#             models.Index(fields=['id'])
#         ]
    
#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(self.name)
#         super().save(*args, **kwargs)
    
#     def get_absolute_url(self):
#         return reverse("collection-detail", kwargs={"pk": self.pk, "slug": self.slug})
    
    
#     def __str__(self):
#         return f'{self.name} by {self.user.username}'
    
