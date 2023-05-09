import os
from types import MappingProxyType

# RBAC CONFIGURATION
x_tenant_id = os.getenv('X_TENANT_ID', 'frinx')
x_from = os.getenv('X_FROM', 'fm-base-workers')
x_auth_user_group = os.getenv('X_AUTH_USER_GROUP', 'network-admin')

# SET SERVICES URL VARIABLES
uniconfig_url_base = os.getenv('UNICONFIG_URL_BASE', 'http://uniconfig:8181/rests')
elastic_url_base = os.getenv('ELASTICSEACRH_URL_BASE', 'http://elasticsearch:9200')
conductor_url_base = os.getenv('CONDUCTOR_URL_BASE', 'http://workflow-proxy:8088/proxy/api')
inventory_url_base = os.getenv('INVENTORY_URL_BASE', 'http://inventory:8000/graphql')
influxdb_url_base = os.getenv('INFLUXDB_URL_BASE', 'http://influxdb:8086')
resource_manager_url_base = os.getenv('RESOURCE_MANAGER_URL_BASE', 'http://resource-manager:8884/query')

# URL HEADERS
uniconfig_headers = MappingProxyType({'Content-Type': 'application/json'})
conductor_headers = MappingProxyType(
    {
        'Content-Type': 'application/json',
        'x-tenant-id': x_tenant_id,
        'from': x_from,
        'x-auth-user-groups': x_auth_user_group
    }
)
additional_uniconfig_request_params = MappingProxyType(
    {
        'verify': False,
        'headers': uniconfig_headers
    }
)
