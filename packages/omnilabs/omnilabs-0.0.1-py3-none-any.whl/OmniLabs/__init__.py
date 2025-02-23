"""
omnilabs
~~~~~~~~~~~~~~

A Python client for the OmniRouter API.

Basic usage:
    >>> from omnilabs import OmniClient, ChatMessage
    >>> client = OmniClient()
    >>> message = ChatMessage(role="user", content="Hello!")
    >>> response = client.chat([message], model="gpt-4")

:copyright: (c) 2025 by Satya Shah.
:license: MIT, see LICENSE for more details.
"""

from .OmniClient import OmniClient, ChatMessage

__all__ = ['OmniClient', 'ChatMessage']
