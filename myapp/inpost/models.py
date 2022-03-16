from typing import Optional

from sqlmodel import Field, SQLModel


class Keys(SQLModel, table=True):
    """This is a class which create Keys model"""

    inpost_org_id: Optional[int] = Field(default=None, primary_key=True)
    inpost_api_key: str
    saleor_domain: str
    is_active: bool
    saleor_auth_token: str
    saleor_webhook_secret: str
