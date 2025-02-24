from dataclasses import dataclass
import inspect
from typing import Callable, List, Any
import ollama
from typing import List, Optional
import asyncio


__all__ = ["Engine", "Conversation",
           "MessageNode", "GenerationParameters", "Event", "ResponseEvent", "StreamEvent", "ToolEvent"]


class MessageNode:
    def __init__(self, role: str, content: str, parent: Optional['MessageNode'] = None, **kwargs):
        self.role = role
        self.content = content
        self.data = kwargs
        self.parent = parent
        self.children: List['MessageNode'] = []

    def __str__(self):
        return "[{}]: {}".format(self.role, self.content)


class Conversation:
    def __init__(self):
        self.root = MessageNode(role='root', content='')
        self.current_node = self.root

    def add_message(self, role: str, content: str, **kwargs) -> MessageNode:
        """
        Adds a message to the current active path.

        :param role: The role of the message (e.g., "user", "assistant").
        :param content: The content of the message.
        :param kwargs: Additional data to associate with the message node.
        :return: The newly created MessageNode.
        """
        if not isinstance(role, str):
            raise ValueError("'role' must be a string, got {}".format(
                type(role).__name__))
        if not isinstance(content, str):
            raise ValueError("'content' must be a string, got {}".format(
                type(content).__name__))

        new_node = MessageNode(role=role, content=content,
                               parent=self.current_node, **kwargs)
        self.current_node.children.append(new_node)
        self.current_node = new_node
        return new_node

    def branch_message(self, node: MessageNode, role: str, content: str) -> MessageNode:
        """
        Creates a new branch at the same level as the specified node.

        :param node: The node where the new branch will be created.
        :param role: The role of the new message (e.g., "user", "assistant").
        :param content: The content of the new message.
        :return: The newly created MessageNode.
        """
        if node.parent is None:
            raise ValueError("Cannot branch at the root node.")

        if not isinstance(role, str):
            raise ValueError("'role' must be a string, got {}".format(
                type(role).__name__))
        if not isinstance(content, str):
            raise ValueError("'content' must be a string, got {}".format(
                type(content).__name__))

        new_node = MessageNode(role=role, content=content, parent=node.parent)
        node.parent.children.append(new_node)
        return new_node

    def set_active_path(self, node: MessageNode):
        """
        Sets the active node to the specified node.

        :param node: The node to set as the current active node.
        :return: None
        """
        if not self._is_node_in_tree(node):
            raise ValueError(
                "The specified node is not part of the conversation tree.")
        self.current_node = node

    def get_active_path(self) -> List[MessageNode]:
        """
        Returns the list of nodes from the root to the current active node.

        :return: A list of MessageNode objects representing the active path.
        """
        path: List[MessageNode] = []
        node = self.current_node
        while node:
            path.append(node)
            node = node.parent
        if len(path) > 0:
            if path[-1].role == "root":
                path.pop()
        return list(reversed(path))

    def traverse_tree(self, node: Optional[MessageNode] = None):
        """
        Traverses the entire conversation tree.

        :param node: The node to start traversal from. If None, traversal starts at the root.
        :yield: Each MessageNode in the tree.
        """
        if node is None:
            node = self.root
        yield node
        for child in node.children:
            yield from self.traverse_tree(child)

    def _is_node_in_tree(self, node: MessageNode) -> bool:
        """
        Checks if a node is part of the conversation tree.

        :param node: The node to check.
        :return: True if the node is in the tree, False otherwise.
        """
        current = node
        while current:
            if current is self.root:
                return True
            current = current.parent
        return False

    def print_tree(self, node: Optional[MessageNode] = None, indent: int = 0):
        """
        Prints the conversation tree.
        - If `node` is provided, prints the tree starting from that node.
        - If no `node` is provided, prints the tree along the active path.

        :param node: The node to start printing from. Defaults to None.
        :param indent: The level of indentation for printing. Defaults to 0.
        :return: None
        """
        if node is None:
            # Use the active path if no node is specified
            path = self.get_active_path()
            for idx, node_in_path in enumerate(path):
                print('    ' * idx + str(node_in_path))
        else:
            # Print the tree starting from the specified node
            print('    ' * indent + str(node))
            for child in node.children:
                self.print_tree(child, indent + 1)

    def system(self, content: str, **kwargs):
        """
        Adds a system message to the conversation.

        :param content: The content of the system message.
        :param kwargs: Additional data to associate with the message node.
        :return: The newly created MessageNode.
        """
        return self.add_message(role="system", content=content, **kwargs)

    def assistant(self, content: str, **kwargs):
        """
        Adds an assistant message to the conversation.

        :param content: The content of the assistant message.
        :param kwargs: Additional data to associate with the message node.
        :return: The newly created MessageNode.
        """
        return self.add_message(role="assistant", content=content, **kwargs)

    def user(self, content: str, **kwargs):
        """
        Adds a user message to the conversation.

        :param content: The content of the user message.
        :param kwargs: Additional data to associate with the message node.
        :return: The newly created MessageNode.
        """
        return self.add_message(role="user", content=content, **kwargs)

    def copy(self) -> 'Conversation':
        """
        Creates a deep copy of the conversation tree, including the current active node.

        :return: A new Conversation instance that is a copy of the current conversation.
        """
        node_mapping = {}

        def copy_node(node: MessageNode, parent_copy: Optional[MessageNode] = None) -> MessageNode:
            # Create a copy of the current node
            new_node = MessageNode(
                role=node.role, content=node.content, parent=parent_copy, **node.data)
            # Map the original node to its copy
            node_mapping[node] = new_node
            # Recursively copy children
            new_node.children = [copy_node(child, new_node)
                                 for child in node.children]
            return new_node

        # Create a new Conversation and copy the root
        new_conversation = Conversation()
        new_conversation.root = copy_node(self.root)
        # Update the current_node to point to the corresponding node in the copied tree
        new_conversation.current_node = node_mapping[self.current_node]

        return new_conversation


class Event:
    def __init__(self):
        self.callbacks: List[Callable[..., Any]] = []

    def on(self, callback: Callable[..., Any]) -> None:
        self.callbacks.append(callback)

    def trigger(self, *args: Any, **kwargs: Any) -> List[Any]:
        results = []
        for callback in self.callbacks:
            # Get the signature of the callback function
            signature = inspect.signature(callback)
            parameters = signature.parameters

            # Filter `args` and `kwargs` to match the number of parameters in the callback
            required_args = len([p for p in parameters.values(
            ) if p.default == p.empty and p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)])
            limited_args = args[:required_args]

            # Filter kwargs based on the callback's parameters
            limited_kwargs = {k: v for k,
                              v in kwargs.items() if k in parameters}

            # Bind the filtered args and kwargs to the function signature
            bound_args = signature.bind_partial(
                *limited_args, **limited_kwargs)
            bound_args.apply_defaults()  # Fill missing parameters with defaults or None

            # Call the callback with the matched arguments
            result = callback(*bound_args.args, **bound_args.kwargs)
            results.append(result)
        return results

    async def trigger_async(self, *args: Any, **kwargs: Any) -> List[Any]:
        results = []
        await asyncio.sleep(0)
        for callback in self.callbacks:
            # Get the signature of the callback function
            signature = inspect.signature(callback)
            parameters = signature.parameters

            # Filter `args` and `kwargs` to match the number of parameters in the callback
            required_args = len([p for p in parameters.values(
            ) if p.default == p.empty and p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)])
            limited_args = args[:required_args]

            # Filter kwargs based on the callback's parameters
            limited_kwargs = {k: v for k,
                              v in kwargs.items() if k in parameters}

            # Bind the filtered args and kwargs to the function signature
            bound_args = signature.bind_partial(
                *limited_args, **limited_kwargs)
            bound_args.apply_defaults()  # Fill missing parameters with defaults or None

            # Call the callback with the matched arguments
            result = await callback(*bound_args.args, **bound_args.kwargs)
            results.append(result)
        return results

    def call(self, *args: Any, **kwargs: Any) -> List[Any]:
        results = []
        for callback in self.callbacks:
            # Call each callback with all arguments; each callback will handle what it needs
            result = callback(*args, **kwargs)
            results.append(result)
        return results

    async def call_async(self, *args: Any, **kwargs: Any) -> List[Any]:
        results = []
        for callback in self.callbacks:
            # Call each callback with all arguments; each callback will handle what it needs
            result = await callback(*args, **kwargs)
            results.append(result)
        return results


@dataclass
class GenerationParameters:
    # Controls randomness; range 0.0-1.0. Lower is more predictable, higher is more creative.
    temperature: float = 0.7

    # Limits token choices to the top k options; range 0-100. Lower is more focused, higher is more diverse.
    top_k: int = 50

    # Probability threshold for token choices; range 0.0-1.0. Lower focuses on most probable words.
    top_p: float = 1.0

    # Reduces word repetition; range 0.0-2.0. Higher values make responses less repetitive.
    frequency_penalty: float = 0

    # Encourages new words/topics; range 0.0-2.0. Higher values make responses more varied.
    presence_penalty: float = 0

    def to_dict(self):
        return {
            'temperature': self.temperature,
            'top_k': self.top_k,
            'top_p': self.top_p,
            'frequency_penalty': self.frequency_penalty,
            'presence_penalty': self.presence_penalty
        }

    def creative(self):
        """Configures settings for highly creative, varied responses."""
        self.temperature = 0.9
        self.top_k = 80
        self.top_p = 0.9
        self.frequency_penalty = 0.2
        self.presence_penalty = 0.5
        return self

    def coding(self):
        """Configures settings for focused, precise responses suitable for technical or coding answers."""
        self.temperature = 0.2
        self.top_k = 20
        self.top_p = 0.8
        self.frequency_penalty = 0
        self.presence_penalty = 0
        return self

    def informative(self):
        """Configures settings for clear, informative responses with minimal creativity."""
        self.temperature = 0.3
        self.top_k = 40
        self.top_p = 0.9
        self.frequency_penalty = 0
        self.presence_penalty = 0
        return self

    def conversational(self):
        """Configures settings for natural, engaging conversation flow."""
        self.temperature = 0.7
        self.top_k = 60
        self.top_p = 0.95
        self.frequency_penalty = 0.2
        self.presence_penalty = 0.3
        return self

    def story_telling(self):
        """Configures settings for imaginative storytelling and longer responses."""
        self.temperature = 1.0
        self.top_k = 100
        self.top_p = 0.85
        self.frequency_penalty = 0.5
        self.presence_penalty = 0.6
        return self

    def brute(self):
        """Configures settings for a brutish style of responses"""
        self.temperature = 0
        self.top_k = 1
        self.top_p = 0
        self.frequency_penalty = 0
        self.presence_penalty = 0
        return self


class ResponseEvent:
    def __init__(self):
        self.message = ""
        self.response = None


class StreamEvent:
    def __init__(self):
        self.mode = 0
        self.delta = ""
        self.text = ""
        self.response = None


class ToolEvent:
    def __init__(self):
        self.tool_calls = []
        self.response = None


class Engine:
    def __init__(self, model: str = "llama3.1:8b"):
        self.model = model
        self.conversation = Conversation()
        self.tools = []
        self.use_tools = False
        self.stream = False
        self.format = ''
        self.options = GenerationParameters()

        self.keep_alive = -1

        self.response_event = Event()
        self.stream_event = Event()
        self.tool_event = Event()
        self.stream_stopped_event = Event()

        self.print_if_loading = True

        self.response: str = ""
        self.tool_calls: list = []

    def system(self, content: str):
        return self.conversation.system(content=content)

    def assistant(self, content: str):
        return self.conversation.assistant(content=content)

    def user(self, content: str):
        return self.conversation.user(content=content)

    def get_messages(self):
        return self.conversation.get_active_path()

    def get_ollama_messages(self):
        messages = self.get_messages()
        ollama_messages = []
        for message in messages:
            ollama_message = {}
            ollama_message["role"] = message.role
            ollama_message["content"] = message.content
            for key in message.data:
                ollama_message[key] = message.data[key]
            ollama_messages.append(ollama_message)

        return ollama_messages

    def chat(self):
        """Progresses the conversation allowing the model to respond and store the response into the conversation"""

        models = ollama.ps()
        models = models.get("models", [])

        if self.print_if_loading:
            found = False
            for model in models:
                name = model.get("name", None)
                model_name = model.get("model", None)
                
                # Split model names to handle versioned names
                current_model = self.model.split(':')[0] if ':' in self.model else self.model
                model_base_name = name.split(':')[0] if name and ':' in name else name
                model_name_base = model_name.split(':')[0] if model_name and ':' in model_name else model_name
                
                if current_model == model_base_name or current_model == model_name_base:
                    found = True
                    break

            if not found:
                print("Model: [{}] is loading...".format(self.model))

        messages = self.get_ollama_messages()

        self.stream_stop = False

        response = ollama.chat(
            model=self.model,
            messages=messages,
            tools=self.tools if self.use_tools else None,
            stream=False if self.use_tools else self.stream,
            format=self.format,
            options=self.options.to_dict(),
            keep_alive=self.keep_alive
        )

        did_stream_stop = self.on_response(response)
        if did_stream_stop:
            self.stream_stopped_event.trigger()

    def on_response(self, response):
        if self.use_tools:
            self.tool_calls = response.get(
                "message", {}).get("tool_calls", {})
            tool_event = ToolEvent()
            tool_event.tool_calls = self.tool_calls
            tool_event.response = response
            self.tool_event.trigger(tool_event)
        elif self.stream:
            if self.stream_stop:
                return True
            stream_event = StreamEvent()
            stream_event.mode = 0
            stream_event.delta = ""
            stream_event.text = ""
            stream_event.response = None
            self.stream_event.trigger(stream_event)
            self.response = ""
            for chunk in response:
                if self.stream_stop:
                    response.close()
                    return True
                delta = chunk.get("message", {}).get("content", {})
                self.response += delta
                stream_event.mode = 1
                stream_event.delta = delta
                stream_event.text = self.response
                stream_event.response = chunk
                self.stream_event.trigger(stream_event)
            if self.stream_stop:
                return True
            stream_event = StreamEvent()
            stream_event.mode = 2
            stream_event.delta = ""
            stream_event.text = self.response
            stream_event.response = None
            self.stream_event.trigger(stream_event)
        else:
            self.response = response.get(
                "message", {}).get("content", {})
            response_event = ResponseEvent()
            response_event.message = self.response
            response_event.response = response
            self.response_event.trigger(response_event)

        return False

    async def chat_async(self):
        """Progresses the conversation allowing the model to respond and store the response into the conversation"""

        models = ollama.ps()
        models = models.get("models", [])

        if self.print_if_loading:
            found = False
            for model in models:
                name = model.get("name", None)
                model_name = model.get("model", None)
                if self.model == name or self.model == model_name:
                    found = True
                    break

            if not found:
                print("Model: [{}] is loading...".format(self.model))

        messages = self.get_ollama_messages()

        self.stream_stop = False

        response = ollama.chat(
            model=self.model,
            messages=messages,
            tools=self.tools if self.use_tools else None,
            stream=False if self.use_tools else self.stream,
            format=self.format,
            options=self.options.to_dict(),
            keep_alive=self.keep_alive
        )

        did_stream_stop = await self.on_response_async(response)
        if did_stream_stop:
            self.stream_stopped_event.trigger()

    async def on_response_async(self, response):
        if self.use_tools:
            self.tool_calls = response.get(
                "message", {}).get("tool_calls", {})
            tool_event = ToolEvent()
            tool_event.tool_calls = self.tool_calls
            tool_event.response = response
            await self.tool_event.trigger_async(tool_event)
        elif self.stream:
            if self.stream_stop:
                return True
            stream_event = StreamEvent()
            stream_event.mode = 0
            stream_event.delta = ""
            stream_event.text = ""
            stream_event.response = None
            await self.stream_event.trigger_async(stream_event)
            self.response = ""
            for chunk in response:
                if self.stream_stop:
                    response.close()
                    return True
                delta = chunk.get("message", {}).get("content", {})
                self.response += delta
                stream_event.mode = 1
                stream_event.delta = delta
                stream_event.text = self.response
                stream_event.response = chunk
                await self.stream_event.trigger_async(stream_event)
            if self.stream_stop:
                return True
            stream_event = StreamEvent()
            stream_event.mode = 2
            stream_event.delta = ""
            stream_event.text = self.response
            stream_event.response = None
            await self.stream_event.trigger_async(stream_event)
        else:
            self.response = response.get(
                "message", {}).get("content", {})
            response_event = ResponseEvent()
            response_event.message = self.response
            response_event.response = response
            await self.response_event.trigger_async(response_event)

        await asyncio.sleep(0)
        return False

    def prompt(self, message: str, **kwargs):
        """Sends a single message to the model, its a temporary message that is not stored into the conversation"""
        pass

    def unload(self):
        """
        This function tries unloading the model by setting the keep_alive value to 0
        However it requires one more call to the model using an empty conversation with the singular instruction:
        'Respond with just the word "stop"'
        This has a high chance of working but a low chance the model says more than just stop. So the function might not finish instantly
        It also uses its own settings for the model so no tools, no format, no stream...etc
        """
        options = {
            'temperature': 0.1,
            'top_p': 1.0,
            'frequency_penalty': 0,
            'presence_penalty': 0
        }
        ollama.chat(
            self.model, [{"role": "system", "content": "Respond with just the word 'stop'"}, {"role": "user", "content": "Respond with just the word 'stop'"}], options=options, keep_alive=0)

    def add_default_stream_print_callback(self):
        def callback(stream_event: StreamEvent):
            if stream_event.mode == 0:
                print("[{}]:".format(self.model))
            elif stream_event.mode == 1:
                print(stream_event.delta, end="", flush=True)
            elif stream_event.mode == 2:
                print()
        self.stream_event.on(callback)
        return callback

    def add_default_response_print_callback(self):
        def callback(response_event: ResponseEvent):
            print(response_event.message)
        self.response_event.on(callback)
        return callback

    def add_default_tool_print_callback(self):
        def callback(tool_event: ToolEvent):
            print(tool_event.tool_calls)
        self.tool_event.on(callback)
        return callback
