from typing import List

import requests
from fastapi.param_functions import Depends
from saleor_app.deps import saleor_domain_header
from saleor_app.schemas.webhook import Webhook

from myapp.configuration.settings import INPOST_URL


async def shipping_list_methods_for_checkout(
    payload: List[Webhook], saleor_domain=Depends(saleor_domain_header)
):
    """
    This def is for shipping_list_methods_for_checkout
    :param payload:
    :param saleor_domain:
    :return:
    """

    # breakpoint()
    print(payload[0].shipping_address["postal_code"], saleor_domain)
    post_code = payload[0].shipping_address["postal_code"]
    search = f"{INPOST_URL}?post_code=" f"{post_code}"
    response = requests.get(search)
    data = response.json()
    items = data["items"]
    i = 0
    x = len(items) - 1
    tab = []
    while i <= x:
        item = items[i]
        address = item["address_details"]
        functions = item["functions"]
        lista = address, functions
        tab.append([i, lista])
        i += 1
    print(tab)
    return None

    # await shipping_list_methods_for_checkout(payload, saleor_domain)
