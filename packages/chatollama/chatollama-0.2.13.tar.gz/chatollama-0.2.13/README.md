# chatollama

[![PyPI version](https://badge.fury.io/py/chatollama.svg)](https://badge.fury.io/py/chatollama)

**chatollama** A Python module to streamline conversational AI with the `ollama` library, providing efficient and customizable chat engines. **ChatOllama** offers conversation management and configuration options, ideal for building interactive assistants, customer service bots, and other conversational AI applications.

## Features

- **Engine Class**: Handles conversation flow, manages message attributes, and facilitates model responses with advanced configuration options.
- **Conversation Tree**: Supports branching conversations with a tree structure, enabling complex, multi-threaded interactions.
- **Event Handling**: Customizable events for response streaming, tool usage, and callback functions.
- **Generation Parameters**: Easily adjustable settings for response generation, including modes for creative, coding, and storytelling outputs.

## Installation

To install ChatOllama, use the following pip command:

```bash
pip install chatollama
```

## Usage Examples

### Basic Usage

#### Setting Up a Conversation

```python
from chatollama import Engine

# Initialize engine and start a conversation
engine = Engine(model="llama3.1:8b")

# Add user and assistant messages
engine.user("Hello, how are you?")
engine.assistant("Fantastic! I'm here to assist you. How can I help?")
engine.user("Great, can we get started with making a python project?")

# Start chat
engine.chat()
```

### Branching and Tree Traversal

ChatOllama supports branching, allowing users to handle conversations that diverge based on user inputs.

```python
conversation = engine.conversation

# Add messages and branch conversation
user_node = conversation.add_message(role="user", content="Tell me a story.")
branch_node = conversation.branch_message(user_node, role="assistant", content="Once upon a time...")
conversation.print_tree(conversation.root)
```

### Customizing Generation Parameters

To create focused, creative, or story-driven responses, ChatOllama provides multiple configuration options.

```python
from chatollama import GenerationParameters

# Set engine options for storytelling
engine.options = GenerationParameters().story_telling()

# Set a user message
engine.user("Create a fantasy story for me.")
engine.chat()
```

## Advanced Features

### Response Events

Attach custom callback functions to handle responses and events.

```python
# Define a callback function for responses
def on_response(message):
    print("Response:", message)

# Register the callback function
engine.response_event.on(on_response)

# Send a message and trigger callback
engine.user("What's the weather like today?")
engine.chat()
```

### Vision Support

ChatOllama allows vision-based responses for supported models.

```python
engine = Engine("llama3.2-vision:11b")
engine.stream = True

engine.conversation.user(
    "Tell me about this image, 2 sentences please", images=["path\\to\\earth.png"]) # As you can see, any kwarg added to a message will be sent as part of the message dict that ollama is expecting. Right now there is really only 'images' that can be sent but in the future it might be other things like videos or other files


def print_stream(mode, delta, text):
    if mode == 0:
        print("[AI]:")
    elif mode == 1:
        print(delta, end="")
    elif mode == 2:
        print("")


engine.stream_event.on(print_stream)
engine.chat()

# In the console it will print over time something like this:

# The image shows a photograph of the Earth from space, with North America and Asia visible on either side of the Indian Ocean. 
# The photo is centered in the middle of the planet's curvature, making its spherical shape apparent.
```