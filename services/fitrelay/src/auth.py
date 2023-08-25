"""
Handles user Fitbit authentication and receiving OAuth token.
"""

from fastapi import APIRouter, Depends, HTTPException
from .db import insert_token, get_token
from .model import Token

router = APIRouter()


@router.get("/fitbit/authorize")
def authorize():
    # Make an authorization request
    # Extract access token and refresh token
    # Call `insert_token` to store the tokens in DB
    pass


@router.get("/fitbit/refresh")
def refresh():
    # Make a refresh token request
    # Update the tokens in DB
    pass
