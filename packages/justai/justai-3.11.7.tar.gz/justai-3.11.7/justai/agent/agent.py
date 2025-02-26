""" Handles the GPT API and the conversation state. """
import json
import os
import re
import time
from pathlib import Path
from PIL.Image import Image

from justai.tools.cache import cached_llm_response
from justai.tools.display import print_message, color_print, SYSTEM_COLOR
from justai.agent.message import Message
from justai.models.modelfactory import ModelFactory


class Agent:
    def __init__(self, model_name: str, **kwargs):
        
        # Model parameters
        self.model = ModelFactory.create(model_name, **kwargs)

        # Parameters to save the current conversation
        self.save_dir = Path(__file__).resolve().parent / 'saves'
        self.message_memory = 20  # Number of messages to remember. Limits token usage.
        self.messages = []  # List of Message objects

        self.input_token_count = 0
        self.output_token_count = 0
        self.last_response_time = 0
        
        self.logger = None
        
    def __setattr__(self, name, value):
        if name not in self.__dict__ and hasattr(self, 'model') and name in self.model.model_params:
            # Not an existing property model but a model_params property. Set it in model_params
            self.model.model_params[name] = value
        else:
            # Update the property as intended
            super().__setattr__(name, value)

    @classmethod
    def from_json(cls, model_name, model_data, **kwargs):
        """ Creates an agent from a json string. Usefull in stateless environments like a web page """
        agent = cls(model_name, **kwargs)
        dictionary = json.loads(model_data)
        for key, value in dictionary.items():
            match key:
                case 'save_dir':
                    agent.save_dir = Path(value)
                case 'messages':
                    agent.messages = [Message.from_dict(m) for m in value]
                case _:
                    agent.__setattr__(key, value)
        return agent

    def set_api_key(self, key: str):
        """ Used when using Aigent from a browser where the user has to specify a key """
        self.model.set('api_key', key)

    @property
    def system(self):  # This function can be overwritten by child classes to make the system message dynamic
        return self.model.system_message

    @system.setter
    def system(self, value):
        self.model.system_message = value

    @property
    def cached_prompt(self): 
        if hasattr(self.model, 'cached_prompt'):
            return self.model.cached_prompt
        raise AttributeError("Model does not support cached_prompt")

    @cached_prompt.setter
    def cached_prompt(self, value):
        if hasattr(self.model, 'cached_prompt'):
            self.model.cached_prompt = value
        else:
            raise AttributeError("Model does not support cached_prompt")

    @property
    def cache_creation_input_tokens(self):
        if hasattr(self.model, 'cache_creation_input_tokens'):
            return self.model.cache_creation_input_tokens
        raise AttributeError("Model does not support cache_creation_input_tokens")
    
    @property
    def cache_read_input_tokens(self):
        if hasattr(self.model, 'cache_read_input_tokens'):
            return self.model.cache_read_input_tokens
        raise AttributeError("Model does not support cache_read_input_tokens")
        
    def reset(self):
        self.messages = []

    def append_messages(self, prompt: str,
                        images: [list[str] | list[bytes] | list[Image] | str | bytes | Image | None] = None):
        if images:
            if not isinstance(images, list):
                images = [images]
        else:
            images = []
        self.messages.append(Message('user', prompt, images))
        return self.messages

    def get_messages(self) -> list[Message]:
        return self.messages[-self.message_memory:]

    def last_token_count(self):
        return self.input_token_count, self.output_token_count, self.input_token_count + self.output_token_count

    def chat(self, prompt, *, images: [list[str] | list[bytes] | list[Image] | str | bytes | Image | None] = None,
             return_json=False, response_format=None, cached=True):
        start_time = time.time()
        if images and not isinstance(images, list):
            images = [images]
        self.append_messages(prompt, images)

        model_response = cached_llm_response(self.model, self.get_messages(), return_json=return_json, 
                                             response_format=response_format, use_cache=cached)
        result, self.input_token_count, self.output_token_count = model_response
        self.messages.append(Message('assistant', str(result)))
        self.last_response_time = time.time() - start_time
        return result
    
    async def chat_async(self, prompt, *,
                         images: [list[str] | list[bytes] | list[Image] | str | bytes | Image | None] = None):
        if images and not isinstance(images, list):
            images = [images]
        self.append_messages(prompt, images)
        for word, _ in self.model.chat_async(messages=self.get_messages()):
            if word:
                yield word

    async def chat_async_reasoning(self, prompt, *,
                         images: [list[str] | list[bytes] | list[Image] | str | bytes | Image | None] = None):
        """ Same as chat_async but returns the reasoning content as well
        """
        if images and not isinstance(images, list):
            images = [images]
        self.append_messages(prompt, images)
        for word, reasoning_content in self.model.chat_async(messages=self.get_messages()):
            if word or reasoning_content:
                yield word, reasoning_content

    def after_response(self):
        # content is in messages[-1]['completion']['choices'][0]['message']['content']
        return  # Can be overridden

    def save(self, name=None):
        if not name:
            name = re.sub(r'\W+', '', self.messages[0].text).replace(' ', '_')[:20]
        self.save_dir.mkdir(exist_ok=True)
        with open((self.save_dir / name).with_suffix('.txt'), "w") as f:
            f.write(f"system: {self.system}\n")
            for message in self.messages:
                f.write(f"{message.role}: {message.text}\n")

    def load(self, name: str):
        def save_message(msg):
            if msg.role == 'system':
                self.system = msg.content
            else:
                self.messages += [msg]

        self.messages = []
        if not name.endswith('.txt'):
            name += '.txt'
        filename = self.save_dir / name
        if not os.path.isfile(filename):
            color_print(f"New conversation:  {filename}", color=SYSTEM_COLOR)
            return
        with open(filename, "r") as f:
            message = Message()
            assert not message
            for line in f.readlines():
                line = line[:-1]
                try:
                    role, text = line.split(': ', 1)
                except ValueError:
                    message.content += '\n' + line
                    continue
                if role in ['system', 'user', 'assistant', 'function']:
                    if message:
                        save_message(message)
                    message = Message(role=role, content=text)
                else:
                    message.content += '\n' + line
            if message:
                save_message(message)
        print_message(Message('system', self.system), 'system')
        for message in self.messages:
            print_message(message.text, message.role)

    def file_input(self, filename):
        with open(filename, "r") as f:
            prompt = f.read()
        self.chat(prompt)

    def dumps(self) -> str:
        data = {}
        for key, value in self.__dict__.items():
            if value is not None:
                try:
                    json.dumps(value)
                    data[key] = value
                except (TypeError, ValueError):
                    match key:
                        case 'save_dir':
                            data[key] = str(value)
                        case 'messages':
                            data[key] = [message.to_dict() for message in value]
        return json.dumps(data, indent=2)

    def token_count(self, text: str):
        return self.model.token_count(text)
