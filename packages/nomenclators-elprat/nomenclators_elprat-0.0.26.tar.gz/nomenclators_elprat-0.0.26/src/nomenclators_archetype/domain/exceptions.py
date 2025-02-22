"""
----------------------------------------------------------------------------------------------------
Written by:
  - Yovany Dominico Girón (y.dominico.giron@elprat.cat)

for Ajuntament del Prat de Llobregat
----------------------------------------------------------------------------------------------------

----------------------------------------------------------------------------------------------------
"""


class InvalidEventTypeException(Exception):
    """Raised when the event does not inherit from BaseEvent."""

    def __init__(self):
        super().__init__("Event must inherit BaseEvent")


class InvalidParameterTypeException(Exception):
    """Raised when the parameter does not inherit from BaseModel."""

    def __init__(self):
        super().__init__("Parameter must inherit BaseModel")


class EmptyContextException(Exception):
    """Raised when the event context is empty."""

    def __init__(self):
        super().__init__("Event context is empty. check if middleware configured well")


class ParameterCountException(Exception):
    """Raised when the event has too many parameters."""

    def __init__(self):
        super().__init__("Event has too many parameter")


class RequiredParameterException(Exception):
    """Raised when the event require parameter."""

    def __init__(self, cls_name):
        super().__init__(f"`{cls_name}` event require parameter")


class RequiredElementError(Exception):
    """Raised when the event require element on Class"""

    def __init__(self, cls_name):
        super().__init__(f"`{cls_name}` event require element")
