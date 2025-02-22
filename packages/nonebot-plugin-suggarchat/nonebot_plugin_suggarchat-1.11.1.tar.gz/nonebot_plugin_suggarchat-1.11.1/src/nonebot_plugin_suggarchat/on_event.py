from .matcher import SuggarMatcher
from .event import EventType


def on_chat():
    return SuggarMatcher(event_type=EventType().chat(),priority=10)

def on_poke():
    return SuggarMatcher(event_type=EventType().poke(),priority=10)

