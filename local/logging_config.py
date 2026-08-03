import logging
from typing import ClassVar

from rich.console import Console
from rich.logging import RichHandler
from rich.text import Text
from rich.theme import Theme
from rich.terminal_theme import TerminalTheme

from smard_pipeline.config import LOGS_DIR

CUSTOM_THEME = TerminalTheme(
    (12, 12, 12),
    (217, 217, 217),
    [
        (26, 26, 26),
        (244, 0, 95),
        (152, 224, 36),
        (255, 255, 0),
        (0, 128, 255),
        (244, 0, 95),
        (88, 209, 235),
        (196, 197, 181),
        (98, 94, 76),
    ],
    [
        (244, 0, 95),
        (152, 224, 36),
        (224, 213, 97),
        (0, 128, 255),
        (244, 0, 95),
        (88, 209, 235),
        (246, 246, 239),
    ],
)

class StatusAwareRichHandler(RichHandler):
    STATUS_ICONS: ClassVar[dict] = {
        "success": "✔",
        "complete": "★",
        "fail": "✗"
    }

    def get_level_text(self, record: logging.LogRecord) -> Text:
        status: str = getattr(record, "status", None)
        if status in self.STATUS_ICONS:
            label: str = status.upper().ljust(8)
            return Text.styled(f"{label}", f"status.{status}")
        return super().get_level_text(record)

    def render_message(self, record: logging.LogRecord, message: str):
        status: str = getattr(record, "status", None)
        message_renderable = super().render_message(record, message)
        if status in self.STATUS_ICONS:
            icon: str = self.STATUS_ICONS[status]
            message_renderable.append(f" {icon}", style=f"status.{status}")
        return message_renderable

custome_theme: Theme = Theme(
    {
        "status.success": "green",
        "status.complete": "bold green",
        "status.fail": "red"
    }
)

# Set handler.
console: Console = Console(record=True, theme=custome_theme)
console_handler: StatusAwareRichHandler = StatusAwareRichHandler(
    console=console,
    log_time_format="[%d.%m.%y %X]"
)
file_handler: logging.FileHandler = logging.FileHandler(
    filename=LOGS_DIR / 'pipeline.log',
    encoding='utf8'
)
formatter: logging.Formatter = logging.Formatter(
    fmt="%(asctime)s %(name)s %(levelname)s : %(message)s",
    datefmt="[%d.%m.%y %X]"
)
file_handler.formatter = formatter

def setup_logging(level: int = logging.DEBUG):
    logging.basicConfig(
        level=level,
        format="%(message)s",
        handlers=[console_handler, file_handler]
    )

def save_log_to_html(file_name: str) -> None:
    console.save_html(LOGS_DIR / f"{file_name}.html", theme=CUSTOM_THEME)