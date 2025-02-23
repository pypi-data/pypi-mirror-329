### **1. `README.md` - Documentation for pyhtmp**
# pyhtmp - Python Hyper Text Markup Programming Template Management Framework

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI Version](https://img.shields.io/pypi/v/pyhtmp)](https://pypi.org/project/pyhtmp/)
[![Documentation](https://img.shields.io/badge/docs-available-brightgreen)](https://github.com/yourusername/pyhtmp#readme)

A modern Python framework for building dynamic HTML interfaces with component-based architecture, virtual DOM implementation, and real-time communication via WebSockets.

---

## Features

- **Component-Based Architecture**: Create reusable UI components.
- **Virtual DOM**: Efficient DOM updates with a diffing algorithm.
- **Real-Time Communication**: WebSocket integration for live updates.
- **Framework Integrations**: Built-in support for Django and Flask.
- **Security**: Automatic HTML sanitization.
- **Type Safety**: Full type hint support.
- **Template Parsing**: HTML string to component conversion.

---

## Installation

Install the package via pip:

```bash
pip install pyhtmp
```

---

## Quick Start

### Basic Usage

```python
from pyhtmp.core import Element, Component, Renderer

# Create elements
div = Element("div", class_="container")
div.add_child(Element("h1", text="Hello World!"))

# Render to HTML
print(Renderer.render_to_string(div))
```

### Real-Time Updates with WebSockets

```python
from pyhtmp.integrations.socket import create_socket_manager
import asyncio

async def main():
    # Connect to WebSocket server
    manager = await create_socket_manager("ws://localhost:8000")

    # Register event handler
    def handle_update(data):
        print(f"Received update: {data}")

    manager.on("update", handle_update)

    # Send a message
    await manager.send("update", {"message": "Hello, WebSocket!"})

    # Start listening for messages
    await manager.receive()

# Run the event loop
asyncio.run(main())
```

---

## Documentation

### Components
Import and use components in your project:
```python
from pyhtmp.components.standard import Button, Form, Layout

button = Button(style="primary", text="Click Me")
form = Form(method="POST", action="/submit")
layout = Layout(columns=2)
```

---

## Available Components

### Standard Components
- **Button**: A customizable button component.
- **Form**: A form component with built-in validation support.
- **Layout**: A flexible layout component for organizing content.

### Custom Components
You can create custom components by extending the `Component` base class.

---

## Creating Custom Components

1. **Extend the `Component` Class**:
```python
from pyhtmp.components.base import Component

class CustomComponent(Component):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def render(self):
        return "<div>Custom Component</div>"
```

2. **Register the Component** (Optional):
```python
from pyhtmp.components import register_component
register_component("custom", CustomComponent)
```

---

## API Reference

### Base Component
- **`Component`**: The base class for all components.
  - Methods:
    - `render()`: Renders the component as an HTML string.
    - `add_child(child)`: Adds a child element or component.

### Standard Components
- **`Button`**:
  - Props: `style`, `text`, `on_click`
- **`Form`**:
  - Props: `method`, `action`, `fields`
- **`Layout`**:
  - Props: `columns`, `gap`, `align`

---

---

### **2. `components/__init__.py` - Component Initialization**
This file initializes the `components` module, exposing the public API and providing utility functions for component management.

```python
# components/__init__.py
"""
pyhtmp Components Module

This module provides reusable UI components built on top of the pyhtmp core framework.
"""

__all__ = ['Component', 'Button', 'Form', 'Layout', 'register_component']

# Base Component
from .base import Component

# Standard Components
from .standard.button import Button
from .standard.form import Form
from .standard.layout import Layout

# Component Registry
_COMPONENT_REGISTRY = {}

def register_component(name: str, component_class: type[Component]):
    """
    Register a custom component for global usage.

    Args:
        name (str): The name of the component (e.g., "custom_button").
        component_class (type[Component]): The component class to register.

    Raises:
        TypeError: If the component_class is not a subclass of Component.
    """
    if not issubclass(component_class, Component):
        raise TypeError(f"{component_class.__name__} must be a subclass of Component")
    _COMPONENT_REGISTRY[name] = component_class

def get_component(name: str) -> type[Component]:
    """
    Retrieve a registered component by name.

    Args:
        name (str): The name of the component.

    Returns:
        type[Component]: The component class.

    Raises:
        KeyError: If the component is not found.
    """
    if name not in _COMPONENT_REGISTRY:
        raise KeyError(f"Component '{name}' is not registered")
    return _COMPONENT_REGISTRY[name]

def list_components() -> list[str]:
    """
    List all registered components.

    Returns:
        list[str]: A list of registered component names.
    """
    return list(_COMPONENT_REGISTRY.keys())

# Auto-register standard components
register_component("button", Button)
register_component("form", Form)
register_component("layout", Layout)
``` 

### **Usage Example**

**1. Using Standard Components:**
```python
from pyhtmp.components import Button, Form, Layout

button = Button(style="primary", text="Submit")
form = Form(method="POST", action="/submit")
layout = Layout(columns=2)

print(button.render())
print(form.render())
print(layout.render())
```

### **Usage Examples**

#### **1. Registering a Custom Component**

```python
from pyhtmp.components import Component, register_component

class CustomComponent(Component):
    def render(self):
        return "<div>Custom Component</div>"

# Register the custom component
register_component("custom", CustomComponent)
```

#### **2. Retrieving a Registered Component**

```python
from pyhtmp.components import get_component

CustomComponent = get_component("custom")
if CustomComponent:
    instance = CustomComponent()
    print(instance.render())
```

#### **3. Listing Registered Components**

```python
from pyhtmp.components import list_components

print(list_components())  # Output: ['button', 'form', 'layout', 'custom']
```

#### **4. Unregistering a Component**

```python
from pyhtmp.components import unregister_component

unregister_component("custom")
print(list_components())  # Output: ['button', 'form', 'layout']
```

---

### Core Structure

```
pyhtmp/
├── core/          # Core framework logic
│
├── dom/           # DOM management
│   
├── components/    # Built-in components
│   
├── utils/         # Utilities
│   
├── integrations/  # Framework integrations
│   
└── exceptions/    # Custom exceptions
```

---

## Framework Integrations

### Django Integration

1. Add `pyhtmp` to your `INSTALLED_APPS`:

   ```python
   # settings.py
   INSTALLED_APPS = [
       ...
       'pyhtmp.integrations.django.PyhtmpConfig',
   ]
   ```

2. Use components in templates:

   ```html
   {% load pyhtmp_tags %}
   {% render_component "button" style="primary" text="Submit" %}
   ```

3. Set up WebSocket views:

   ```python
   from pyhtmp.integrations.socket import create_socket_manager
   from django.http import JsonResponse

   async def websocket_view(request):
       manager = await create_socket_manager("ws://localhost:8000")
       await manager.send("update", {"message": "Hello from Django!"})
       return JsonResponse({"status": "success"})
   ```

### Flask Integration

1. Use components in routes:

   ```python
   from pyhtmp.integrations.flask import flask_render
   from pyhtmp.components import Button

   @app.route('/')
   def home():
       return flask_render(Button(text="Click Me"))
   ```

2. Set up WebSocket views:

   ```python
   from pyhtmp.integrations.socket import create_socket_manager
   from flask import jsonify

   async def websocket_view():
       manager = await create_socket_manager("ws://localhost:8000")
       await manager.send("update", {"message": "Hello from Flask!"})
       return jsonify({"status": "success"})
   ```

---

## Real-Time Communication

### WebSocket Integration

1. **Connect to a WebSocket Server**:

   ```python
   from pyhtmp.integrations.socket import create_socket_manager
   import asyncio

   async def main():
       manager = await create_socket_manager("ws://localhost:8000")
       await manager.send("update", {"message": "Hello, WebSocket!"})
       await manager.receive()

   asyncio.run(main())
   ```

2. **Handle Incoming Messages**:

   ```python
   def handle_update(data):
       print(f"Received update: {data}")

   manager.on("update", handle_update)
   ```

3. **Send Messages**:

   ```python
   await manager.send("update", {"message": "Hello, WebSocket!"})
   ```

---

## Security Features

### Input Sanitization

```python
from pyhtmp.utils.sanitize import sanitize_input

user_input = '<script>alert("XSS")</script>'
safe_html = sanitize_input(user_input)  # Output: &lt;script&gt;...
```

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature.
3. Submit a pull request with a detailed description of your changes.

For more information, see the [Contributing Guidelines](CONTRIBUTING.md).

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

---

This updated `README.md` provides a comprehensive guide for users to get started with `pyhtmp`, including post-packaging implementation details and real-time communication features. It is designed to be user-friendly and informative for both new and experienced developers.