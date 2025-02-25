import backoff
from flywheel.rest import ApiException
from fw_client import FWClient


def is_not_500_502_504(exc):
    if hasattr(exc, "status"):
        if exc.status in [504, 502, 500]:
            # 500: Internal Server Error
            # 502: Bad Gateway
            # 504: Gateway Timeout
            return False
    return True


@backoff.on_exception(
    backoff.expo, ApiException, max_time=60, giveup=is_not_500_502_504
)
# will retry for 60s, waiting an exponentially increasing delay between retries
# e.g. 1s, 2s, 4s, 8s, etc, giving up if exception is in 500, 502, 504.
def robust_client_call(client: FWClient, action: str, endpoint: str, **kwargs):
    action = action.lower()
    if action not in ["get", "put", "patch", "delete", "post"]:
        raise ValueError(f"Invalid API action {action}")
    client_method = getattr(client, action)
    response = client_method(endpoint, **kwargs)
    return response
