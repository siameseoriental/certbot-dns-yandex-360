import time
import requests
import logging
import configparser
from acme import challenges
from certbot import interfaces
from certbot.plugins import common

# Set up basic logging
logger = logging.getLogger(__name__)

class Yandex360DNSAuthenticator(common.Plugin, interfaces.Authenticator):
    description = "Create or update DNS records via API 360"

    # Initializer method to set up the plugin
    def __init__(self, *args, **kwargs):
        super(Yandex360DNSAuthenticator, self).__init__(*args, **kwargs)
        # Load configuration from the .ini file
        self.config = self._load_config()
        # API endpoint and token are loaded from the configuration file
        self.api_endpoint = self.config.get('api_endpoint', 'https://api360.yandex.net/directory/v1/org/orgId/domains/domain/dns')
        self.api_token = self.config.get('api_token', 'default_token_here')

    # More information about the plugin
    def more_info(self):
        return "This plugin creates or updates _acme-challenge DNS record using Yandex API 360."

    # Preparation phase for the plugin, currently unused
    def prepare(self):
        pass

    # Perform method where DNS challenges are handled
    def perform(self, achalls):
        responses = []
        # Process each ACME challenge provided by Certbot
        for achall in achalls:
            domain = achall.domain
            validation = achall.validation(achall.account_key)
            logger.info(f"Expected DNS _acme-challenge for {domain} value is {validation}.")

            # Check if the DNS record already exists
            record_id = self._check_dns_record("_acme-challenge." + domain)

            if not record_id:
                # If not, create a new DNS record
                logger.info(f"Creating DNS record _acme-challenge for {domain}.")
                record_id = self._create_dns_record("_acme-challenge", validation)
                record_created = True
            else:
                record_created = False

            # Update the DNS record if it already exists
            if record_id and not record_created:
                logger.info(f"Updating DNS record _acme-challenge for {domain}.")
                self._update_dns_record(record_id, "_acme-challenge", validation)

            # Append the response from the ACME challenge and wait for DNS propagation
            responses.append(achall.response(achall.account_key))
            logger.info(f"Please wait 20 minutes for DNS propagation.")
            time.sleep(1200)  # Sleep for 20 minutes
        return responses

    # Cleanup method, currently unused
    def cleanup(self, achalls):
        pass

    # Load configuration from the .ini file
    def _load_config(self):
        config_parser = configparser.ConfigParser()
        config_file = './config.ini'
        config_parser.read(config_file)
        return {'api_endpoint': config_parser.get('API', 'endpoint'),
                'api_token': config_parser.get('API', 'token')}

    # Check if the _acme-challenge DNS record already exists
    def _check_dns_record(self, name):
        url = f"{self.api_endpoint}?page=1&perPage=100"
        headers = {'Authorization': f'OAuth {self.api_token}', 'Content-Type': 'application/json'}
        response = requests.get(url, headers=headers)
        records = response.json().get('records', [])
        for record in records:
            if record['name'] == "_acme-challenge" and record['type'] == 'TXT':
                return record['recordId']
        return None

    # Create a new _acme-challenge DNS record
    def _create_dns_record(self, name, validation):
        url = self.api_endpoint
        headers = {'Authorization': f'OAuth {self.api_token}', 'Content-Type': 'application/json'}
        data = {'name': name, 'text': validation, 'ttl': 600, 'type': 'TXT'}
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json().get('recordId')
        else:
            logger.error(f"Failed to create DNS record: {response.status_code} {response.text}")
            return None

    # Update an existing _acme-challenge DNS record
    def _update_dns_record(self, record_id, name, validation):
        url = f"{self.api_endpoint}/{record_id}"
        headers = {'Authorization': f'OAuth {self.api_token}', 'Content-Type': 'application/json'}
        data = {'name': name, 'text': validation, 'ttl': 600, 'type': 'TXT'}
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()

    # Method to define additional parser arguments for the plugin
    @classmethod
    def add_parser_arguments(cls, add):
        add('api-endpoint', help='API endpoint for Yandex DNS service')

    # Method to return the preferred challenge type
    def get_chall_pref(self, domain):
        return [challenges.DNS01]