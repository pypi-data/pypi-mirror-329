from django.db import models
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField
from django.utils.html import strip_tags
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

# Create your models here.
cloudinary_url = "https://res.cloudinary.com/dkcjpdk1c/image/upload/"


class CompanyInfo(models.Model):
    logo = CloudinaryField(null=True, blank=True)
    get_page_header_image = models.URLField(default="")
    company_name = models.CharField(max_length=100, null=True, blank=True)
    company_address = models.CharField(
        max_length=255, null=True, blank=True)
    telephone = models.CharField(max_length=15, validators=[
        RegexValidator(r'^\d{11}$', 'Enter a valid phone number.')], null=True, blank=True)
    telephone_2 = models.CharField(max_length=15, null=True, blank=True, validators=[
        RegexValidator(r'^\d{11}$', 'Enter a valid phone number.')])
    email = models.EmailField(null=True, blank=True)
    about_company = RichTextField(blank=True, null=True)
    about_company_img = CloudinaryField(null=True, blank=True)
    return_policy = RichTextField(blank=True, null=True)
    term_and_conditions = RichTextField(blank=True, null=True)
    privacy_policy = RichTextField(blank=True, null=True)
    ceo_statment = RichTextField(null=True, blank=True)
    ceo_img = CloudinaryField(null=True, blank=True)

    def get_logo(self):
        return f"{cloudinary_url}{self.logo}"

    def get_about_img(self):
        return f"{cloudinary_url}{self.about_company_img}"

    def get_ceo_img(self):
        return f"{cloudinary_url}{self.ceo_img}"


class ServiceCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"


class Service(models.Model):
    title = models.CharField(max_length=50)
    description = RichTextField()
    image = CloudinaryField()
    category = models.ManyToManyField(ServiceCategory, blank=True, null=True)
    slug = models.SlugField(max_length=250, blank=True, null=True)

    def __str__(self):
        return f"{self.title}"

    def get_image_url(self):
        return f"{cloudinary_url}{self.image}"

    def safe_description_html(self):
        return strip_tags(self.description)


class ProductCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    title = models.CharField(max_length=50)
    description = RichTextField()
    image = CloudinaryField()
    hero_image = CloudinaryField(blank=True, null=True)
    hero_snippet = models.TextField(blank=True, null=True)
    category = models.ManyToManyField(ProductCategory)
    slug = models.SlugField(max_length=250, blank=True, null=True)

    def __str__(self):
        return f"{self.title}"

    def get_image_url(self):
        return f"{cloudinary_url}{self.image}"

    def get_hero_image_url(self):
        return f"{cloudinary_url}{self.hero_image}"

    def safe_description_html(self):
        return strip_tags(self.description)


class ContactForm(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    full_name = models.CharField(max_length=50)
    email = models.EmailField()
    # subject = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    message = RichTextField()

    def __str__(self):
        return f"{self.full_name}"

    class Meta:
        verbose_name_plural = "Contact Forms"


class EmailSubcription(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    email = models.EmailField()

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name_plural = "Email Subcriptions"


class OurClient(models.Model):
    name_of_client = models.CharField(max_length=50)
    logo = CloudinaryField()

    def __str__(self):
        return f"{self.name_of_client}"

    def get_logo_url(self):
        return f"{cloudinary_url}{self.logo}"


class OurSponsor(models.Model):
    name_of_sponsor = models.CharField(max_length=50)
    logo = CloudinaryField()

    def __str__(self):
        return f"{self.name_of_sponsor}"

    def get_logo_url(self):
        return f"{cloudinary_url}{self.logo}"


class Stat(models.Model):
    stat_figure = models.IntegerField()
    stat_title = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.stat_title} - {self.stat_figure}"


class Testimonial(models.Model):
    name = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    message = RichTextField()
    image = CloudinaryField()

    def __str__(self):
        return f"{self.name} - {self.position}"

    def get_image_url(self):
        return f"{cloudinary_url}{self.image}"


class OurTeam(models.Model):
    name = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    image = CloudinaryField()

    def __str__(self):
        return f"{self.name} - {self.position}"

    def get_image_url(self):
        return f"{cloudinary_url}{self.image}"


class SocialUrl(models.Model):
    company = models.OneToOneField(
        CompanyInfo, related_name='company_social', on_delete=models.CASCADE, blank=True, null=True)
    facebook_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)
    whatsapp_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.company} Social URLs"


class FAQ(models.Model):
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="faqs", blank=True, null=True)
    company = models.ForeignKey(
        CompanyInfo, related_name='company_faqs', on_delete=models.CASCADE, blank=True, null=True)
    faq_question = models.CharField(max_length=50)
    faq_answer = RichTextField()

    def __str__(self):
        return f"{self.service} {self.company} - {self.faq_question}"

    def clean(self):
        if self.service and self.company:
            raise ValidationError(
                "Only one of service and company can be selected.")


class CoreValue(models.Model):
    pic_url = models.URLField(
        default='https://img.freepik.com/premium-photo/compass-with-arrow-marks-word-mission_207634-2241.jpg?size=626&ext=jpg&ga=GA1.1.1699289041.1668069491&semt=ais')
    title = models.CharField(max_length=50)
    description = RichTextField()

    def __str__(self):
        return f"{self.title}"


class HeroSection(models.Model):
    title = models.CharField(max_length=50)
    description = RichTextField()
    image = CloudinaryField()

    def get_image_url(self):
        return f"{cloudinary_url}{self.image}"

    def __str__(self):
        return f"{self.title}"


class Event(models.Model):
    date_added = models.DateField(auto_now_add=True)
    image = CloudinaryField('image')
    title = models.CharField(max_length=32)
    body = RichTextField()
    event_date = models.DateField()
    slug = models.SlugField(max_length=250, blank=True, null=True)

    def safe_body_html(self):
        return strip_tags(self.body)

    def get_image_url(self):
        return f"{cloudinary_url}{self.image}"

    def __str__(self):
        return f"{self.title}"


class YouTubeVideo(models.Model):
    title = models.CharField(max_length=255, help_text="Title of the video")
    description = models.TextField(
        blank=True, help_text="Optional video description")
    video_url = models.URLField(help_text="URL of the YouTube video")
    embed_code = models.TextField(
        blank=True, help_text="Optional HTML embed code for the video")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

    def get_embed_url(self):
        """
        If embed_code is not provided, this method attempts to generate
        the YouTube embed URL from the video_url.
        Example: https://www.youtube.com/watch?v=VIDEO_ID becomes
        https://www.youtube.com/embed/VIDEO_ID
        """
        import re
        # Regex to extract the video ID from various YouTube URL formats.
        pattern = re.compile(
            r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
        )
        match = pattern.search(self.video_url)
        if match:
            video_id = match.group(1)
            return f'https://www.youtube.com/embed/{video_id}'
        return self.video_url  # fallback if not matched


class PhotoGallery(models.Model):
    title = models.CharField(max_length=50)
    photo = CloudinaryField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        ordering = ['-created_at']

    def get_photo_url(self):
        return f"{cloudinary_url}{self.photo}"
