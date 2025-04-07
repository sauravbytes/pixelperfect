from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

from dataclasses import dataclass


@dataclass
class SeoMeta:
    """
    A class for wrapping seo meta details.
    Fields: title, seo_title, canonical_url, keywords, search_image, description
    """
    title: str
    seo_title: str = None
    canonical_url: str = None
    keywords: str = None
    search_image: str = None
    description: str = None
    author: str = None
    site: str = 'Stotra Ratnavali'
    type: str = None
    page: str = None

    def __post_init__(self):
        if not self.seo_title:
            self.seo_title = self.title



# Create your models here.


class BaseMetaData(models.Model):
    """
    This abstract model contains the most essential meta tags for SEO.
    It includes fields for the page title, SEO title, meta description, keywords,
    search image, and canonical page and URL.
    """

    class Meta:
        abstract = True

    title = models.CharField(max_length=100)
    seo_title = models.CharField(max_length=200, null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)
    keywords = models.TextField(null=True, blank=True)
    search_image = models.ImageField(null=True, blank=True)
    is_canonical_page = models.BooleanField(default=True)
    canonical_url = models.URLField(null=True, blank=True)

    def clean_fields(self, exclude=None):
        canonical_error_message = 'Please either set this page as canonical page or enter canonical url'

        if self.is_canonical_page and not self.canonical_url:
            return

        if not self.is_canonical_page and self.canonical_url:
            return

        raise ValidationError(canonical_error_message)

    def get_canonical_url(self,request):
        if self.is_canonical_page:
            return request.build_absolute_uri
        else:
            return self.canonical_url



class AuthorMetaData(models.Model):
    """
    This abstract model contains additional meta tags for the page author.
    It includes a boolean field for showing the author and a foreign key to the author's user model.
    """

    class Meta:
        abstract = True

    show_author = models.BooleanField(default=False)
    author = models.ForeignKey(to=get_user_model(), null=True, blank=True, on_delete=models.SET_NULL)


class SeoMetaData(BaseMetaData, AuthorMetaData):
    """
    This abstract model combines the most essential meta tags and the page author details.
    """

    class Meta:
        abstract = True


class FixedPageMetaData(BaseMetaData):
    url = models.TextField()

    def __str__(self):
        """
        This title comes from BaseMetaData
        """

        return self.title
