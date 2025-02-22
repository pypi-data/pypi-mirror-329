from pydantic import Field
from pydantic_zarr.v2 import ArraySpec, GroupSpec

from ome_zarr_models._v05.base import BaseGroupv05, BaseOMEAttrs, BaseZarrAttrs
from ome_zarr_models._v05.image_label_types import Label
from ome_zarr_models._v05.multiscales import Multiscale

__all__ = ["ImageLabel", "ImageLabelAttrs"]


class ImageLabelAttrs(BaseOMEAttrs):
    """
    Attributes for an image label object.
    """

    image_label: Label = Field(..., alias="image-label")
    multiscales: list[Multiscale]


class ImageLabel(
    GroupSpec[BaseZarrAttrs[ImageLabelAttrs], ArraySpec | GroupSpec],  # type: ignore[misc]
    BaseGroupv05,
):
    """
    An OME-Zarr image label dataset.
    """
