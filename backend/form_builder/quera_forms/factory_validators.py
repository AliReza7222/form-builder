from abc import ABC, abstractmethod

from .enums import QuestionTypeEnum
from .validators import *


class BaseValidatorFactory(ABC):
    @abstractmethod
    def validators(self):
        pass

    @classmethod
    @abstractmethod
    def get_validator(cls, question_type):
        pass


class QuestionValidatorFactory(BaseValidatorFactory):
    def validators(self):
        return {
            QuestionTypeEnum.SHORT_TEXT.name: ShortTextValidator(),
            QuestionTypeEnum.LONG_TEXT.name: LongTextValidator(),
            QuestionTypeEnum.NUMBER.name: NumberValidator(),
        }

    @classmethod
    def get_validator(cls, question_type):
        return cls.validators.get(question_type, DefaultValidator())


class AnswerValidatorFactory(BaseValidatorFactory):
    def validators(self):
        return {
            QuestionTypeEnum.SHORT_TEXT.name: TextAnswerValidator(),
            QuestionTypeEnum.LONG_TEXT.name: TextAnswerValidator(),
            QuestionTypeEnum.EMAIL.name: EmailAnswerValidator(),
            QuestionTypeEnum.NUMBER.name: NumberAnswerValidator(),
        }

    @classmethod
    def get_validator(cls, question_type):
        return cls.validators.get(question_type)
