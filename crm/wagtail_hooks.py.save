from wagtail.core import hooks
from wagtail.admin.menu import MenuItem
from django.urls import path
from django.shortcuts import render

@hooks.register("register_admin_urls")
def register_medical_tourism_guide_url():
    return [
        path(
            "medical-tourism-guide/",
            medical_tourism_guide_view,
            name="medical_tourism_guide",
        ),
    ]

def medical_tourism_guide_view(request):
    return render(request, "wagtail_hooks/medical_tourism_guide.html")

@hooks.register("register_settings_menu_item")
def register_medical_tourism_guide_menu():
    return MenuItem(
        "Medical Tourism Guide",
        "/admin/medical-tourism-guide/",
        classnames="icon icon-doc-full",
    )
