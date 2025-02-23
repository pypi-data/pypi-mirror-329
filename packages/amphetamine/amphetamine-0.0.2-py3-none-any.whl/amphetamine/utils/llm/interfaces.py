"""
garter.utils.llm.interfaces

Classes for interfacing with LLMs as defined in the `models` module.
"""
# Standard library imports: Package-level
import json
import logging
import os
from datetime import datetime as dt
from pathlib import Path
from typing import Dict, List, Tuple, TYPE_CHECKING, Union
if TYPE_CHECKING:
    from _typeshed import SupportsWrite

# Third-party imports: Module-level
from anthropic import Anthropic
from anthropic.types import Message
from dotenv import load_dotenv
from openai import OpenAI

# Local imports: Module-level
from .models import ClaudeModel, ChatGPTModel, CLAUDE_CONVERSATIONS_DIR

# Setting up logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

class Claude(ClaudeModel):
    def __init__(self):
        super().__init__()
        self.client: Anthropic = Anthropic()
        self.conversation: List[Dict] = []
        self.max_tokens: int = 2048
        self.temperature: float = 0.2
        
        # Ensure save_to is a Path object
        self.save_to = Path(CLAUDE_CONVERSATIONS_DIR) / f"{dt.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
        
        # Create directory if it doesn't exist
        self.save_to.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"Conversation will be saved to {self.save_to}")

    def message(self, msg: str) -> Tuple[Dict, Message]:
        """
        Creates a payload using the `msg` string and returns Claude's
        response as a string.
        """
        self.conversation.append({"role": "user", "content": msg})

        # Calling Anthropic's API to transmit the message
        result = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=self.conversation
        )

        response = {"role": "assistant", "content": result.content[0].text}
        self.conversation.append(response)
        
        return response, result

    def save(self, save_as: Union[str, Path] = None) -> int:
        """
        Save the current conversation to a file.
        
        Args:
            save_as: Optional path to save the conversation. If not provided,
                    uses the default path from initialization.
                    
        Returns:
            0 on success, 1 on failure
        """
        try:
            target_path = Path(save_as) if save_as else self.save_to
            if not target_path.is_absolute():
                target_path = Path(CLAUDE_CONVERSATIONS_DIR) / target_path
                
            target_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(target_path, "w") as f:
                json.dump(self.conversation, f, indent=4)
            logger.info(f"Successfully saved conversation to {target_path}")
            return 0
            
        except Exception as e:
            logger.error(f"Failed to save conversation: {str(e)}")
            return 1

class ChatGPT(ChatGPTModel):
    def __init__(self):
        self.client = OpenAI()
        self.conversation: List[Dict] = []
        self.save_to: Union[str, Path] = (
            Path("~/.llm/chatgpt/conversations").expanduser()
        )
        self.max_tokens: int = 2048
        self.temperature: float = 0.2

        if not self.save_to.exists():
            logger.warning(f"{self.save_to} does not exist; creating it.")
            try:
                self.save_to.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                print(e)
        else:
            logger.info(f"{self.save_to} already exists; skipping creation.")


    def message(self, msg: str):
        self.conversation.append({"role": "user", "content": msg})

        result = self.client.chat.completions.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=self.conversation
        )

        response = {"role": "assistant", "content": result.choices[0].message.content}

        print(response)

        self.conversation.append(response)

        return response, result

    # noinspection DuplicatedCode
    def save(
        self,
        save_as: Union[str, Path] = Path(f"~/.llm/chatgpt/conversations/{dt.now().strftime('%Y-%m-%d_%H-%M-%S')}.json").expanduser()) -> int:
        with open(save_as, "w") as f:
            f: SupportsWrite[str]
            logger.info(f"Saving conversation to {self.save_to}")

            try:
                json.dump(self.conversation, f, indent=4)
                logger.info("Success.")
                return 0
            except Exception as e:
                print(e)
                return 1
