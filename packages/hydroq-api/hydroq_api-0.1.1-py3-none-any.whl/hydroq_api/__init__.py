import uuid
from datetime import timedelta, datetime
import re
from typing import Callable
import requests
from pkce import generate_pkce_pair

HOST_LOGIN = "https://connexion.solutions.hydroquebec.com"
HOST_SESSION = "https://session.hydroquebec.com"
HOST_SERVICES = "https://services-cl.solutions.hydroquebec.com"
HOST_RB_SOL = "https://rb.solutions.hydroquebec.com"
HOST_OUTAGES = "https://services-bs.solutions.hydroquebec.com"
HOST_OPEN_DATA = "https://donnees.solutions.hydroquebec.com"

# Azure B2C
AZB2C_TENANT_ID = "32bf9b91-0a36-4385-b231-d9a8fa3b05ab"
AZB2C_POLICY = "B2C_1A_PRD_signup_signin"
AZB2C_CLIENT_ID_WEB = "09b0ae72-6db8-4ecc-a1be-041b67afc1cd"
AZB2C_CLIENT_ID_MOBILE = "70cd7b23-de9a-4d74-8592-d378afbfb863"
AZB2C_RESPONSE_TYPE = "code"
AZB2C_SCOPE_WEB = ("openid https://connexionhq.onmicrosoft.com/hq-clientele/Espace.Client")
AZB2C_CODE_CHALLENGE_METHOD = "S256"

# Time to remove from the token expiration time to avoid calls to fail
AZB2C_TIMEOUT_SKEW_SECS = 60

# OAUTH PATHS
AUTHORIZE_URL = (
    f"{HOST_LOGIN}/{AZB2C_TENANT_ID}/{AZB2C_POLICY.lower()}/oauth2/v2.0/authorize"
)
AUTH_URL = f"{HOST_LOGIN}/{AZB2C_TENANT_ID}/{AZB2C_POLICY}/SelfAsserted"
AUTH_URL_COMB = f"{HOST_LOGIN}/{AZB2C_TENANT_ID}/{AZB2C_POLICY}/api/CombinedSigninAndSignup/confirmed"
AUTH_CALLBACK_URL = f"{HOST_SESSION}/oauth2/callback"
TOKEN_URL = f"{HOST_LOGIN}/{AZB2C_TENANT_ID}/{AZB2C_POLICY.lower()}/oauth2/v2.0/token"

CONTRACT_SUMMARY_URL = (
    f"{HOST_SERVICES}/wsapi/web/prive/api/v3_0/partenaires/"
    "calculerSommaireContractuel?indMAJNombres=true"
)
CONTRACT_LIST_URL = f"{HOST_SERVICES}/wsapi/web/prive/api/v3_0/partenaires/contrats"

CUSTOMER_INFO_URL = f"{HOST_SERVICES}/wsapi/web/prive/api/v3_0/partenaires/infoCompte"

RELATION_URL = f"{HOST_SERVICES}/wsapi/web/prive/api/v1_0/relations"

PORTRAIT_URL = (f"{HOST_SERVICES}/lsw/portail/fr/group/clientele/portrait-de-consommation")
SESSION_URL = f"{HOST_SERVICES}/lsw/portail/prive/maj-session"
DAILY_USAGE_URL = f"{PORTRAIT_URL}/resourceObtenirDonneesQuotidiennesConsommation"
HOURLY_USAGE_URL = f"{PORTRAIT_URL}/resourceObtenirDonneesConsommationHoraires"
MONTHLY_USAGE_URL = f"{PORTRAIT_URL}/resourceObtenirDonneesConsommationMensuelles"


class HydroQuebec:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.guid: str = str(uuid.uuid1())
        self.code = None
        self.access_token = None
        self.refresh_token = None

    def login(self):
        code_verifier, code_challenge = generate_pkce_pair()

        # Step 1: Get the CSRF token and transId
        headers = {"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}
        params = {
            "redirect_uri": AUTH_CALLBACK_URL,
            "client_id": AZB2C_CLIENT_ID_WEB,
            "response_type": "code",
            "scope": AZB2C_SCOPE_WEB,
            "prompt": "login",
            "ui_locales": "fr",
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
            "mobile": "false",
        }
        res = self.session.get(AUTHORIZE_URL, headers=headers, params=params)
        html_data = res.text

        try: 
            self.csrf_token = re.search(r'csrf":"(.+?)"', html_data).group(1)
        except:
            print("Login error finding csrf token")

        try:
            self.transid = re.search(r'transId":"(.+?)"', html_data).group(1)
        except:
            print("Login error finding trans Id")
        
        # Step 2: Submit the login form
        params = {
            "tx": self.transid,
            "p": AZB2C_POLICY,
        }
        headers = {
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "accept": "application/json, text/javascript, */*; q=0.01",
            "x-csrf-token": self.csrf_token,
        }

        payload = {
            "request_type": "RESPONSE",
            "signInName": self.username,
            "password": self.password,
        }
        res = self.session.post(AUTH_URL, headers=headers, data=payload, params=params, timeout=10)
        if res.status_code != 200:
            print("Login error")
            return

        # Step 3: Get redirect URL and code
        params = {
            "rememberMe": "false",
            "csrf_token": self.csrf_token,
            "tx": self.transid,
            "p": AZB2C_POLICY,
        }
        headers = {"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}
        res = self.session.get(AUTH_URL_COMB, headers=headers, params=params, timeout=10)

        try:
            self.code = re.search(r"code=(.+?)$", res.request.path_url).group(1)
        except:
            print("Login error finding code attribute in location header")

        # Step 4: Get the access token
        headers = {"content-type": "application/x-www-form-urlencoded", "accept": "*/*"}
        data = {
            "grant_type": "authorization_code",
            "client_id": AZB2C_CLIENT_ID_WEB,
            "redirect_uri": AUTH_CALLBACK_URL,
            "code": self.code,
            "code_verifier": code_verifier,
        }
        res = self.session.post(TOKEN_URL, headers=headers, data=data, timeout=10)
        res_json = res.json()

        self.id_token = res_json["id_token"]
        self.access_token = res_json["access_token"]
        self.access_token_expiry = datetime.now() + timedelta(
            seconds=int(res_json["expires_in"]) - AZB2C_TIMEOUT_SKEW_SECS
        )
        self.refresh_token = res_json["refresh_token"]
        self.refresh_token_expiry = datetime.now() + timedelta(
            seconds=int(res_json["refresh_token_expires_in"]) - AZB2C_TIMEOUT_SKEW_SECS
        )

        # relation info
        relation_info = self.session.get(RELATION_URL, headers={"Authorization": "Bearer " + self.access_token})
        self.applicant_id = relation_info.json()[0]["noPartenaireDemandeur"]
        self.customer_id = relation_info.json()[0]["noPartenaireTitulaire"]


    def _refresh_token(self) -> bool:
        """Refresh current session."""

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json, text/plain, */*",
        }
        data = {
            "grant_type": "refresh_token",
            "scope": AZB2C_SCOPE_WEB,
            "client_id": AZB2C_CLIENT_ID_WEB,
            "refresh_token": self.refresh_token,
        }

        res = self.session.post(TOKEN_URL, headers=headers, data=data)
        res_json = res.json()

        self.id_token = res_json["id_token"]
        self.access_token = res_json["access_token"]
        self.access_token_expiry = datetime.now() + timedelta(
            seconds=int(res_json["expires_in"]) - AZB2C_TIMEOUT_SKEW_SECS
        )
        self.refresh_token = res_json["refresh_token"]
        self.refresh_token_expiry = datetime.now() + timedelta(
            seconds=int(res_json["refresh_token_expires_in"]) - AZB2C_TIMEOUT_SKEW_SECS
        )
        return True

    def _get_customer_headers(self, force_refresh: bool = False) -> dict[str, str]:
        """Prepare http headers for customer url queries."""
        if force_refresh: self._refresh_token()
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.access_token,
            "NO_PARTENAIRE_DEMANDEUR": self.applicant_id,
            "NO_PARTENAIRE_TITULAIRE": self.customer_id,
            "DATE_DERNIERE_VISITE": datetime.now().strftime(
                "%Y-%m-%dT%H:%M:%S.000+0000"
            ),
            "GUID_SESSION": self.guid,
        }
        return headers

    def requires_web_session(func: Callable) -> Callable:
        def wrapper(self, *args, **kwargs):
            current_time = datetime.now()
            
            # Create session if it doesn't exist or is older than 5 minutes
            if not hasattr(self, '_session_created_at') or (current_time - self._session_created_at).total_seconds() > 300:
                contract_summary = self.session.get(CONTRACT_SUMMARY_URL, headers=self._get_customer_headers())
                contract_num = contract_summary.json()["comptesContrats"][0]["listeNoContrat"][0]
                self.session = requests.Session()
                new_token = self._get_customer_headers(force_refresh=True)
                params = {"mode": "web"}
                self.session.get(SESSION_URL, params=params, headers=new_token)
                self._get_portrait(contract_num)
                self._session_created_at = current_time
                
            return func(self, *args, **kwargs)
        return wrapper 

    def _get_portrait(self, conctract_num: str) -> None:
        """Load user snapshot information."""
        params = {"noContrat": conctract_num}
        self.session.get(PORTRAIT_URL, headers=self._get_customer_headers(), params=params)

    @requires_web_session
    def get_daily_usage(self, start_date: str, end_date: str) -> dict:
        """Get daily usage for a given period. It seems that about 2 years worth of 
        daily data is available
        """
        params = {
            "dateDebut": start_date,
            "dateFin": end_date,
        }
        headers = self._get_customer_headers()
        r = self.session.get(DAILY_USAGE_URL, params=params, headers=headers)
        r.raise_for_status()
        return r.json()

    @requires_web_session
    def get_hourly_usage(self, date: str) -> dict:
        """Get hourly usage for a given date."""
        params = {"date": date}
        headers = self._get_customer_headers()
        r = self.session.get(HOURLY_USAGE_URL, params=params, headers=headers)
        r.raise_for_status()
        return r.json()

    @requires_web_session
    def get_monthly_usage(self) -> dict:
        """Get monthly usage for last year and previous year as comparable."""
        headers = self._get_customer_headers()
        r = self.session.get(MONTHLY_USAGE_URL, headers=headers)
        r.raise_for_status()
        return r.json()