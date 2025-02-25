from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from .. import errors
from ..client import AuthenticatedClient, Client
from ...models.user_login_dto import UserLoginDto
from qubicon.api.types import Response


def _get_kwargs(
    *,
    body: UserLoginDto,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {
        "Content-Type": "application/json",  # Explicitly set the Content-Type
    }

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/public-api/login",
        "json": body.to_dict(),  # Send the body as JSON
        "headers": headers,      # No Authorization header
    }

    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Any]:
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: UserLoginDto,
) -> Response[Any]:
    """
    Perform a login request with no additional headers or authorization.

    Args:
        client: The client to use for the request.
        body: The login data.

    Returns:
        Response[Any]: The response from the server.
    """
    # Extract the base_url from the client
    base_url = client.base_url if hasattr(client, "base_url") else getattr(client, "_base_url", None)
    if not base_url:
        raise ValueError("The 'base_url' is not set on the client object.")
    
    # Define headers explicitly to ensure no 'Authorization' or JWT headers are included
    headers = {
        "Content-Type": "application/json",  # Match Postman behavior
    }

    # Create a direct httpx client and make the POST request
    with httpx.Client(base_url=base_url, headers=headers) as http_client:
        response = http_client.post(
            "/public-api/login",
            json=body.to_dict(),  # Ensure the payload matches Postman
        )

    # Log the response for debugging purposes
    print("Request Headers:", headers)
    print("Request Payload:", body.to_dict())
    print("Response Status:", response.status_code)
    print("Response Body:", response.text)

    # Return the response as expected by the rest of the system
    return _build_response(client=client, response=response)



async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: UserLoginDto,
) -> Response[Any]:
    """
    Args:
        body (UserLoginDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
