from pydantic import ValidationError
from pydantic.v1 import ValidationError as ValidationError_v1
import logging
from . import payload
from .payload_0_1 import Payload as Payload_0_1
from .payload_0_2 import Payload as Payload_0_2
from .payload_1_0 import Payload as Payload_1_0
from .payload_2_0 import Payload as Payload_2_0

logger = logging.getLogger(__name__)

models = {
    "2.0": Payload_2_0,
    "1.0": Payload_1_0,
    "0.2": Payload_0_2,
    "0.1": Payload_0_1,
}


def to_payload(**kwargs):
    firste = None
    for ver, Model in models.items():
        try:
            payload = Model(**kwargs)
            return payload
        except (ValidationError, ValidationError_v1) as e:
            logger.info("Could not parse 'kwargs' using Payload-%s.", ver)
            logger.debug(e)
            if firste is None:
                firste = e
    raise ValueError(firste)


__all__ = [
    "payload",
    "to_payload",
]
