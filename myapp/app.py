import json
import logging
from typing import Optional

from fastapi.param_functions import Depends
from fastapi.responses import HTMLResponse, PlainTextResponse
from pydantic import BaseSettings
from saleor_app.app import SaleorApp
from saleor_app.deps import ConfigurationFormDeps
from saleor_app.schemas.handlers import SaleorEventType
from saleor_app.schemas.core import DomainName, WebhookData
from saleor_app.schemas.manifest import Manifest
from saleor_app.schemas.utils import LazyUrl
from sqlmodel import Session
from sqlalchemy import select
from myapp.configuration.settings import (
    DOMAIN_IP,
    DATA_PRIVACY_URL,
    HOMEPAGE_URL,
    SUPPORT_URL,
    ID,
    APP_URL,
)

from myapp.database import create_db_and_tables, engine, SessionLocal
from myapp.inpost.models import Keys
from myapp.inpost.webhooks import shipping_list_methods_for_checkout

from myapp.inpost.router import router as inpost_router


class Settings(BaseSettings):
    """This is class for BaseSettings"""

    debug: bool = False
    development_auth_token: Optional[str] = None


settings = Settings(
    debug=True,
    development_auth_token="token_test",
)


async def validate_domain(saleor_domain: str) -> bool:
    """This def validate_domain"""
    logging.debug("validating domain %s", saleor_domain)

    with SessionLocal() as session:
        db_config = await Keys.get_domain_config(session, saleor_domain)

    if db_config:
        return True

    return False


class SaleorDomainNotFound(Exception):
    """This is class for created Exception"""


async def validate_domain_db(saleor_domain: str):
    """
    This def checking if saleor_domain is in database.
    When saleor_domain is active def validate_domain_db return True.
    When saleor_domain isn't active def validate_domain_db return False
    """
    # breakpoint()
    try:
        with Session(engine) as session:
            query = select(Keys).where(
                Keys.is_active.is_(True),
                Keys.saleor_domain == saleor_domain,
            )
            # breakpoint()

            results = session.exec(query)
            for keys in results:
                return True

    except SaleorDomainNotFound as saleor_domain_not_found:
        if not keys.is_active:
            print("Saleor domain for 'is_active' == False")
            return False
        return saleor_domain_not_found


class KeysMissing(Exception):
    pass


async def store_app_data(
    saleor_domain: DomainName, auth_token: str, webhook_data: WebhookData
):
    """This def called store_app_data"""

    logging.debug("storing app data %s", saleor_domain)

    with SessionLocal() as session:

        config = await Keys.get_domain_config(session, saleor_domain)

        if not config:
            raise KeysMissing("Keys missing")

        # breakpoint()
        config.saleor_domain = saleor_domain
        # breakpoint()
        config.saleor_auth_token = auth_token

        if webhook_data:
            config.webhook_id = webhook_data.webhook_id
            config.saleor_webhook_secret = webhook_data.webhook_secret_key

        session.commit()


async def get_webhook_details(saleor_domain: DomainName):
    """
    This def return webhook_details:
    - webhook_id
    - webhook_secret_key
    """
    # breakpoint()
    with SessionLocal() as session:
        config = await Keys.get_domain_config(session, saleor_domain)
        if not config:
            raise KeysMissing("Keys missing")

    return WebhookData(
        webhook_id=config.webhook_id,
        webhook_secret_key=config.webhook_secret,
    )


manifest = Manifest(
    name="Sample Saleor App",
    version="0.1.0",
    about="Sample Saleor App seving as an example",
    data_privacy="",
    data_privacy_url=DATA_PRIVACY_URL,
    homepage_url=HOMEPAGE_URL,
    support_url=SUPPORT_URL,
    id=ID,
    permissions=["MANAGE_PRODUCTS", "MANAGE_USERS", "MANAGE_ORDERS"],
    app_url=LazyUrl(APP_URL),
    extensions=[],
)

app = SaleorApp(
    manifest=manifest,
    validate_domain=validate_domain_db,
    save_app_data=store_app_data,
    use_insecure_saleor_http=settings.debug,
    development_auth_token=settings.development_auth_token,
)
app.include_webhook_router(get_webhook_details=get_webhook_details)
app.include_router(inpost_router)
app.include_saleor_app_routes()

app.webhook_router.http_event_route(SaleorEventType.SHIPPING_LIST_METHODS_FOR_CHECKOUT)(
    shipping_list_methods_for_checkout
)


@app.on_event("startup")
def on_startup():
    """This def creating db and tables"""

    create_db_and_tables()


@app.get("/", response_class=HTMLResponse, name=APP_URL)
async def get_public_form(commons: ConfigurationFormDeps = Depends()):
    """
    This def check configuration for:
    - request
    - form_url
    - saleor_domain
    """

    context = {
        "request": str(commons.request),
        "form_url": str(commons.request.url),
        "saleor_domain": commons.saleor_domain,
    }
    return PlainTextResponse(json.dumps(context, indent=4))
