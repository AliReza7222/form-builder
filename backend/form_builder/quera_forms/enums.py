from form_builder.base.enums import BaseEnum


class QuestionTypeEnum(BaseEnum):
    SHORT_TEXT = "Short Text"
    LONG_TEXT = "Long Text"
    EMAIL = "Email"
    NUMBER = "Number"


class TabFormAdminPanel(BaseEnum):
    GENERAL = "General"
    INFO = "Info"
