from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase
import netaddr

class LookupModule(LookupBase):
    """
    This lookup plugin calculates subnets from a given network prefix.
    Example usage:
        "{{ lookup('calculate_subnets', '192.168.0.0/24', 26) }}"
    """
    def run(self, terms, variables=None, **kwargs):
        network = terms[0]
        subnet_size = int(terms[1])
        try:
            ip_network = netaddr.IPNetwork(network)
            subnets = list(ip_network.subnet(subnet_size))
            return [str(subnet) for subnet in subnets]
        except Exception as e:
            raise AnsibleError(f"Error calculating subnets: {str(e)}")
