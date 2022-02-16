from __future__ import annotations

import data_models.interaction
from data_models.interaction import ButtonStyle
from data_models.interaction import ComponentType


class Component:
    def __init__(self, type: data_models.interaction.ComponentType):
        self.type = type
        if type == ComponentType.ACTION_ROW:
            self.components = []
        elif type == ComponentType.BUTTON:
            self._style = 1
            self._custom_id = 'placeholder'
        elif type == ComponentType.SELECT_MENU:
            self._custom_id = 'placeholder'
        elif type == ComponentType.TEXT_INPUT:
            self.title = 'modal'
            self._custom_id = 'placeholder'
            self._label = 'placeholder'

    def to_json(self):
        pass


class ActionRow(Component):
    def __init__(self):
        super().__init__(ComponentType.ACTION_ROW)

    def add_component(self, component: Component):
        self.components.append(component)
        return self

    def to_json(self):
        components = [i.to_json() for i in self.components]
        return {'type': self.type, 'components': components}


class Button(Component):
    def __init__(self, style, custom_id):
        super().__init__(ComponentType.BUTTON)
        self._disabled = False
        self._url = None
        self._custom_id = custom_id
        self._emoji = None
        self._label = ''
        self._style = style

    @classmethod
    def from_json(cls, data):
        button = cls(data['style'])
        if data.get('label'):
            button._label = data.get('label')
        if data.get('emoji'):
            button._emoji = data.get('emoji')
        if data.get('custom_id'):
            button._custom_id = data.get('custom_id')
        if data.get('url'):
            button._url = data.get('url')
        if data.get('disabled') is not None:
            button._disabled = data.get('disabled')
        return button

    def style(self, style: ButtonStyle):
        self._style = style
        return self

    def label(self, label: str):
        self._label = label
        return self

    def emoji(self, emoji: dict):
        self._emoji = emoji
        return self

    def custom_id(self, custom_id: str):
        self._custom_id = custom_id
        return self

    def url(self, url: str):
        self._url = url
        return self

    def disabled(self, disabled: bool):
        self._disabled = disabled
        return self

    def to_json(self):
        json = {'type': self.type, 'style': self._style, 'label': self._label,
                'disabled': self._disabled
                }
        if self._emoji:
            json['emoji'] = self._emoji
        if self._custom_id:
            json['custom_id'] = self._custom_id
        if self._url:
            json['url'] = self._url
        return json


class SelectMenu(Component):
    def __init__(self, custom_id):
        super().__init__(ComponentType.SELECT_MENU)
        self._custom_id = custom_id
        self._disabled = False
        self._max_values = None
        self._min_values = None
        self._placeholder_text = 'placeholder'
        self.options = []

    @classmethod
    def from_json(cls, data):
        menu = cls(data['custom_id'])
        for i in data.get('options'):
            option = {'label': i['label'], 'value': i['value']}
            if 'description' in data:
                option['description'] = data['description']
            if 'emoji' in data:
                option['emoji'] = data['emoji']
            if 'default' in data:
                option['default'] = data['default']
        if 'placeholder' in data:
            menu.placeholder_text(data['placeholder'])
        if 'min_values' in data:
            menu.min_values(data['min_values'])
        if 'max_values' in data:
            menu.max_values(data['max_values'])
        if 'disabled' in data:
            menu.disabled(data['disabled'])
        return menu

    def custom_id(self, custom_id):
        self._custom_id = custom_id
        return self

    def add_option(self, label: str, value: str, description='', emoji=None, default=False):
        self.options.append(
            {'label': label, 'value': value, 'description': description, 'emoji': emoji, 'default': default})
        return self

    def placeholder_text(self, placeholder_text):
        self._placeholder_text = placeholder_text
        return self

    def min_values(self, min_values: int):
        """The minimum amount of values that must be chosen"""
        self._min_values = min_values
        return self

    def max_values(self, max_values):
        """The maximum amount of values that can be chosen"""
        self._max_values = max_values
        return self

    def disabled(self, disabled):
        self._disabled = disabled
        return self

    def to_json(self):
        json = {'type': self.type, 'custom_id': self._custom_id, 'options': self.options,
                'placeholder': self._placeholder_text,
                'disabled': self._disabled}
        if self._min_values:
            json['min_values'] = self._min_values
        if self._max_values:
            json['max_values'] = self._max_values
        return json


class TextInput(Component):
    def __init__(self, custom_id, style=None, label=None):
        super().__init__(ComponentType.TEXT_INPUT)
        self._label = label
        self._style = style
        self._custom_id = custom_id
        self._placeholder = None
        self._value = None
        self._required = False
        self._max_length = 4000
        self._min_length = 1

    @classmethod
    def from_json(cls, data):
        text_input = cls(data['custom_id'])
        if 'label' in data:
            text_input.label(data['label'])
        if 'style' in data:
            text_input.style(data['style'])
        if 'min_length' in data:
            text_input.min_length(data['min_length'])
        if 'max_length' in data:
            text_input.max_length(data['max_length'])
        if 'required' in data:
            text_input.required(data['required'])
        if 'value' in data:
            text_input.value(data['value'])
        if 'placeholder' in data:
            text_input.placeholder(data['placeholder'])
        return text_input

    def custom_id(self, custom_id) -> TextInput:
        self._custom_id = custom_id
        return self

    def style(self, style: data_models.interaction.TextInputStyle) -> TextInput:
        self._style = style
        return self

    def label(self, label: str) -> TextInput:
        self._label = label
        return self

    def min_length(self, min_length: int) -> TextInput:
        self._min_length = min_length
        return self

    def max_length(self, max_length: int) -> TextInput:
        self._max_length = max_length
        return self

    def required(self, required: bool) -> TextInput:
        self._required = required
        return self

    def value(self, value: str) -> TextInput:
        self._value = value
        return self

    def placeholder(self, placeholder: str) -> TextInput:
        self._placeholder = placeholder
        return self

    def to_json(self):
        json = {'type': self.type, 'custom_id': self._custom_id, 'style': self._style, 'label': self._label,
                'min_length': self._min_length, 'max_length': self._max_length,
                'required': self._required,
                'value': self._value, 'placeholder': self._value}
        if self._placeholder:
            json['placeholder'] = self._placeholder
        if self._value:
            json['value'] = self._value
        return json


class Modal:
    def __init__(self):
        self._title = 'placeholder'
        self._custom_id = 'placeholder'
        self._components = []

    def title(self, title):
        self._title = title
        return self

    def custom_id(self, custom_id):
        self._custom_id = custom_id
        return self

    def add_component(self, component):
        self._components.append(component)
        return self

    def to_json(self):
        components = [i.to_json() for i in self._components]
        return {'title': self._title, 'custom_id': self._custom_id, 'components': components}
