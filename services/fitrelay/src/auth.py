"""
Handles user Fitbit authentication and receiving OAuth token.
"""
import secrets
import hashlib
import base64
import json
import time
from urllib.parse import quote

from fastapi import APIRouter, Request, Response, HTTPException
from fastapi.responses import RedirectResponse
import requests

from db import insert_token_to_db, get_all_tokens_from_db
from models import TokenInfo, TokenResponse
from constants import (
    AUTH_URL,
    CLIENT_ID,
    CLIENT_SECRET,
    REDIRECT_URL,
    STATE,
    SCOPES,
    TOKEN_URL,
    USER_PROFILE_URL,
)

router = APIRouter()


def _get_client_auth_header() -> str:
    auth_token = base64.b64encode(
        f"{CLIENT_ID}:{CLIENT_SECRET}".encode("utf-8")
    ).decode("utf-8")
    auth_header = f"Basic {auth_token}"
    return {"Authorization": auth_header}


def _get_token(code_verifier: str, code: str) -> dict:
    # Create the authorization code grant request body
    auth_header = _get_client_auth_header()

    # Send a request to the token URL to exchange the authorization code for an access token
    token_response = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "authorization_code",
            "client_id": CLIENT_ID,
            "code_verifier": code_verifier,
            "redirect_uri": REDIRECT_URL,
            "code": code,
        },
        headers=auth_header,
        timeout=5,
    )

    return token_response.json()


@router.get("/login")
def login(request: Request) -> Response:
    """Redirect the user to the Fitbit authorization page."""
    # Generate the code verifier and code challenge
    code_verifier = secrets.token_hex(32)
    code_challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode()).digest())
        .decode()
        .rstrip("=")
    )

    # Save the code verifier in the user's session
    request.session["code_verifier"] = code_verifier

    # Construct the authorization URL
    auth_url = (
        f"{AUTH_URL}?"
        "response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={quote(REDIRECT_URL)}"
        f"&state={STATE}"
        f"&code_challenge={code_challenge}"
        f"&scope={'%20'.join(SCOPES)}"
        "&code_challenge_method=S256"
    )

    # Redirect the user to the authorization URL
    return RedirectResponse(auth_url)


@router.get("/callback")
def callback(request: Request, code: str, state: str) -> Response:
    """Exchange the authorization code for an access token."""
    # Validate the state value to protect against CSRF attacks

    if state != STATE:
        return Response(status_code=400, content="Invalid state value")

    # Get the code verifier from the user's session
    if "code_verifier" not in request.session:
        return Response(status_code=400, content="Missing code verifier in session")

    code_verifier = request.session["code_verifier"]
    token_response = _get_token(code_verifier, code)

    access_token = token_response["access_token"]

    # if the token has the user_id field, save it as json to the tokens/ folder
    if "user_id" not in token_response:
        raise HTTPException(
            status_code=400,
            detail="No user_id field in token response",
        )

    user_profile_response = requests.get(
        USER_PROFILE_URL.format(user_id=token_response["user_id"]),
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=5,
    )

    # Save the token in the database
    token = TokenInfo(
        user_id=token_response["user_id"],
        user_profile=user_profile_response.json(),
        token_response=token_response,
        created=int(time.time()),
    )
    insert_token_to_db(token)

    # Return the response from the protected resource
    return Response(
        content=json.dumps(user_profile_response.json(), indent=4),
        media_type="application/json",
    )


def refresh_tokens(leeway: int = 3600):
    all_tokens = get_all_tokens_from_db()
    for token in all_tokens:
        expire_time = token.created + token.token_response.expires_in
        # one hour leeway
        if expire_time < int(time.time()) - leeway:
            refresh_token(token)


def refresh_token(token: TokenInfo) -> TokenInfo:
    refresh_token = token.token_response.refresh_token
    auth_header = _get_client_auth_header()

    token_response = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        },
        headers={
            **auth_header,
            "Content-Type": "application/x-www-form-urlencoded",
        },
        timeout=5,
    )

    token.token_response = TokenResponse.model_validate(token_response.json())
    token.created = int(time.time())

    insert_token_to_db(token)
