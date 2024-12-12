from .enums import QuestionTypeEnum
from .validators import (
    DefaultValidator,
    LongTextValidator,
    NumberValidator,
    ShortTextValidator,
)


class QuestionValidatorFactory:
    validators = {
        QuestionTypeEnum.SHORT_TEXT.name: ShortTextValidator(),
        QuestionTypeEnum.LONG_TEXT.name: LongTextValidator(),
        QuestionTypeEnum.NUMBER.name: NumberValidator(),
    }

    @classmethod
    def get_validator(cls, question_type):
        return cls.validators.get(question_type, DefaultValidator())
