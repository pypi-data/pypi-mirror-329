import logging
from . import dataschema
from pydantic import ValidationError
from pydantic.v1 import ValidationError as ValidationError_v1
from .dataschema_6_0 import DataSchema as DataSchema_6_0
from .dataschema_5_1 import DataSchema as DataSchema_5_1
from .dataschema_5_0 import DataSchema as DataSchema_5_0, Metadata as Metadata_5_0
from .dataschema_4_2 import DataSchema as DataSchema_4_2, Metadata as Metadata_4_2
from .dataschema_4_1 import DataSchema as DataSchema_4_1, Metadata as Metadata_4_1
from .dataschema_4_0 import DataSchema as DataSchema_4_0, Metadata as Metadata_4_0

logger = logging.getLogger(__name__)

models = {
    "6.0": (DataSchema_6_0, None),
    "5.1": (DataSchema_5_1, None),
    "5.0": (DataSchema_5_0, Metadata_5_0),
    "4.2": (DataSchema_4_2, Metadata_4_2),
    "4.1": (DataSchema_4_1, Metadata_4_1),
    "4.0": (DataSchema_4_0, Metadata_4_0),
}


def to_dataschema(**kwargs):
    # figure out matching Metadata -> identify correct Model:
    errors = ["Could not parse 'kwargs['metadata']' using any Metadata!", ""]
    for ver, tup in models.items():
        Model, Metadata = tup
        try:
            if Metadata is None:
                schema = Model(**kwargs)
                return schema
            else:
                Metadata(**kwargs["metadata"])
                break
        except (ValidationError, ValidationError_v1) as e:
            errors.append(
                f"Could not parse 'kwargs['metadata']' using Metadata v{ver}:"
            )
            errors += str(e).replace("\n", "\n ").split("\n")
            errors.append("")
    else:
        raise ValueError("\n".join(errors))

    logger.debug("Identified 'kwargs['metadata']' as Metadata v%s.", ver)

    # attempt to parse using identified Model
    schema = Model(**kwargs)
    return schema


__all__ = [
    "dataschema",
    "to_dataschema",
]
