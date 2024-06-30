from typing import List, Literal

from models.common import TestField, TestFieldValidationError


class BaseTest:
    """Base test class that contains for all verification methods"""
    def __init__(self):
        self.name: str
        self.alert_message: str
        self.fields_to_prompt: List[TestField] = [
            TestField(
                mutator=self._set_name, 
                help_text="Name of test to convey purpose of test.",
                examples=["Verify >30 comments scraped"]
            ),
            TestField(
                mutator=self._set_alert_message, 
                help_text="Alert message should provide information helpful for debugging, like TSS source and table, catalog URL, possible reasons for failure of this test.",
                examples=["No EUREX data scraped over last 3 days. Please go to the subscriber dashboard at a7.dataplatform.com to check if there is data."]
            )
        ]

    def _set_name(self, name: str) -> None:
        MIN_CHARS: int = 5
        if len(name) < MIN_CHARS:
            raise TestFieldValidationError(
                f"\"{name}\" has less than {MIN_CHARS} characters. Set a more meaningful test name."
            )
        self.name = name


    def _set_alert_message(self, alert_message: str) -> None:
        MIN_CHARS: int = 10
        if len(alert_message) < MIN_CHARS:
            raise TestFieldValidationError(
                f"\"{alert_message}\" has less than {MIN_CHARS} characters. Set a more meaningful alert message."
            )
        self.alert_message = alert_message


class SQLTest(BaseTest):
    def __init__(self):
        super().__init__()
        self.db_name: str
        self.verification_command: str
        self.fields_to_prompt.extend([
            TestField(
                mutator = self._set_db_name,

            )
        ])


    def _set_db_name(self, db_name: str) -> None:
        if not db_name:
            raise TestFieldValidationError("<db_name> is required.")
        self.db_name = db_name

    
    def _set_verification_command(self, verification_command: str) -> None:
        # TODO
        # verify sql query
        self.verification_command = verification_command


class TSSTest(BaseTest):
    QUERY_TYPE = Literal["all", "last_by_ref"]

    def __init__(self):
        super().__init__()
        self.query_type: self.QUERY_TYPE
        self.source: str
        self.table: str
        self.min: int = 1
        self.limit: int = 1
        self.fields_to_prompt.extend([
            TestField(
                mutator=self._set_query_type,
                help_text="TSS query method to use in your verifier test",
                examples=["all", "last_by_ref"]
            )
        ])


    def _set_query_type(self, query_type: QUERY_TYPE) -> None:
        if query_type not in self.QUERY_TYPE.__args__:
            raise TestFieldValidationError(f"Expected {self.QUERY_TYPE.__args__}, received {query_type}")
        self.query_type = query_type

    def _set_source(self, source: str) -> None:
        if not source:
            raise TestFieldValidationError("<source> is required.")
        self.source = source

    def _set_table(self, table: str) -> None:
        if not table:
            raise TestFieldValidationError("<table> is required.")
        self.table = table


class GeneralTSSTest(TSSTest):
    def __init__(self):
        super().__init__()
        self.min_key: str = "reference_period={current_date}"

