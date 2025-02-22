import sys
import typer
from prettytable import PrettyTable

from arlas.cli.service import Service
from arlas.cli.settings import Configuration
from arlas.cli.variables import variables

org = typer.Typer()


@org.command(help="List organisations", name="list", epilog=variables["help_epilog"])
def list_organisations():
    config = variables["arlas"]
    organisations = Service.list_organisations(config)
    print(organisations)
    tab = PrettyTable(organisations[0], sortby="name", align="l")
    tab.add_rows(organisations[1:])
    print(tab)


@org.command(help="Create organisation with the given name", name="add", epilog=variables["help_epilog"])
def create_organisation(organisation: str = typer.Argument(default="", help="Organisation's name")):
    config = variables["arlas"]
    if organisation:
        print(Service.create_organisation(config, organisation).get("id"))
    else:
        print(Service.create_organisation_from_user_domain(config).get("id"))


@org.command(help="Delete the organisation", name="delete", epilog=variables["help_epilog"])
def delete_organisation(org_id: str = typer.Argument(help="Organisation's identifier")):
    config = variables["arlas"]
    print(Service.delete_organisation(config, org_id).get("message"))


@org.command(help="List the collections of the organisation", name="collections", epilog=variables["help_epilog"])
def collections(org_id: str = typer.Argument(help="Organisation's identifier")):
    config = variables["arlas"]
    organisations = Service.list_organisation_collections(config, org_id)
    tab = PrettyTable(["collection"], sortby="collection", align="l")
    for org in organisations:
        tab.add_row([org])
    print(tab)


@org.command(help="List the users of the organisation", name="users", epilog=variables["help_epilog"])
def users(org_id: str = typer.Argument(help="Organisation's identifier")):
    config = variables["arlas"]
    users = Service.list_organisation_users(config, org_id)
    tab = PrettyTable(["id", "email", "is owner", "groups"], sortby="email", align="l")
    tab.add_rows(users)
    print(tab)


@org.command(help="Add a user to the organisation, and optionally within groups", name="add_user",
             epilog=variables["help_epilog"])
def add_user(org_id: str = typer.Argument(help="Organisation's identifier"),
             email: str = typer.Argument(help="User's email"),
             group: list[str] = typer.Option([], help="Group identifier")):
    config = variables["arlas"]
    print(Service.add_user_in_organisation(config, org_id, email, group))


@org.command(help="Remove the user from the organisation", name="delete_user", epilog=variables["help_epilog"])
def delete_user(org_id: str = typer.Argument(help="Organisation's identifier"),
                user_id: str = typer.Argument(help="User ID")):
    config = variables["arlas"]
    Service.delete_user_in_organisation(config, org_id, user_id)


@org.command(help="List the groups of the organisation", name="groups", epilog=variables["help_epilog"])
def groups(org_id: str = typer.Argument(help="Organisation's identifier")):
    config = variables["arlas"]
    tab = PrettyTable(["id", "name", "description", "is technical", "type"], sortby="name", align="l")
    groups = Service.list_organisation_groups(config, org_id)
    tab.add_rows(groups)
    roles = Service.list_organisation_roles(config, org_id)
    tab.add_rows(roles)
    print(tab)


@org.command(help="List the permissions of the organisation", name="permissions", epilog=variables["help_epilog"])
def permissions(org_id: str = typer.Argument(help="Organisation's identifier")):
    config = variables["arlas"]
    groups = Service.list_organisation_permissions(config, org_id)
    tab = PrettyTable(["id", "name", "value", "groups"], sortby="name", align="l")
    tab.add_rows(groups)
    print(tab)


@org.command(help="Add a group to the organisation", name="add_group", epilog=variables["help_epilog"])
def add_group(org_id: str = typer.Argument(help="Organisation's identifier"),
              name: str = typer.Argument(help="Group name"),
              description: str = typer.Argument(help="Group description")):
    config = variables["arlas"]
    print(Service.add_group_in_organisation(config, org_id, name, description).get("id"))


@org.command(help="Remove the group from the organisation", name="delete_group", epilog=variables["help_epilog"])
def delete_group(org_id: str = typer.Argument(help="Organisation's identifier"),
                 id: str = typer.Argument(help="Group ID")):
    config = variables["arlas"]
    print(Service.delete_group_in_organisation(config, org_id, id).get("message"))


@org.command(help="Add a permission to the organisation", name="add_permission", epilog=variables["help_epilog"])
def add_permission(org_id: str = typer.Argument(help="Organisation's identifier"),
                   value: str = typer.Argument(help="Permission value"),
                   description: str = typer.Argument(help="Permission description")):
    config = variables["arlas"]
    print(Service.add_permission_in_organisation(config, org_id, value, description).get("id"))


@org.command(help="Remove the permission from the organisation", name="delete_permission",
             epilog=variables["help_epilog"])
def delete_permission(org_id: str = typer.Argument(help="Organisation's identifier"),
                      id: str = typer.Argument(help="Permission ID")):
    config = variables["arlas"]
    print(Service.delete_permission_in_organisation(config, org_id, id).get("message"))


@org.command(help="Add a permission to a group within the organisation", name="add_permission_to_group",
             epilog=variables["help_epilog"])
def add_permission_to_group(org_id: str = typer.Argument(help="Organisation's identifier"),
                            group_id: str = typer.Argument(help="Group identifier"),
                            permission_id: str = typer.Argument(help="Permission identifier")):
    config = variables["arlas"]
    print(Service.add_permission_to_group_in_organisation(config, org_id, group_id, permission_id))


@org.command(help="Remove a permission to a group within the organisation", name="delete_permission_from_group",
             epilog=variables["help_epilog"])
def delete_permission_from_group(organisation: str = typer.Argument(help="Organisation's identifier"),
                                 group_id: str = typer.Argument(help="Group identifier"),
                                 permission_id: str = typer.Argument(help="Permission identifier")):
    config = variables["arlas"]
    print(Service.delete_permission_from_group_in_organisation(config, organisation, group_id, permission_id))


@org.command(help="Add a user to a group within the organisation", name="add_user_to_group",
             epilog=variables["help_epilog"])
def add_user_to_group(org_id: str = typer.Argument(help="Organisation's identifier"),
                      user_id: str = typer.Argument(help="User identifier"),
                      group_id: str = typer.Argument(help="Group identifier")):
    config = variables["arlas"]
    print(Service.add_user_to_organisation_group(config, org_id, user_id, group_id))


@org.command(help="Remove a user from a group within the organisation", name="remove_user_from_group", epilog=variables["help_epilog"])
def remove_user_from_group(org_id: str = typer.Argument(help="Organisation's identifier"),
                           user_id: str = typer.Argument(help="User identifier"),
                           group_id: str = typer.Argument(help="Group identifier")):
    config = variables["arlas"]
    print(Service.remove_user_from_organisation_group(config, org_id, user_id, group_id))


@org.command(help="Add and return an new API Key with permissions associated to provided groups. Use the key id and key secret with the arlas-api-key-id and arlas-api-key-secret headers.", name="add-apikey",
             epilog=variables["help_epilog"])
def add_apikey(org_id: str = typer.Argument(help="Organisation's identifier"),
               name: str = typer.Argument(help="API Key name"),
               user_id: str = typer.Option(help="User identifier", default=None),
               ttlInDays: int = typer.Option(help="Time To Live in days", default=365),
               gids: list[str] = typer.Option(help="Group identifiers. If not provided, all groups of the user are used.", default=None)
               ):
    config = variables["arlas"]
    if not gids or len(gids) == 0:
        gids = list(map(lambda arr: arr[0], Service.list_organisation_groups(config, org_id) + Service.list_organisation_roles(config, org_id)))
    print(Service.create_api_key(config, org_id, name, ttlInDays, __solve_user_id__(config, org_id, user_id), gids))


@org.command(help="Delete an API Key", name="delete-apikey",
             epilog=variables["help_epilog"])
def delete_apikey(org_id: str = typer.Argument(help="Organisation's identifier"),
                  key_id: str = typer.Argument(help="API Key identifier"),
                  user_id: str = typer.Option(help="User identifier", default=None),
                  ):
    config = variables["arlas"]
    print(Service.delete_api_key(config, org_id, __solve_user_id__(config, org_id, user_id), key_id))


def __solve_user_id__(config: str, org_id: str, user_id: str):
    if not user_id:
        c = Configuration.settings.arlas.get(config)
        if c and c.authorization and c.authorization.token_url and c.authorization.token_url.login:
            user_id = Service.get_user_from_organisation(config, org_id, c.authorization.token_url.login)[0]
            if not user_id:
                print("Error : user id not found for {}.".format(config), file=sys.stderr)
                sys.exit(1)
        else:
            print("Error : no login found for {}.".format(config), file=sys.stderr)
            sys.exit(1)
    return user_id


@org.command(help="Check if user's organisation exists", name="check",
             epilog=variables["help_epilog"])
def check():
    config = variables["arlas"]
    print(Service.check_organisation(config))


@org.command(help="List forbidden organisations.", name="forbidden",
             epilog=variables["help_epilog"])
def forbidden():
    config = variables["arlas"]
    print(Service.forbidden_organisations(config))


@org.command(help="Forbid an organisation name.", name="forbid",
             epilog=variables["help_epilog"])
def forbid(name: str = typer.Argument(help="Name of the organisation to forbid")):
    config = variables["arlas"]
    print(Service.forbid_organisation(config, name))


@org.command(help="Remove an organisation name from the forbidden list.", name="authorize",
             epilog=variables["help_epilog"])
def authorize(name: str = typer.Argument(help="Name of the organisation to authorize")):
    config = variables["arlas"]
    print(Service.authorize_organisation(config, name))
