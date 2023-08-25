"""
Handles user Fitbit authentication and receiving OAuth token.
"""
import secrets
import hashlib
import base64
import json
from urllib.parse import quote

from fastapi import APIRouter, Request, Response, HTTPException
from fastapi.responses import RedirectResponse
import requests

from db import insert_token_to_db, get_token_from_db
from models import Token
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


def _get_token(code_verifier: str, code: str) -> dict:
    # Create the authorization code grant request body
    auth_token = base64.b64encode(
        f"{CLIENT_ID}:{CLIENT_SECRET}".encode("utf-8")
    ).decode("utf-8")
    auth_header = f"Basic {auth_token}"

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
        headers={"Authorization": auth_header},
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
    token = Token(
        access_token=token_response["access_token"],
        refresh_token=token_response["refresh_token"],
        user_id=token_response["user_id"],
        user_profile=user_profile_response.json(),
    )
    insert_token_to_db(token)

    # Return the response from the protected resource
    return Response(
        content=json.dumps(user_profile_response.json(), indent=4),
        media_type="application/json",
    )
