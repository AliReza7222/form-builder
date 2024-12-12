# Form Fields
# ------------------------------------------------------------------------------
FORM_GENERAL_FIELDS = ("title",)
FORM_READONLY_FIELDS = (
    "created_by",
    "created_at",
    "updated_by",
    "updated_at",
)
FORM_DISPLAY_FIELDS = (
    "title",
    "created_by",
    "created_at",
)
FORM_SEARCH_FIELDS = (
    "title",
    "created_by__username",
)
