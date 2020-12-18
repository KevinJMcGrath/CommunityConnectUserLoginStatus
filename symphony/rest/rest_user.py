import symphony.rest.endpoints as sym_ep

from symphony.api_base import APIBase


class User(APIBase):
    def __init__(self, session):
        super().__init__(session)

    def lookup_user_id(self, email: str):
        ep = self.get_endpoint(sym_ep.lookup_user(email))

        user_list = self.get(ep)

        if user_list:
            return user_list['users'][0]['id']
        else:
            return None

    def list_user_groups(self):
        ep = self.get_endpoint(sym_ep.list_user_groups("ROLE_SCOPE"))

        return self.get(ep)
