from typing import Literal
from dgbowl_schemas.dgpost.recipe_2_1 import Recipe as Recipe_2_1


class Recipe(Recipe_2_1, extra="forbid"):
    version: Literal["2.2"]
