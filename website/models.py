"""
Create or customize your page models here.
"""

from coderedcms.forms import CoderedFormField
from coderedcms.models import CoderedArticleIndexPage
from coderedcms.models import CoderedArticlePage
from coderedcms.models import CoderedEmail
from coderedcms.models import CoderedEventIndexPage
from coderedcms.models import CoderedEventOccurrence
from coderedcms.models import CoderedEventPage
from coderedcms.models import CoderedFormPage
from coderedcms.models import CoderedLocationIndexPage
from coderedcms.models import CoderedLocationPage
from coderedcms.models import CoderedWebPage
from modelcluster.fields import ParentalKey


class ArticlePage(CoderedArticlePage):
    """
    Article, suitable for news or blog content.
    """

    class Meta:
        verbose_name = "Article"
        ordering = ["-first_published_at"]

    # Only allow this page to be created beneath an ArticleIndexPage.
    parent_page_types = ["website.ArticleIndexPage"]

    template = "coderedcms/pages/article_page.html"
    search_template = "coderedcms/pages/article_page.search.html"


class ArticleIndexPage(CoderedArticleIndexPage):
    """
    Shows a list of article sub-pages.
    """

    class Meta:
        verbose_name = "Article Landing Page"

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = None

    # Only allow ArticlePages beneath this page.
    subpage_types = ["website.ArticlePage","wagtail_word.BaseWordDocumentPage","CustomArticlePage"]

    template = "coderedcms/pages/article_index_page.html"

    def get_articles(self):
        # Returns all published ArticlePages beneath this index page.
        return self.get_children().specific().live().order_by('-first_published_at')

class EventPage(CoderedEventPage):
    class Meta:
        verbose_name = "Event Page"

    parent_page_types = ["website.EventIndexPage"]
    template = "coderedcms/pages/event_page.html"


class EventIndexPage(CoderedEventIndexPage):
    """
    Shows a list of event sub-pages.
    """

    class Meta:
        verbose_name = "Events Landing Page"

    index_query_pagemodel = "website.EventPage"

    # Only allow EventPages beneath this page.
    subpage_types = ["website.EventPage"]

    template = "coderedcms/pages/event_index_page.html"


class EventOccurrence(CoderedEventOccurrence):
    event = ParentalKey(EventPage, related_name="occurrences")


class FormPage(CoderedFormPage):
    """
    A page with an html <form>.
    """

    class Meta:
        verbose_name = "Form"

    template = "coderedcms/pages/form_page.html"


class FormPageField(CoderedFormField):
    """
    A field that links to a FormPage.
    """

    class Meta:
        ordering = ["sort_order"]

    page = ParentalKey("FormPage", related_name="form_fields")


class FormConfirmEmail(CoderedEmail):
    """
    Sends a confirmation email after submitting a FormPage.
    """

    page = ParentalKey("FormPage", related_name="confirmation_emails")


class LocationPage(CoderedLocationPage):
    """
    A page that holds a location.  This could be a store, a restaurant, etc.
    """

    class Meta:
        verbose_name = "Location Page"

    template = "coderedcms/pages/location_page.html"

    # Only allow LocationIndexPages above this page.
    parent_page_types = ["website.LocationIndexPage"]


class LocationIndexPage(CoderedLocationIndexPage):
    """
    A page that holds a list of locations and displays them with a Google Map.
    This does require a Google Maps API Key in Settings > CRX Settings
    """

    class Meta:
        verbose_name = "Location Landing Page"

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = "website.LocationPage"

    # Only allow LocationPages beneath this page.
    subpage_types = ["website.LocationPage"]

    template = "coderedcms/pages/location_index_page.html"


class WebPage(CoderedWebPage):
    """
    General use page with featureful streamfield and SEO attributes.
    """

    class Meta:
        verbose_name = "Web Page"

    template = "coderedcms/pages/web_page.html"


from django.db import models
from wagtailmedia.models import Media
from wagtailmedia.edit_handlers import MediaChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from coderedcms.fields import CoderedStreamField
from coderedcms.blocks import CONTENT_STREAMBLOCKS
from coderedcms.blocks import LAYOUT_STREAMBLOCKS
from coderedcms.blocks import STREAMFORM_BLOCKS
from coderedcms.blocks import ContentWallBlock
from coderedcms.fields import CoderedStreamField
from coderedcms.fields import ColorField
from coderedcms.forms import CoderedFormBuilder
from coderedcms.forms import CoderedSubmissionsListView
from coderedcms.models.snippet_models import ClassifierTerm
from coderedcms.models.wagtailsettings_models import LayoutSettings
from coderedcms.settings import crx_settings
from coderedcms.wagtail_flexible_forms.blocks import FormFieldBlock
from coderedcms.wagtail_flexible_forms.blocks import FormStepBlock
from coderedcms.wagtail_flexible_forms.models import SessionFormSubmission
from coderedcms.wagtail_flexible_forms.models import Step
from coderedcms.wagtail_flexible_forms.models import Steps
from coderedcms.wagtail_flexible_forms.models import StreamFormJSONEncoder
from coderedcms.wagtail_flexible_forms.models import StreamFormMixin
from coderedcms.wagtail_flexible_forms.models import SubmissionRevision
from coderedcms.widgets import ClassifierSelectWidget
from wagtail.search import index
from wagtail.search.index import SearchField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, FieldRowPanel, InlinePanel
from wagtail.admin.panels import ObjectList
from wagtail.admin.panels import TabbedInterface
from wagtail.utils.decorators import cached_classmethod
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from coderedcms.models import CoderedWebPage

from django.db import models
from wagtailmedia.models import Media
from wagtail.images.models import Image
from wagtail.admin.panels import FieldPanel
from wagtail.models import Orderable
from modelcluster.fields import ParentalKey
from coderedcms.models import CoderedWebPage
from wagtail.snippets.models import register_snippet

# Defining the snippets
@register_snippet
class AboutUsSnippet(models.Model):
    heading = models.CharField(max_length=255, help_text="Heading for the About Us section.")

    panels = [
        FieldPanel('heading'),
    ]

    class Meta:
        verbose_name = "About Us Section"
        verbose_name_plural = "About Us Sections"


@register_snippet
class ServiceSnippet(models.Model):
    title = models.CharField(max_length=255, help_text="Service title.")
    description = models.TextField(help_text="Service description.")
    icon_url = models.URLField(help_text="URL for the service icon image.")

    panels = [
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('icon_url'),
    ]

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"

@register_snippet
class PatientJourneySnippet(models.Model):
    name = models.CharField(max_length=255, help_text="Name of the patient.")
    journey_title = models.CharField(max_length=255, help_text="Title of the patient journey.")
    journey_subtitle = models.CharField(max_length=255, help_text="Subtitle of the patient journey.")
    story = models.TextField(help_text="Content of the patient story.")
    stories_link = models.URLField(help_text="URL for more patient stories.")
    read_more_text = models.CharField(max_length=255, help_text="Text for the 'Read More' button.")
    background_image = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Background image for the patient journey section."
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('journey_title'),
        FieldPanel('journey_subtitle'),
        FieldPanel('story'),
        FieldPanel('stories_link'),
        FieldPanel('read_more_text'),
        FieldPanel('background_image'),
    ]

    class Meta:
        verbose_name = "Patient Journey"
        verbose_name_plural = "Patient Journeys"

@register_snippet
class PricingSnippet(models.Model):
    price = models.CharField(max_length=255, help_text="Price for the pricing item.")
    title = models.CharField(max_length=255, help_text="Title of the pricing item.")
    features = models.TextField(help_text="Features for the pricing item, separated by commas.")
    is_premium = models.BooleanField(default=False, help_text="Mark this pricing item as premium.")
    details_link = models.URLField(help_text="Link to more details.")

    panels = [
        FieldPanel('price'),
        FieldPanel('title'),
        FieldPanel('features'),
        FieldPanel('is_premium'),
        FieldPanel('details_link'),
    ]

    class Meta:
        verbose_name = "Pricing Item"
        verbose_name_plural = "Pricing Items"

    def get_features_list(self):
        """Returns the features as a list of strings."""
        return self.features.split(',') if self.features else []

class doctorspage(CoderedWebPage):
    """
    Custom model for the homepage that includes a background video
    selected from uploaded media using the Wagtail media extension.
    """

    class Meta:
        verbose_name = "Our doctors"
        abstract = False

    template = "coderedcms/pages/doctors.html"

    # Video-related fields
    background_video = models.ForeignKey(
        Media,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Background video to be displayed in the video container."
    )
    scroll_link = models.URLField(null=True, blank=True, help_text="Link for the scroll icon.")
    scroll_icon_url = models.URLField(null=True, blank=True, help_text="URL for the scroll icon image.")

    # Panels for video-related fields
    content_panels = CoderedWebPage.content_panels + [
        FieldPanel("background_video"),
        FieldPanel("scroll_link"),
        FieldPanel("scroll_icon_url"),
    ]
#################################################################
from coderedcms.models import CoderedArticlePage
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
import uuid
from wagtail.models import TranslatableMixin, Locale
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel
from django.db import models

from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel
from django.db import models

from wagtail.models import TranslatableMixin
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from django.db import models
from wagtail.snippets.blocks import SnippetChooserBlock

class HocaPage(CoderedWebPage):
    """
    A page model to display Hoca snippets.
    """
    hoca_section = CoderedStreamField(
        [
            ('hoca', SnippetChooserBlock(target_model='website.Hoca')),  # Replace 'app_name' with your app's name
        ],
        blank=True,
        use_json_field=True,
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('hoca_section'),
    ]
    
    template = "coderedcms/pages/doctors.html"  # Update with your template path

    class Meta:
        verbose_name = "Hoca Page"

@register_snippet
class Hoca(TranslatableMixin, models.Model):
    number = models.IntegerField("Order Number", help_text="Number to control the order of display")
    name = models.CharField(max_length=255)
    specialty = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    photo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        FieldPanel('number'),
        FieldPanel('name'),
        FieldPanel('specialty'),
        FieldPanel('description'),
        FieldPanel('photo'),
    ]

    def __str__(self):
        return f"{self.number} - {self.name}"

# Modifying the CustomHomePage model to use snippets for the relevant sections
class CustomHomePage(CoderedWebPage):
    """
    Custom model for the homepage that includes a background video
    selected from uploaded media using the Wagtail media extension.
    """

    class Meta:
        verbose_name = "Custom Home Page"
        abstract = False

    template = "coderedcms/pages/home_page.html"

    # Video-related fields
    background_video = models.ForeignKey(
        Media,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Background video to be displayed in the video container."
    )
    scroll_link = models.URLField(null=True, blank=True, help_text="Link for the scroll icon.")
    scroll_icon_url = models.URLField(null=True, blank=True, help_text="URL for the scroll icon image.")

    about_us_section = CoderedStreamField(
        [
            ('about_us', SnippetChooserBlock(target_model='website.AboutUsSnippet')),
        ],
        blank=True,
        use_json_field=True,
    )

    services_section = CoderedStreamField(
        [
            ('service', SnippetChooserBlock(target_model='website.ServiceSnippet')),
        ],
        blank=True,
        use_json_field=True,
    )

    patient_journey_section = CoderedStreamField(
        [
            ('patient_journey', SnippetChooserBlock(target_model='website.PatientJourneySnippet')),
        ],
        blank=True,
        use_json_field=True,
    )

    pricing_section = CoderedStreamField(
        [
            ('pricing_item', SnippetChooserBlock(target_model='website.PricingSnippet')),
        ],
        blank=True,
        use_json_field=True,
    )

    portfolio_section = CoderedStreamField(
        [
            ('portfolio_item', SnippetChooserBlock(target_model='website.PortfolioSnippet')),
        ],
        blank=True,
        use_json_field=True,
    )


    # Panels for video-related fields
    content_panels = CoderedWebPage.content_panels + [
        FieldPanel("background_video"),
        FieldPanel("scroll_link"),
        FieldPanel("scroll_icon_url"),
        FieldPanel("about_us_section"),
        FieldPanel("services_section"),
        FieldPanel("patient_journey_section"),
        FieldPanel("pricing_section"),
        FieldPanel("portfolio_section"),

    ]


from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.models import Page
from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.snippets.models import register_snippet




@register_snippet
class PortfolioSnippet(models.Model):
    title = models.CharField(max_length=255, help_text="Title for the portfolio item.")
    description = models.TextField(help_text="Description for the portfolio item.")
    image = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Portfolio image."
    )

    panels = [
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('image'),
    ]

    class Meta:
        verbose_name = "Portfolio Item"
        verbose_name_plural = "Portfolio Items"





from coderedcms.models import CoderedArticlePage
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel

# Make sure to properly extend from CoderedArticlePage
class CustomArticlePage(CoderedArticlePage):
    # Adding custom body field or any other custom fields as needed
    content_body = RichTextField(
        blank=True,
        null=True,
        features=[
            "h1", "h2", "h3", "h4", "h5", "h6",
            "bold", "italic", "ol", "ul", "link",
            "document-link", "image", "embed",
            "code", "blockquote", "superscript",
            "subscript", "strikethrough",
            "hr", "ai"  # Custom AI feature
        ]
    )
    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    # Custom panels to be shown in the admin
    content_panels = CoderedArticlePage.content_panels + [
        FieldPanel('hero_image'),
        FieldPanel('content_body'),

    ]

    class Meta:
        verbose_name = "Custom Article Page"
        verbose_name_plural = "Custom Article Pages"

    template = "coderedcms/pages/custom_article_page.html"
    search_template = "coderedcms/pages/article_page.search.html"
    parent_page_types = ["website.ArticleIndexPage"]


from wagtail.fields import StreamField, RichTextField
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.panels import FieldPanel
from coderedcms.models import CoderedLocationPage

class CustomLocationPage(CoderedLocationPage):
    description = RichTextField(
        blank=True,
        help_text="Add a detailed description of the location."
    )

    images = StreamField(
        [
            ('image', ImageChooserBlock()),
        ],
        blank=True,
        help_text="Add multiple images."
    )

    content_panels = CoderedLocationPage.content_panels + [
        FieldPanel('description'),
        FieldPanel('images'),
    ]

    class Meta:
        verbose_name = "Hotel Page"

    template = "coderedcms/pages/custom_location_page.html"
    parent_page_types = ["website.CustomLocationIndexPage"]

class CustomLocationIndexPage(CoderedWebPage):
    """
    A custom index page for managing and displaying CustomLocationPage instances.
    """
    intro = RichTextField(
        blank=True,
        help_text="Optional introduction text for this index page."
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('intro'),
    ]

    subpage_types = ['CustomLocationPage']  # Replace 'yourapp' with the actual app name

    class Meta:
        verbose_name = "Custom Location Index Page"

    template = "coderedcms/pages/custom_location_index_page.html"
    def get_locations(self):
        """
        Returns all published CustomLocationPage instances beneath this index page.
        """
        return self.get_children().specific().live().order_by('-first_published_at')

from coderedcms.models import CoderedWebPage
from wagtail.fields import StreamField, RichTextField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.blocks import CharBlock, TextBlock, StructBlock, RichTextBlock
from wagtail.admin.panels import FieldPanel
from coderedcms.blocks import CONTENT_STREAMBLOCKS


class CustomDynamicPage(CoderedWebPage):
    """
    Page model to represent the dynamic content for the given HTML template.
    """

    class Meta:
        verbose_name = "Services Page"

    template = "coderedcms/pages/service.html"


    # Vegas Slide Section
    vegas_slides = StreamField(
        [
            ("slide_image", ImageChooserBlock(label="Slide Image")),
        ],
        blank=True,
        use_json_field=True,
        verbose_name="Vegas Slides",
        help_text="Upload images for the Vegas slider background.",
    )

    # Home Section
    home_content = StreamField(
        [
            ("title", CharBlock(label="Home Title", required=True)),
            ("subtitle", TextBlock(label="Home Subtitle", required=False)),
            ("button_text", CharBlock(label="Button Text", required=False)),
        ],
        blank=True,
        use_json_field=True,
        verbose_name="Home Section Content",
    )

    # About Section
    about_section = StreamField(
        [
            ("image", ImageChooserBlock(label="About Section Image")),
            ("title", CharBlock(label="About Title", required=True)),
            ("subtitle", CharBlock(label="About Subtitle", required=False)),
            ("text", RichTextBlock(label="About Text", required=False)),
        ],
        blank=True,
        use_json_field=True,
        verbose_name="About Section Content",
    )

    # Feature Section
    features = StreamField(
        [
            (
                "feature",
                StructBlock(
                    [
                        ("icon", CharBlock(label="Feature Icon", required=False)),
                        ("heading", CharBlock(label="Feature Heading", required=False)),
                        ("text", TextBlock(label="Feature Text", required=False)),
                    ],
                    label="Feature Block",
                ),
            ),
        ],
        blank=True,
        use_json_field=True,
        verbose_name="Features",
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel("vegas_slides"),
        FieldPanel("home_content"),
        FieldPanel("about_section"),
        FieldPanel("features"),
    ]

from coderedcms.models import CoderedWebPage
from wagtail.fields import StreamField
from wagtail.blocks import CharBlock, TextBlock, StructBlock, RichTextBlock, URLBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.panels import FieldPanel
from wagtail.blocks import ListBlock

class MedicalTourismPage(CoderedWebPage):
    """
    A landing page model for medical tourism services.
    """

    class Meta:
        verbose_name = "Medical Tourism Landing Page"

    template = "coderedcms/pages/service2.html"
    
    def get_medical_hotels(self):
        """
        Retrieves all CustomLocationPage instances to display on the page.
        """
        # Returns all live CustomLocationPage instances
        current_locale = self.locale
        return CustomLocationPage.objects.live().filter(locale=current_locale)

    # Hero Section
    hero_section = StreamField(
        [
            ("background_image", ImageChooserBlock(label="Background Image")),
            ("title", CharBlock(label="Hero Title", required=True)),
            ("subtitle", TextBlock(label="Hero Subtitle", required=False)),
            ("button_primary", StructBlock([
                ("label", CharBlock(label="Button Label", required=True)),
                ("url", URLBlock(label="Button URL", required=True)),
            ], label="Primary Button", required=False)),
            ("button_secondary", StructBlock([
                ("label", CharBlock(label="Button Label", required=True)),
                ("url", URLBlock(label="Button URL", required=True)),
            ], label="Secondary Button", required=False)),
        ],
        blank=True,
        use_json_field=True,
        verbose_name="Hero Section",
    )

    # About Section
    about_section = StreamField(
        [
            ("image", ImageChooserBlock(label="About Image")),
            ("title", CharBlock(label="About Title", required=True)),
            ("subtitle", CharBlock(label="About Subtitle", required=False)),
            ("text", RichTextBlock(label="About Description", required=False)),
        ],
        blank=True,
        use_json_field=True,
        verbose_name="About Section",
    )

    # Doctors/Specialists Section
    doctors_section = StreamField(
        [
            ("doctor", StructBlock([
                ("image", ImageChooserBlock(label="Doctor Image")),
                ("name", CharBlock(label="Name", required=True)),
                ("specialty", CharBlock(label="Specialty", required=True)),
                ("description", TextBlock(label="Description", required=False)),
                ("social_link", URLBlock(label="Social/Profile Link", required=False)),
            ], label="Doctor")),
        ],
        blank=True,
        use_json_field=True,
        verbose_name="Doctors Section",
    )

    dentists_section = CoderedStreamField(
        [
            ('hoca', SnippetChooserBlock(target_model='website.Hoca')),  # Replace 'app_name' with your app's name
        ],
        blank=True,
        use_json_field=True,
        verbose_name="Denrtists Section",
    )


    # Patient Journey Section
    patient_journey_section = StreamField(
        [
            ("day", StructBlock([
                ("day_label", CharBlock(label="Day Label", required=True)),
                ("description", RichTextBlock(label="Description", required=True)),
            ], label="Patient Journey Day")),
        ],
        blank=True,
        use_json_field=True,
        verbose_name="Patient Journey Section",
    )

    # Clinics/Hospitals Section
    clinics_section = StreamField(
        [
            ("clinic", StructBlock([
                ("image", ImageChooserBlock(label="Clinic Image")),
                ("name", CharBlock(label="Clinic Name", required=True)),
                ("location", CharBlock(label="Location", required=False)),
                ("description", TextBlock(label="Description", required=False)),
                ("map_link", URLBlock(label="Google Maps Link", required=False)),
            ], label="Clinic")),
        ],
        blank=True,
        use_json_field=True,
        verbose_name="Clinics Section",
    )

    # Pricing Section
    pricing_section = StreamField(
        [
            ("pricing_item", StructBlock([
                ("title", CharBlock(label="Package Title", required=True)),
                ("price", CharBlock(label="Price", required=True)),
                ("features", ListBlock(CharBlock(label="Feature"), label="Features List")),
                ("cta_label", CharBlock(label="Call to Action Label", required=True)),
                ("cta_url", URLBlock(label="Call to Action URL", required=True)),
            ], label="Pricing Item")),
        ],
        blank=True,
        use_json_field=True,
        verbose_name="Pricing Section",
    )

    # FAQ Section
    faq_section = StreamField(
        [
            ("faq", StructBlock([
                ("question", CharBlock(label="Question", required=True)),
                ("answer", RichTextBlock(label="Answer", required=True)),
            ], label="FAQ")),
        ],
        blank=True,
        use_json_field=True,
        verbose_name="FAQ Section",
    )

    # Gallery Section
    gallery_section = StreamField(
        [
            ("image", ImageChooserBlock(label="Gallery Image")),
        ],
        blank=True,
        use_json_field=True,
        verbose_name="Gallery Section",
    )

    # Content Panels for Admin Interface
    content_panels = CoderedWebPage.content_panels + [
        FieldPanel("hero_section"),
        FieldPanel("about_section"),
        FieldPanel("doctors_section"),
        FieldPanel('dentists_section'),
        FieldPanel("patient_journey_section"),
        FieldPanel("clinics_section"),
        FieldPanel("pricing_section"),
        FieldPanel("faq_section"),
        FieldPanel("gallery_section"),
    ]

from wagtail.snippets.models import register_snippet
from wagtail.fields import StreamField
from wagtail.blocks import StructBlock, CharBlock, RichTextBlock
from wagtail.admin.panels import FieldPanel

@register_snippet
class FAQ(models.Model):
    """
    Reusable FAQ Snippet
    """
    title = models.CharField(max_length=255, verbose_name="FAQ Title")
    faqs = StreamField(
        [
            ("faq", StructBlock([
                ("question", CharBlock(label="Question", required=True)),
                ("answer", RichTextBlock(label="Answer", required=True)),
            ], label="FAQ")),
        ],
        use_json_field=True,
        verbose_name="FAQs",
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("faqs"),
    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "FAQ Snippet"
        verbose_name_plural = "FAQ Snippets"

@register_snippet
class Sponsor(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    link = models.URLField(blank=True, null=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('logo'),
        FieldPanel('link'),
    ]

    def __str__(self):
        return self.name


from wagtail import blocks
from wagtail.snippets.models import register_snippet
from wagtail.models import TranslatableMixin
from django.db import models
from coderedcms.fields import CoderedStreamField
from coderedcms.blocks import BaseBlock
from django.utils.translation import gettext_lazy as _
from coderedcms.blocks.stream_form_blocks import (
    CoderedStreamFormCharFieldBlock,
    CoderedStreamFormTextFieldBlock,
    CoderedStreamFormCheckboxFieldBlock,
    CoderedStreamFormRadioButtonsFieldBlock,
    CoderedStreamFormDropdownFieldBlock,
    CoderedStreamFormFileFieldBlock,
    CoderedStreamFormImageFieldBlock,
)

from wagtail.snippets.models import register_snippet
from wagtail.models import TranslatableMixin
from wagtail import blocks
from coderedcms.fields import CoderedStreamField
from coderedcms.blocks import BaseBlock
from coderedcms.blocks.stream_form_blocks import (
    CoderedStreamFormCharFieldBlock,
    CoderedStreamFormTextFieldBlock,
    CoderedStreamFormCheckboxFieldBlock,
    CoderedStreamFormRadioButtonsFieldBlock,
    CoderedStreamFormDropdownFieldBlock,
)

@register_snippet
class LocalizedFooter(TranslatableMixin, models.Model):
    """
    Localized footer snippet for managing the entire footer, including contact.
    """
    name = models.CharField(max_length=255, verbose_name="Name")
    custom_css_class = models.CharField(max_length=255, blank=True, verbose_name="Custom CSS Class")
    custom_id = models.CharField(max_length=255, blank=True, verbose_name="Custom ID")
    template = "coderedcms/snippets/lfooter.html"  # Reference the template here

    content = CoderedStreamField([
        ("contact_info", blocks.StructBlock([
            ("address", blocks.TextBlock(label="Address", required=False)),
            ("phone", blocks.TextBlock(label="Phone", required=False)),
            ("email", blocks.EmailBlock(label="Email", required=False)),
        ], icon="placeholder", label="Contact Information")),

        ("map", blocks.RawHTMLBlock(label="Google Map Embed", required=False)),

        ("form", blocks.StreamBlock([
            ("char_field", CoderedStreamFormCharFieldBlock()),
            ("text_field", CoderedStreamFormTextFieldBlock()),
            ("checkbox_field", CoderedStreamFormCheckboxFieldBlock()),
            ("radio_buttons", CoderedStreamFormRadioButtonsFieldBlock()),
            ("dropdown", CoderedStreamFormDropdownFieldBlock()),
        ], verbose_name="Contact Form Fields", required=False)),

        ("links", blocks.ListBlock(
            blocks.StructBlock([
                ("text", blocks.CharBlock(label="Link Text")),
                ("url", blocks.URLBlock(label="Link URL")),
            ]),
            label="Useful Links"
        )),
    ], verbose_name="Footer Content", blank=True, use_json_field=True)

    panels = [
        FieldPanel("name"),
        MultiFieldPanel([
            FieldPanel("custom_css_class"),
            FieldPanel("custom_id"),
        ], heading="Attributes"),
        FieldPanel("content"),
    ]

    def __str__(self):
        return self.name


from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel
from coderedcms.fields import CoderedStreamField
from coderedcms.blocks import STREAMFORM_BLOCKS

@register_snippet
class FooterWithForm(models.Model):
    name = models.CharField(max_length=255, verbose_name="Footer Name")
    content = CoderedStreamField(STREAMFORM_BLOCKS, verbose_name="Footer Content")
    custom_css_class = models.CharField(max_length=255, blank=True, verbose_name="CSS Class")
    
    panels = [
        FieldPanel("name"),
        FieldPanel("content"),
        FieldPanel("custom_css_class"),
    ]

    def __str__(self):
        return self.name
