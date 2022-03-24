from typing import List

from fastapi.param_functions import Depends
from saleor_app.deps import saleor_domain_header
from saleor_app.schemas.webhook import Webhook


async def shipping_list_methods_for_checkout(
    payload: List[Webhook], saleor_domain=Depends(saleor_domain_header)
):
    """
    This def is for shipping_list_methods_for_checkout
    :param payload:
    :param saleor_domain:
    :return:
    """
    print(payload, saleor_domain)
    await shipping_list_methods_for_checkout(payload, saleor_domain)
