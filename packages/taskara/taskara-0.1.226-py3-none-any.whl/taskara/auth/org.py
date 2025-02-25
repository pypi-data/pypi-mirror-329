import os
from typing import List, Optional

from agentcore.models import V1UserProfile
from clerk_backend_api import Clerk


def get_org_slug(name: str) -> Optional[str]:
    with Clerk(bearer_auth=os.getenv("CLERK_API_KEY")) as clerk:
        # Query organizations with the given name
        orgs = clerk.organizations.list(query=name)

        if not orgs:
            return None

        # Find exact name match and return its ID
        for org in orgs.data:
            if org.name == name:
                return org.slug

    return None


def get_user_email(handle: str) -> Optional[str]:
    with Clerk(bearer_auth=os.getenv("CLERK_API_KEY")) as clerk:
        # Query users with the given handle
        users = clerk.users.list(query=handle)

        if not users:
            return None

        # Find exact handle match and return primary email
        for user in users:
            if user.username == handle:
                # Get primary email address
                primary_email = next(
                    (
                        email.email_address
                        for email in user.email_addresses
                        if email.id == user.primary_email_address_id
                    ),
                    None,
                )
                return primary_email

    return None


def get_org_names(user: V1UserProfile) -> List[str]:
    org_names = []
    if user.organizations:
        for _, info in user.organizations.items():
            if info["org_name"]:
                org_names.append(info["org_name"])
    return org_names
