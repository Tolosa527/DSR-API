############## RESPONSE MESSAGES ###############

messages = {
    "dsr_detail_success": "DSR found in JSON format",
    "not found": "DSR does not exist",
    "dsr_list_success": "An array of DSR in JSON format",
    "failed": "FAILED",
    "resources_found": "List of resources in JSON format ordered by revenue in EURO",
}

############# DEFAULT VARIABLES ################


TERRITORY_DEFAULT_NAME = "Spain"
TERRITORY_DEFAULT_CODE = "ES"
CURRENCY_DEFAULT_NAME = "Euro"
CURRENCY_DEFAULT_CODE = "EUR"


STATUS_ALL = (
    ("failed", "FAILED"),
    ("ingested", "INGESTED"),
)

DEFAULT_PATH = "/path/to/dsr.tsv"
