from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display
import netaddr


display = Display()

class LookupModule(LookupBase):
    """
    This lookup plugin calculates subnets from a given network prefix.
    Example usage:
        "{{ lookup('calculate_subnets', '192.168.0.0/24', 26) }}"
    """

    def run(self, terms, variables=None, **kwargs):
        # Ensure we have two terms: the network prefix and the subnet size
        if len(terms) != 2:
            raise AnsibleError("The 'validate_subnets' lookup requires two arguments: network and subnet size")

        network = terms[0]
        subnet_size = int(terms[1])

        try:
            # Use netaddr to calculate subnets
            ip_network = netaddr.IPNetwork(network)
            subnets = list(ip_network.subnet(subnet_size))
            return [str(subnet) for subnet in subnets]
        except Exception as e:
            raise AnsibleError(f"Error calculating subnets: {str(e)}")
