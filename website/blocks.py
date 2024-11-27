from wagtail import blocks
from wagtail.contrib.forms.models import AbstractEmailForm
from wagtail.contrib.forms.blocks import FormChooserBlock

class FooterFormBlock(blocks.StructBlock):
    """
    Custom block for embedding a form in the footer.
    """
    form = FormChooserBlock(required=True, label="Select a Form")

    class Meta:
        template = "blocks/footer_form_block.html"
        icon = "form"
        label = "Footer Form"
