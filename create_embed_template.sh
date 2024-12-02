#!/bin/bash

# Script to create Wagtail hook and template for embedding an iframe tutorial in the admin interface.
# It uses the "crm" app as the location for templates and hooks.

# Define app directory based on the project tree
APP_NAME="crm"
HOOKS_FILE="$APP_NAME/wagtail_hooks.py"
TEMPLATE_DIR="$APP_NAME/templates/wagtail_hooks"
TEMPLATE_FILE="$TEMPLATE_DIR/medical_tourism_guide.html"

# Create the template directory and file
echo "Creating template directory and file in app: $APP_NAME..."
mkdir -p "$TEMPLATE_DIR" || { echo "Failed to create template directory"; exit 1; }

cat > "$TEMPLATE_FILE" << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Medical Tourism Landing Page Guide</title>
</head>
<body>
    <iframe 
        src="https://scribehow.com/embed/Creating_a_Medical_Tourism_Landing_Page_Guide__ON0XbTipQwOn2YivGtGQtg?as=scrollable" 
        width="100%" 
        height="640" 
        allowfullscreen 
        frameborder="0">
    </iframe>
</body>
</html>
EOF
echo "Template created: $TEMPLATE_FILE"

# Create or append the Wagtail hooks file in the app directory
if [[ -f "$HOOKS_FILE" ]]; then
    echo "Appending to existing hooks file: $HOOKS_FILE"
else
    echo "Creating new hooks file: $HOOKS_FILE"
fi

cat >> "$HOOKS_FILE" << 'EOF'
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
EOF
echo "Hooks updated: $HOOKS_FILE"

# Final message
echo "Embed template and hook creation complete."
echo "Restart your Django server to see the changes."
