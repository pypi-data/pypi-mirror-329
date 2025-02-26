# coding: utf-8

# flake8: noqa

from .configuration import Configuration
from .api_client import ApiClient


from autoenhance.api.images_api import ImagesApi
from autoenhance.api.orders_api import OrdersApi

from autoenhance.models.bracket_out import BracketOut
from autoenhance.models.http_error import HTTPError
from autoenhance.models.image_created_out import ImageCreatedOut
from autoenhance.models.image_in import ImageIn
from autoenhance.models.image_in_update import ImageInUpdate
from autoenhance.models.image_out import ImageOut
from autoenhance.models.order_brackets_out import OrderBracketsOut
from autoenhance.models.order_hdr_merge import OrderHDRMerge
from autoenhance.models.order_in import OrderIn
from autoenhance.models.order_out import OrderOut
from autoenhance.models.orders_out import OrdersOut
from autoenhance.models.pagination import Pagination
from autoenhance.models.report_in import ReportIn
from autoenhance.models.validation_error import ValidationError
from autoenhance.models.validation_error_detail import ValidationErrorDetail
from autoenhance.models.validation_error_detail_location import ValidationErrorDetailLocation

__version__ = "1.0.7"
__api_version__ = "2025-01-01"

class Autoenhance(ApiClient, ImagesApi, OrdersApi):

    def __init__(self, apiKey: str, baseURL: str = 'https://api.autoenhance.ai'):
        self.configuration = Configuration(host=baseURL)
        self.configuration.api_key["ApiKeyAuth"] = apiKey

        super().__init__(self.configuration)

        ImagesApi.__init__(self, self)
        OrdersApi.__init__(self, self)

        self.user_agent = f"Autoenhance/Python {__version__}"
        self.default_headers['x-api-version'] = __api_version__

    def create_image(self, **kwargs):
        kwargs['image_in'] = ImageIn.from_dict(kwargs)
        return super().create_image(image_in=kwargs.get('image_in', None)) 
    def delete_image(self, **kwargs):
        return super().delete_image(id=kwargs.get('id', None)) 
    def download_enhanced_image(self, **kwargs):
        return super().download_enhanced_image(id=kwargs.get('id', None), quality=kwargs.get('quality', None), format=kwargs.get('format', None), preview=kwargs.get('preview', None), watermark=kwargs.get('watermark', None), max_width=kwargs.get('max_width', None), scale=kwargs.get('scale', None)) 
    def download_original_image(self, **kwargs):
        return super().download_original_image(id=kwargs.get('id', None), quality=kwargs.get('quality', None), format=kwargs.get('format', None), preview=kwargs.get('preview', None), watermark=kwargs.get('watermark', None), max_width=kwargs.get('max_width', None), scale=kwargs.get('scale', None)) 
    def report_image(self, **kwargs):
        kwargs['report_in'] = ReportIn.from_dict(kwargs)
        return super().report_image(id=kwargs.get('id', None), report_in=kwargs.get('report_in', None)) 
    def retrieve_image(self, **kwargs):
        return super().retrieve_image(id=kwargs.get('id', None)) 
    def v3_images_id_process_post(self, **kwargs):
        kwargs['image_in_update'] = ImageInUpdate.from_dict(kwargs)
        return super().v3_images_id_process_post(id=kwargs.get('id', None), image_in_update=kwargs.get('image_in_update', None)) 

    def create_order(self, **kwargs):
        kwargs['order_in'] = OrderIn.from_dict(kwargs)
        return super().create_order(order_in=kwargs.get('order_in', None)) 
    def delete_order(self, **kwargs):
        return super().delete_order(id=kwargs.get('id', None)) 
    def list_orders(self, **kwargs):
        return super().list_orders(offset=kwargs.get('offset', None), per_page=kwargs.get('per_page', None)) 
    def merge_hdr(self, **kwargs):
        kwargs['order_hdr_merge'] = OrderHDRMerge.from_dict(kwargs)
        return super().merge_hdr(id=kwargs.get('id', None), order_hdr_merge=kwargs.get('order_hdr_merge', None)) 
    def retrieve_order(self, **kwargs):
        return super().retrieve_order(id=kwargs.get('id', None)) 
    def update_order(self, **kwargs):
        kwargs['order_in'] = OrderIn.from_dict(kwargs)
        return super().update_order(id=kwargs.get('id', None), order_in=kwargs.get('order_in', None)) 
    def v3_orders_order_id_brackets_get(self, **kwargs):
        return super().v3_orders_order_id_brackets_get(order_id=kwargs.get('order_id', None)) 

