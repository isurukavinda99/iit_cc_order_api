import os
import time
import requests
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from typing import Optional, Dict
from fastapi import Depends

class ALBCognitoAuth(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)
        self._validate_config()
        self._jwks_cache = None
        self._jwks_cache_time = 0
        self._jwks_cache_ttl = 3600

    def _validate_config(self):
        required_vars = ['COGNITO_USER_POOL_ID', 'AWS_REGION', 'COGNITO_CLIENT_ID']
        missing = [var for var in required_vars if not os.getenv(var)]
        if missing:
            raise RuntimeError(f"Missing environment variables: {', '.join(missing)}")

    @property
    def issuer(self) -> str:
        return f"https://cognito-idp.{os.getenv('AWS_REGION')}.amazonaws.com/{os.getenv('COGNITO_USER_POOL_ID')}"

    @property
    def jwks_url(self) -> str:
        return f"{self.issuer}/.well-known/jwks.json"

    def _get_jwks(self) -> dict:
        now = time.time()
        if self._jwks_cache and now - self._jwks_cache_time < self._jwks_cache_ttl:
            return self._jwks_cache
        resp = requests.get(self.jwks_url)
        resp.raise_for_status()
        self._jwks_cache = resp.json()
        self._jwks_cache_time = now
        return self._jwks_cache

    def _get_public_key(self, kid: str):
        jwks = self._get_jwks()
        for key in jwks.get('keys', []):
            if key.get('kid') == kid:
                return key
        return None

    async def __call__(self, request: Request) -> Optional[Dict]:
        # Skip auth for flagged paths (middleware can set request.state.skip_auth)
        if getattr(request.state, "skip_auth", False):
            return None

        # If ALB header present, validate ALB token
        if "x-amzn-oidc-data" in request.headers:
            return self._process_alb_token(request)

        # Otherwise, validate Bearer token directly (for dev/test)
        return await self._process_bearer_token(request)

    def _process_alb_token(self, request: Request) -> Dict:
        try:
            token = request.headers["x-amzn-oidc-data"]
            claims = jwt.get_unverified_claims(token)
            request.state.claims = claims
            return claims
        except JWTError as e:
            raise HTTPException(status_code=403, detail=f"Invalid ALB token: {str(e)}")

    async def _process_bearer_token(self, request: Request) -> Dict:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials.scheme.lower() != "bearer":
            raise HTTPException(status_code=403, detail="Invalid authentication scheme")

        token = credentials.credentials
        try:
            headers = jwt.get_unverified_header(token)
            kid = headers.get("kid")
            if not kid:
                raise HTTPException(status_code=403, detail="Missing kid in token header")

            key = self._get_public_key(kid)
            if not key:
                raise HTTPException(status_code=403, detail="Public key not found in JWKS")

            claims = jwt.decode(
                token,
                key,
                algorithms=key.get("alg", "RS256"),
                issuer=self.issuer,
                audience=os.getenv("COGNITO_USER_POOL_ID"), #COGNITO_USER_POOL_ID
                options={"verify_aud": True},
            )
            request.state.claims = claims
            return claims
        except JWTError as e:
            raise HTTPException(status_code=403, detail=f"Invalid token: {str(e)}")

def require_auth(claims: Dict = Depends(ALBCognitoAuth())) -> Dict:
    return claims