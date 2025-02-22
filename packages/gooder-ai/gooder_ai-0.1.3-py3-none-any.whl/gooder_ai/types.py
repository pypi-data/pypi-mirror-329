from typing import TypedDict, Literal, NotRequired
from pandas import DataFrame


class ValuateModelParams(TypedDict):
    email: str
    password: str
    data: DataFrame
    config: dict
    mode: Literal["public", "protected", "private"]

    view_id: NotRequired[str]
    dataset_name: NotRequired[str]

    # AWS Global Variables
    api_url: NotRequired[str]
    app_client_id: NotRequired[str]
    identity_pool_id: NotRequired[str]
    user_pool_id: NotRequired[str]
    bucket_name: NotRequired[str]
    base_url: NotRequired[str]
    validation_api_url: NotRequired[str]
