"""
Main interface for network-firewall service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_network_firewall import (
        Client,
        ListFirewallPoliciesPaginator,
        ListFirewallsPaginator,
        ListRuleGroupsPaginator,
        ListTLSInspectionConfigurationsPaginator,
        ListTagsForResourcePaginator,
        NetworkFirewallClient,
    )

    session = get_session()
    async with session.create_client("network-firewall") as client:
        client: NetworkFirewallClient
        ...


    list_firewall_policies_paginator: ListFirewallPoliciesPaginator = client.get_paginator("list_firewall_policies")
    list_firewalls_paginator: ListFirewallsPaginator = client.get_paginator("list_firewalls")
    list_rule_groups_paginator: ListRuleGroupsPaginator = client.get_paginator("list_rule_groups")
    list_tls_inspection_configurations_paginator: ListTLSInspectionConfigurationsPaginator = client.get_paginator("list_tls_inspection_configurations")
    list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    ```
"""

from .client import NetworkFirewallClient
from .paginator import (
    ListFirewallPoliciesPaginator,
    ListFirewallsPaginator,
    ListRuleGroupsPaginator,
    ListTagsForResourcePaginator,
    ListTLSInspectionConfigurationsPaginator,
)

Client = NetworkFirewallClient


__all__ = (
    "Client",
    "ListFirewallPoliciesPaginator",
    "ListFirewallsPaginator",
    "ListRuleGroupsPaginator",
    "ListTLSInspectionConfigurationsPaginator",
    "ListTagsForResourcePaginator",
    "NetworkFirewallClient",
)
