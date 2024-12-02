"""A custom Ansible filter."""

class FilterModule(object):
    """ACL State Filter."""

    def filters(self):
        """Default filters method to overload"""
        return {"acl_state": self.acl_state}

    def acl_state(self,acl_def):
        """ACL State filter logic."""
        for acl_name, acl_rules in acl_def.items():
            for rule in acl_rules:
                rule["state"] = rule["state"].upper()
        return acl_def
