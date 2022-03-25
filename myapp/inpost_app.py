import requests

from myapp.app import app
from myapp.configuration.settings import INPOST_URL

INPOST_API_URL = INPOST_URL


class InpostHttpError(Exception):
    """This is class for created Exception"""


def inpost_data(url):
    """This def checking response for url"""

    try:
        response = requests.get(url)
        response.raise_for_status()
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError):
        raise InpostHttpError("Fail to fetch Inpost data") from InpostHttpError
    return response.json()


@app.get("/inpost/")
async def read_inpost(post_code: str):
    """
    This def read INPOST_API_URL,
    then user's typing post_code,
    and return points according to user post_code
    """

    search = f"{INPOST_API_URL}/?post_code=" f"{post_code}"
    response = requests.get(search)
    data = response.json()

    return data


@app.get("/read_inpost/")
async def read_inpost_query(post_code: str):
    """This def check query and return data"""

    query = {"post_code": f"{post_code}"}

    response = requests.get(INPOST_API_URL, params=query)

    data = response.json()

    return data
