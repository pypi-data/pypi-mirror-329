from typing import Union

from ee.imagecollection import ImageCollection
from ee.feature import Feature
from ee.featurecollection import FeatureCollection
from ee.image import Image
from eeclient.typing import MapTileOptions
from ee.data import convert_asset_id_to_asset_name  # type: ignore: it will be imported from another moduel


def _get_ee_image(
    ee_object: Union[Image, ImageCollection, Feature, FeatureCollection],
    vis_params: Union[MapTileOptions, dict] = {},
):
    """Convert an Earth Engine object to a image request object"""

    def get_image_request(ee_image: Image, vis_params={}):

        vis_image, request = ee_image._apply_visualization(vis_params)
        request["image"] = vis_image

        return request

    if isinstance(ee_object, Image):
        return get_image_request(ee_object, vis_params)

    elif isinstance(ee_object, ImageCollection):

        ee_image = ee_object.mosaic()
        return get_image_request(ee_image, vis_params)

    elif isinstance(ee_object, Feature):
        ee_image = FeatureCollection(ee_object).draw(
            color=(vis_params or {}).get("color", "000000")
        )
        return get_image_request(ee_image)

    elif isinstance(ee_object, FeatureCollection):
        ee_image = ee_object.draw(color=(vis_params or {}).get("color", "000000"))
        return get_image_request(ee_image)

    else:
        raise ValueError("Invalid ee_object type")


def parse_cookie_string(cookie_string):
    cookies = {}
    for pair in cookie_string.split(";"):
        key_value = pair.strip().split("=", 1)
        if len(key_value) == 2:
            key, value = key_value
            cookies[key] = value
    return cookies
