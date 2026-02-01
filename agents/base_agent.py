import logging


class Agent:
    # --- Bright, Readable Colors ---
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    MAGENTA = '\033[95m'
    RED = '\033[91m'
    RESET = '\033[0m'

    # Configuration
    NAME_WIDTH = 12  # Fixed width for all agent names
    name: str = "BASE"
    color: str = CYAN

    def __init__(self):
        logging.basicConfig(format='%(message)s', level=logging.INFO)

    def log(self, message, is_error=False):
        # If empty message, print blank line
        if not message:
            logging.info("")
            return

        # 1. Format the Name Tag (Centered or Left Aligned)
        formatted_name = f" {self.name:^{self.NAME_WIDTH}} "

        # 2. Build the Tag
        if is_error:
            # Error: Red Tag, Red Message
            tag = f"{self.RED}[{formatted_name}]{self.RESET}"
            content = f"{self.RED}{message}{self.RESET}"
        else:
            # Normal: Agent Color Tag, White Message (Cleaner look)
            tag = f"{self.color}[{formatted_name}]{self.RESET}"
            content = message

        logging.info(f"{tag}  {content}")
