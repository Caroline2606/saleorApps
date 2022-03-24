from typing import Optional

from sqlmodel import Field, SQLModel

from sqlmodel import select


class Keys(SQLModel, table=True):
    """This is a class which create Keys model"""

    inpost_org_id: Optional[int] = Field(default=None, primary_key=True)
    webhook_id: Optional[str]
    inpost_api_key: str
    saleor_domain: str
    is_active: bool
    saleor_auth_token: str
    saleor_webhook_secret: str

    @classmethod
    async def get_domain_config(cls, session, saleor_domain):
        statement = select(cls).where(cls.saleor_domain == saleor_domain)
        results = session.execute(statement)
        # breakpoint()
        keys = results.one_or_none()
        if keys:
            return keys[0]
