"""TcEx Framework Module"""

# third-party
from pydantic import BaseModel, Field


class PytestArgsModel(BaseModel):
    """Model Definition"""

    merge_inputs: bool = Field(
        default=False,
        description='Merge inputs from profile with inputs from PB execution.',
    )
    replace_exit_message: bool = Field(
        default=False,
        description='Replace exit message from profile with exit message from PB execution.',
    )
    replace_outputs: bool = Field(
        default=False, description='Replace outputs from profile with outputs from PB execution.'
    )
    record: bool = Field(
        default=False, description='Record all requests and responses for use in future tests.'
    )

    @property
    def updated(self) -> bool:
        """Return True if profile should be updated."""
        return any(
            [
                self.merge_inputs,
                self.replace_exit_message,
                self.replace_outputs,
                self.record,
            ]
        )
