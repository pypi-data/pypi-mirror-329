from typing import Any, Optional

from fused.models.api import UdfJobStepConfig
from fused.models.udf._eval_result import UdfEvaluationResult
from fused.models.udf.output import Output
from fused.models.udf.udf import load_udf_from_response_data


def get_step_config_from_server(
    email_or_handle: Optional[str],
    slug: str,
    cache_key: Any,
    _is_public: bool = False,
) -> UdfJobStepConfig:
    from fused.api.api import FusedAPI

    # cache_key is unused
    api = FusedAPI()
    if _is_public:
        obj = api._get_public_udf(slug)
    else:
        obj = api._get_udf(email_or_handle, slug)
    udf = load_udf_from_response_data(obj)

    step_config = UdfJobStepConfig(udf=udf)
    return step_config


def get_github_udf_from_server(
    url: str,
    cache_key: Any,
):
    from fused.api.api import FusedAPI

    # cache_key is unused
    # TODO: Do this locally in fused-py
    api = FusedAPI(credentials_needed=False)
    obj = api._get_code_by_url(url)
    udf = load_udf_from_response_data(obj)

    step_config = UdfJobStepConfig(udf=udf)
    return step_config


def run_and_get_data(udf, *args, **kwargs):
    # TODO: This is a silly way to do this, because we have to pass parameters in such an odd way
    job = udf(*args, **kwargs)
    result = job.run_local()
    if isinstance(result, (Output, UdfEvaluationResult)):
        return result.data
    else:
        return result


def get_step_config_from_shared_token(token: str) -> UdfJobStepConfig:
    from fused.api.api import FusedAPI

    api = FusedAPI()
    token = api.get_udf_access_token(token)
    obj = api._get_udf_by_id(token.udf_id)
    udf = load_udf_from_response_data(obj)
    return UdfJobStepConfig(udf=udf)
