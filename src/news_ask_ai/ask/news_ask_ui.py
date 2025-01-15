from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Input, Button, Static
from textual.containers import Horizontal, Container

from textual.widget import Widget

# from news_ask_ai.ask.news_ask_engine import NewsAskEngine
from news_ask_ai.utils.logger import setup_logger

logger = setup_logger()


class ConversationalContainer(Container, can_focus=True):
    """Conversational container widget."""


class MessageBox(Widget):
    def __init__(self, text: str, role: str) -> None:
        self.text = text
        self.role = role
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Static(self.text, classes=f"message {self.role}")


class NewsAskUI(App):  # type: ignore
    TITLE = "NewsAskAI"
    SUB_TITLE = "Ask questions about the news directly in your terminal"
    CSS_PATH = "../static/css/styles.css"

    def __init__(self) -> None:
        super().__init__()
        logger.info("Initializing RAG engine...")

    def compose(self) -> ComposeResult:
        yield Header()

        # -- Container for topic input and ingest button.
        with Container(id="news_topic_container"):
            yield MessageBox(
                "Welcome to NewsAskAI!\n"
                "Get the latest news insights with just a few clicks.\n"
                "Enter a topic of interest below and press 'Ingest news' to start.\n"
                "Need help? Use the commands at the bottom of your screen.",
                role="info",
            )

            with Horizontal(id="input_box"):
                yield Input(placeholder="Enter news topic...", id="news_topic_input")
                yield Button(label="Ingest news", variant="success", id="news_ingest_button")

        # -- Container for conversation UI, hidden by default.
        with Container(id="conversation_container"):
            with ConversationalContainer(id="conversation_box"):
                yield MessageBox(
                    "You're all set to explore the news!\n"
                    "Type a question about the ingested news and press 'Ask' to get your answer.\n"
                    "Wait for the response...\n"
                    "Need assistance? Commands are listed at the bottom.",
                    role="info",
                )

                with Horizontal(id="input_box"):
                    yield Input(placeholder="Enter your question", id="conversation_input")
                    yield Button(label="Ask", variant="success", id="conversation_button")

        yield Footer()

    def on_mount(self) -> None:
        """Called when app is first mounted."""
        self.query_one("#news_topic_input", Input).focus()

        conversation_container = self.query_one("#conversation_container")
        conversation_container.display = False

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button pressed events."""
        button = event.button

        if button.id == "news_ingest_button":
            news_topic_input = self.query_one("#news_topic_input", Input)
            if not news_topic_input.value.strip():
                return  # No topic entered, do nothing or prompt us

            conversation_container = self.query_one("#news_topic_container")
            conversation_container.display = False  # remove 'none', showing it

            conversation_container = self.query_one("#conversation_container")
            conversation_container.display = True  # remove 'none', showing it

            # TODO: Ingestion routine

        elif button.id == "conversation_button":
            await self.conversation()

    async def conversation(self) -> None:
        message_input = self.query_one("#conversation_input", Input)
        if message_input.value == "":
            return

        conversation_box = self.query_one("#conversation_box")

        message_box = MessageBox(message_input.value, "question")
        conversation_box.mount(message_box)
        conversation_box.scroll_end(animate=True)

        # Clean up the input without triggering events
        with message_input.prevent(Input.Changed):
            message_input.value = ""

        conversation_box.mount(MessageBox("Test", "test"))
