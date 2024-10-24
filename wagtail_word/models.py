from coderedcms.models import CoderedArticlePage
from wagtail.admin.panels import FieldPanel, ObjectList, TabbedInterface
from wagtail.fields import RichTextField
from django.db import models
from django.utils.translation import gettext_lazy as _
from .forms import WagtailWordPageForm

class BaseWordDocumentPage(CoderedArticlePage):
    """
    Inherit directly from CoderedArticlePage to avoid multiple inheritance conflicts.
    This keeps the article functionality intact while adding Word document upload functionality.
    """
    base_form_class = WagtailWordPageForm
    allow_styling = False

    file = models.FileField(upload_to='documents/', blank=True, null=True)  # File upload for the Word document

    # Override body to use the RichTextField with the desired features
    body = RichTextField(
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

    # Panels for handling file upload and title first
    content_panels = CoderedArticlePage.content_panels + [
        FieldPanel('file'),  # File upload panel
    ]

    # Edit panels for handling content after conversion
    edit_panels = [
        FieldPanel('body'),
    ]

    # Tabbed interface: first for uploading, then editing content, then the CodeRed article features
    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading=_('Upload')),  # First: file upload and title
        ObjectList(edit_panels, heading=_('Edit')),  # Then: editing the RichTextField after conversion
        ObjectList(CoderedArticlePage.promote_panels, heading=_('Promote')),  # Article promotion panels
        ObjectList(CoderedArticlePage.settings_panels, heading=_('Settings')),  # Settings panels
    ])

    class Meta:
        verbose_name = _("Word Document Article")
        abstract = False

    parent_page_types = ["website.ArticleIndexPage"]

    search_template = "coderedcms/pages/article_page.search.html"

    def set_content(self, content: str):
        """
        This method will be called after the Word document is uploaded and processed.
        It sets the content in the RichTextField after conversion.
        """
        self.body = content
