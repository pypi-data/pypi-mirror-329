from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from .book_authentication_descriptor import BookAuthenticationDescriptor
from .oauth_argument_descriptor import OauthArgumentDescriptor


class OAuthFlow(Enum):
    AUTHORIZATION_CODE = 0
    CLIENT_CREDENTIALS = 1


class OAuthProvider(Enum):
    MICROSOFT = 0
    GOOGLE = 1


@dataclass
class BookOAuthAuthenticationDescriptor(BookAuthenticationDescriptor):
    provider: OAuthProvider
    flows: List[OAuthFlow]
    authorize_endpoint: str
    token_endpoint: str
    scopes: Optional[List[str]]
    arguments: Optional[List[OauthArgumentDescriptor]] = None
    oauth_token_function_name: Optional[str] = None
