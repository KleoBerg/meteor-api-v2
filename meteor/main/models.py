from enum import Enum




# NOTE: This enum is a manual mirror of the UserRole enum defined in the
#       GraphQL schema (`dgraph/schema.graphql`). The GraphQL schema is the
#       single source of truth for all API data types.
#
# TODO: Replace this manual definition with one generated automatically from the GraphQL schema.

class UserRole(Enum):
    ANON = "Anon"
    CONTRIBUTOR = "Contributor"
    REVIEWER = "Reviewer"
    ADMIN = "Admin"

# this enum is for the internal account status predicate of the user type in dgraph (set in the private_predicates.dql)
class AccountStatus(Enum):
    PENDING = "pending"
    ACTIVE = "active"


