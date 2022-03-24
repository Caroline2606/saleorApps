from typing import List, Optional

import requests
from fastapi import APIRouter
from sqlmodel import Session, select
from myapp.configuration.settings import INPOST_URL, VALIDATE_IP

from myapp.database import engine
from myapp.inpost import models

router = APIRouter(prefix="/inpost")

"""INPOST_URL = "https://api-shipx-pl.easypack24.net/v1/points/"""


@router.get("/test_one", tags=["inpost_tests"])
async def read_url(post_code: str):
    """
    This def read INPOST_URL,
    then user's typing post_code,
    and return points according to user post_code
    """

    search = f"{INPOST_URL}/?post_code=" f"{post_code}"
    response = requests.get(search)
    data = response.json()

    return data


@router.get("/test_two", tags=["inpost_tests"])
async def read_validate_domain_db():
    """This def is a test for validate_domain_db
    in app.py. It's working with pdb"""

    from myapp.app import validate_domain_db

    await validate_domain_db(VALIDATE_IP)


@router.post("/keys", response_model=models.Keys, tags=["inpost_database"])
async def save_keys(
    inpost_api_key: str,
    saleor_domain: str,
    is_active: bool,
    saleor_auth_token: str,
    saleor_webhook_secret: str,
):
    """This def saves keys into database"""

    key = models.Keys(
        inpost_api_key=inpost_api_key,
        saleor_domain=saleor_domain,
        is_active=is_active,
        saleor_auth_token=saleor_auth_token,
        saleor_webhook_secret=saleor_webhook_secret,
    )
    with Session(engine) as session:
        session.add(key)
        session.commit()
        session.refresh(key)
        return key


@router.get(
    "/get_configuration",
    response_model=List[models.Keys],
    tags=["inpost_configuration"],
)
async def get_configuration(inpost_org_id: int):
    """This def get information from database
    after inpost_org_id"""

    with Session(engine) as session:
        statement = select(models.Keys).where(
            models.Keys.inpost_org_id == inpost_org_id
        )
        results = session.exec(statement)
        keys = []
        for key in results.all():
            keys.append(models.Keys.from_orm(key))
        return keys


@router.post(
    "/update_configuration", response_model=models.Keys, tags=["inpost_configuration"]
)
async def update_configuration(
    inpost_org_id: int,
    inpost_api_key: Optional[str] = None,
    saleor_domain: Optional[str] = None,
    is_active: Optional[bool] = None,
    saleor_auth_token: Optional[str] = None,
    saleor_webhook_secret: Optional[str] = None,
):
    """
    This def update information from database.
    User typing inpost_org_id and inpost_api_key,
    then user updating information.
    """

    with Session(engine) as session:
        statement = select(models.Keys).where(
            models.Keys.inpost_org_id == inpost_org_id
            and models.Keys.inpost_api_key == inpost_api_key
        )

        results = session.exec(statement)
        keys = []

        for key in results.all():
            keys.append(models.Keys.from_orm(key))

            key.saleor_domain = saleor_domain
            key.is_active = is_active
            key.saleor_auth_token = saleor_auth_token
            key.saleor_webhook_secret = saleor_webhook_secret

            session.add(key)
        session.commit()


@router.delete(
    "/delete_configuration",
    response_model=List[models.Keys],
    tags=["inpost_configuration"],
)
async def delete_configuration(
    inpost_org_id: int,
):
    """This def deletes information from database.
    User typing inpost_org_id and delete information."""

    with Session(engine) as session:
        statement = select(models.Keys).where(
            models.Keys.inpost_org_id == inpost_org_id
        )

        results = session.exec(statement)
        keys = []

        for key in results.all():
            keys.append(models.Keys.from_orm(key))

            session.delete(key)
            session.commit()
