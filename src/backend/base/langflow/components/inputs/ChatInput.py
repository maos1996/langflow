from langflow.base.data.utils import IMG_FILE_TYPES, TEXT_FILE_TYPES
from langflow.base.io.chat import ChatComponent
from langflow.io import DropdownInput, FileInput, MultilineInput, Output, TextInput
from langflow.schema.message import Message


class ChatInput(ChatComponent):
    display_name = "Chat Input"
    description = "Get chat inputs from the Playground."
    icon = "ChatInput"

    inputs = [
        MultilineInput(
            name="input_value",
            display_name="Text",
            value="",
            info="Message to be passed as input.",
        ),
        DropdownInput(
            name="sender",
            display_name="Sender Type",
            options=["Machine", "User"],
            value="User",
            info="Type of sender.",
            advanced=True,
        ),
        TextInput(
            name="sender_name",
            display_name="Sender Name",
            info="Name of the sender.",
            value="User",
            advanced=True,
        ),
        TextInput(name="session_id", display_name="Session ID", info="Session ID for the message.", advanced=True),
        FileInput(
            name="files",
            display_name="Files",
            file_types=TEXT_FILE_TYPES + IMG_FILE_TYPES,
            info="Files to be sent with the message.",
            advanced=True,
            is_list=True,
        ),
    ]
    outputs = [
        Output(display_name="Message", name="message", method="message_response"),
    ]

    def message_response(self) -> Message:
        message = Message(
            text=self.input_value,
            sender=self.sender,
            sender_name=self.sender_name,
            session_id=self.session_id,
            files=self.files,
        )
        if self.session_id and isinstance(message, Message) and isinstance(message.text, str):
            self.store_message(message)
            self.message.value = message

        self.status = message
        return message
