import logging
from . import recipe
from pydantic import ValidationError
from pydantic.v1 import ValidationError as ValidationError_v1
from .recipe_2_2 import Recipe as Recipe_2_2
from .recipe_2_1 import Recipe as Recipe_2_1
from .recipe_1_0 import Recipe as Recipe_1_0

logger = logging.getLogger(__name__)

models = {
    "2.2": Recipe_2_2,
    "2.1": Recipe_2_1,
    "1.0": Recipe_1_0,
}


def to_recipe(**kwargs):
    firste = None
    for ver, Model in models.items():
        try:
            payload = Model(**kwargs)
            return payload
        except (ValidationError, ValidationError_v1) as e:
            logger.info("Could not parse 'kwargs' using Recipe v%s.", ver)
            logger.info(e)
            if firste is None:
                firste = e
    raise ValueError(firste)


__all__ = [
    "recipe",
    "to_recipe",
]
