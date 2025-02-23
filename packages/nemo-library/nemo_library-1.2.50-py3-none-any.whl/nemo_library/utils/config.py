import configparser
import requests
import json

from nemo_library.utils.password_manager import PasswordManager

COGNITO_URLS = {
    "demo": "https://cognito-idp.eu-central-1.amazonaws.com/eu-central-1_1ZbUITj21",
    "dev": "https://cognito-idp.eu-central-1.amazonaws.com/eu-central-1_778axETqE",
    "test": "https://cognito-idp.eu-central-1.amazonaws.com/eu-central-1_778axETqE",
    "prod": "https://cognito-idp.eu-central-1.amazonaws.com/eu-central-1_1oayObkcF",
    "challenge": "https://cognito-idp.eu-central-1.amazonaws.com/eu-central-1_U2V9y0lzx",
}
COGNITO_APPCLIENT_IDS = {
    "demo": "7tvfugcnunac7id3ebgns6n66u",
    "dev": "4lr89aas81m844o0admv3pfcrp",
    "test": "4lr89aas81m844o0admv3pfcrp",
    "prod": "8t32vcmmdvmva4qvb79gpfhdn",
    "challenge": "43lq8ej98uuo8hvnoi1g880onp",
}
NEMO_URLS = {
    "demo": "https://demo.enter.nemo-ai.com",
    "dev": "http://development.enter.nemo-ai.com",
    "test": "http://test.enter.nemo-ai.com",
    "prod": "https://enter.nemo-ai.com",
    "challenge": "https://challenge.enter.nemo-ai.com",
}


class Config:

    def __init__(
        self,
        config_file: str = "config.ini",
        environment: str = None,
        tenant: str = None,
        userid: str = None,
        password: str = None,
        hubspot_api_token: str = None,
        migman_local_project_directory: str = None,
        migman_proALPHA_project_status_file: str = None,
        migman_projects: list[str] = None,
        migman_mapping_fields: list[str] = None,
        migman_additional_fields: dict[str, list[str]] = None,
        migman_synonym_fields: dict[str, list[str]] = None,
        migman_multi_projects: dict[str, list[str]] = None,
    ):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

        self.tenant = tenant or self.config.get("nemo_library", "tenant", fallback=None)
        self.userid = userid or self.config.get("nemo_library", "userid", fallback=None)
        self.password = password or self.config.get(
            "nemo_library", "password", fallback=None
        )

        if self.password is None:
            pm = PasswordManager(service_name="nemo_library", username=self.userid)
            self.password = pm.get_password()

        self.environment = environment or self.config.get(
            "nemo_library", "environment", fallback=None
        )
        self.hubspot_api_token = hubspot_api_token or self.config.get(
            "nemo_library", "hubspot_api_token", fallback=None
        )

        self.migman_local_project_directory = (
            migman_local_project_directory
            or self.config.get(
                "nemo_library", "migman_local_project_directory", fallback=None
            )
        )

        self.migman_proALPHA_project_status_file = (
            migman_proALPHA_project_status_file
            or self.config.get(
                "nemo_library", "migman_proALPHA_project_status_file", fallback=None
            )
        )

        self.migman_projects = migman_projects or (
            json.loads(
                self.config.get("nemo_library", "migman_projects", fallback="null")
            )
            if self.config.has_option("nemo_library", "migman_projects")
            else None
        )

        self.migman_mapping_fields = migman_mapping_fields or (
            json.loads(
                self.config.get(
                    "nemo_library", "migman_mapping_fields", fallback="null"
                )
            )
            if self.config.has_option("nemo_library", "migman_mapping_fields")
            else None
        )

        self.migman_additional_fields = migman_additional_fields or (
            json.loads(
                self.config.get(
                    "nemo_library", "migman_additional_fields", fallback="null"
                )
            )
            if self.config.has_option("nemo_library", "migman_additional_fields")
            else None
        )

        self.migman_synonym_fields = migman_synonym_fields or (
            json.loads(
                self.config.get(
                    "nemo_library", "migman_synonym_fields", fallback="null"
                )
            )
            if self.config.has_option("nemo_library", "migman_synonym_fields")
            else None
        )

        self.migman_multi_projects = migman_multi_projects or (
            json.loads(
                self.config.get(
                    "nemo_library", "migman_multi_projects", fallback="null"
                )
            )
            if self.config.has_option("nemo_library", "migman_multi_projects")
            else None
        )

    def get_config_nemo_url(self):
        env = self.get_environment()
        try:
            return NEMO_URLS[env]
        except KeyError:
            raise Exception(f"unknown environment '{env}' provided")

    def get_tenant(self):
        return self.tenant

    def get_userid(self):
        return self.userid

    def get_password(self):
        return self.password

    def get_environment(self):
        return self.environment

    def get_hubspot_api_token(self):
        return self.hubspot_api_token

    def get_migman_local_project_directory(self):
        return self.migman_local_project_directory

    def get_migman_proALPHA_project_status_file(self):
        return self.migman_proALPHA_project_status_file

    def get_migman_projects(self):
        return self.migman_projects

    def get_migman_mapping_fields(self):
        return self.migman_mapping_fields

    def get_migman_additional_fields(self):
        return self.migman_additional_fields

    def get_migman_synonym_fields(self):
        return self.migman_synonym_fields

    def get_migman_multi_projects(self):
        return self.migman_multi_projects

    def connection_get_headers(self):
        tokens = self.connection_get_tokens()
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {tokens[0]}",
            "refresh-token": tokens[2],
            "api-version": "1.0",
        }
        return headers

    def connection_get_cognito_authflow(self):
        return "USER_PASSWORD_AUTH"

    def connection_get_cognito_url(self):
        env = self.get_environment()
        try:
            return COGNITO_URLS[env]
        except KeyError:
            raise Exception(f"unknown environment '{env}' provided")

    def connection_get_cognito_appclientid(self):
        env = self.get_environment()
        try:
            return COGNITO_APPCLIENT_IDS[env]
        except KeyError:
            raise Exception(f"unknown environment '{env}' provided")

    def connection_get_tokens(self):
        headers = {
            "X-Amz-Target": "AWSCognitoIdentityProviderService.InitiateAuth",
            "Content-Type": "application/x-amz-json-1.1",
        }

        authparams = {
            "USERNAME": self.get_userid(),
            "PASSWORD": self.get_password(),
        }

        data = {
            "AuthParameters": authparams,
            "AuthFlow": self.connection_get_cognito_authflow(),
            "ClientId": self.connection_get_cognito_appclientid(),
        }

        # login and get token
        response_auth = requests.post(
            self.connection_get_cognito_url(),
            headers=headers,
            data=json.dumps(data, indent=2),
        )
        if response_auth.status_code != 200:
            raise Exception(
                f"request failed. Status: {response_auth.status_code}, error: {response_auth.text}"
            )
        tokens = json.loads(response_auth.text)
        id_token = tokens["AuthenticationResult"]["IdToken"]
        access_token = tokens["AuthenticationResult"]["AccessToken"]
        refresh_token = tokens["AuthenticationResult"].get(
            "RefreshToken"
        )  # Some flows might not return a RefreshToken

        return id_token, access_token, refresh_token
