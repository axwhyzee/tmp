from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Iterable


@dataclass
class TestField:
    mutator: Callable[[str], None]
    help_text: str
    field_name: str = '' # to be derived from mutator.__name__
    examples: Iterable[str] = field(default_factory=lambda:[])

    def __post_init(self):
        """Performs 2 main actions
        
        1) Add examples to help_text in a standardised way
        
            <help_text>
            Examples:
            ├ example 1
            └ example 2

        2) Derive field_name from mutator
        """
        if self.examples:
            self.help_text += "Examples:"
            self.help_text += '\n ├ '.join(self.examples[:-1])
            self.help_text += '\n └ ' + self.examples[-1]

        if not self.field_name:
            self.field_name = self.mutator.__name__.split('_set', maxsplit=1)[1]


class TestFieldValidationError(Exception):
    pass


class TestName(str, Enum):
    TSS_GENERAL = 'TSS_GENERAL'
    TSS_DAYS_START = 'TSS_DAYS_START'