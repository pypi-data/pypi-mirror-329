from energy_base.api.permissions.base.roles import BaseRolePermissions


class IsHududGazNaturalgazUser(BaseRolePermissions):
    required_role = 'hududgaz_naturalgaz'
