from .module_imports import key
from uplink import (
    Consumer,
    get as http_get,
    returns,
    headers,
    Query,
)


@headers({"Ocp-Apim-Subscription-Key": key})
class _Warranty_Configurations(Consumer):
    """Inteface to warranty configurations resource for the RockyRoad API."""

    def __init__(self, Resource, *args, **kw):
        self._base_url = Resource._base_url
        super().__init__(base_url=Resource._base_url, *args, **kw)

    @returns.json
    @http_get("warranties/configurations/roles")
    def get_roles_configuration(
        self,
    ):
        """This call will return configuration information for warranty roles."""

    @returns.json
    @http_get("warranties/configurations/claim-process-states")
    def get_claim_process_states(
        self,
    ):
        """This call will return configuration information for claim process states."""

    @returns.json
    @http_get("warranties/configurations/claim-settings")
    def get_claim_settings(
        self,
    ):
        """This call will return configuration information for claim settings."""

    @returns.json
    @http_get("warranties/configurations/claim-process-transitions")
    def get_claim_process_transitions(
        self,
        state: Query = None,
        roles: Query = None,
        claim_level: Query = None,
        is_hub_claim: Query = None,
    ):
        """This call will return configuration information for claim process transitions."""

    @returns.json
    @http_get("warranties/configurations/warranty-role-tests")
    def get_warranty_role_tests(
        self,
        hub_claim_option: Query = None,
        excluded_states: Query = None,
        excluded_claim_levels: Query = None,
        excluded_roles: Query = None,
    ):
        """This call will return configuration information for warranty role tests."""
