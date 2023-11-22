from collections import namedtuple
from uc_flow_schemas.flow import Property

Param = namedtuple('Param', ['displayName', 'name', 'type'])

deal_properties = (
    Param(displayName='Amount', name='amount', type=Property.Type.NUMBER),
    Param(displayName='Deal name', name='dealname', type=Property.Type.STRING),
    Param(displayName='Pipeline', name='pipeline', type=Property.Type.STRING),
    Param(displayName='Close date', name='closedate', type=Property.Type.DATETIME),
    Param(displayName='Deal stage', name='dealstage', type=Property.Type.STRING),
    Param(displayName='Owner', name='hubspot_owner_id', type=Property.Type.NUMBER),
)

contact_properties = (
    Param(displayName='Email', name='email', type=Property.Type.EMAIL),
    Param(displayName='Phone', name='phone', type=Property.Type.STRING),
    Param(displayName='Company', name='company', type=Property.Type.STRING),
    Param(displayName='Website', name='website', type=Property.Type.URL),
    Param(displayName='Last name', name='lastname', type=Property.Type.STRING),
    Param(displayName='First name', name='firstname', type=Property.Type.STRING),
)

association_properties = (
    Param(displayName='From object', name='fromObjectTypeId', type=Property.Type.STRING),
    Param(displayName='To object', name='toObjectTypeId', type=Property.Type.STRING),
    Param(displayName='From object id', name='fromObjectId', type=Property.Type.NUMBER),
    Param(displayName='To object id', name='toObjectId', type=Property.Type.NUMBER),
)
