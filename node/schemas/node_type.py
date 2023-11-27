from typing import List

from uc_flow_schemas import flow
from uc_flow_schemas.flow import DisplayOptions, OptionValue, Property

from node.schemas.properties import association_properties, contact_properties, deal_properties


class NodeType(flow.NodeType):
    id: str = 'de8e3ff2-3aed-470d-b847-d6909a0b95bd'
    type: flow.NodeType.Type = flow.NodeType.Type.action
    name: str = 'Hubspot'
    is_public: bool = False
    displayName: str = 'Hubspot'
    icon: str = '<svg><text x="8" y="50" font-size="50">🤖</text></svg>'
    description: str = 'Hubspot'
    properties: List[Property] = [
        Property(
            displayName='Object',
            name='object',
            type=Property.Type.OPTIONS,
            required=True,
            noDataExpression=True,
            options=[
                OptionValue(
                    name='Contact',
                    value='contacts',
                ),
                OptionValue(
                    name='Deal',
                    value='deals',
                ),
                OptionValue(
                    name='Association',
                    value='association',
                )
            ],
        ),
        Property(
            displayName='Api token',
            name='token',
            type=Property.Type.STRING,
            required=True,
        ),
        Property(
            displayName='Method',
            name='method',
            type=Property.Type.OPTIONS,
            displayOptions=DisplayOptions(
                show={
                    'object': ['contacts', 'deals'],
                },
            ),
            options=[
                OptionValue(
                    name='List',
                    value='list',
                ),
                OptionValue(
                    name='Get',
                    value='get',
                ),
                OptionValue(
                    name='Create',
                    value='create',
                ),
                OptionValue(
                    name='Update',
                    value='update',
                ),
                OptionValue(
                    name='Delete',
                    value='delete',
                ),
            ],
        ),
        # Filter properties
        Property(
            displayName='Limit',
            name='limit',
            type=Property.Type.NUMBER,
            displayOptions=DisplayOptions(
                show={
                    'object': ['contacts', 'deals'],
                    'method': ['list'],
                },
            ),
        ),
        Property(
            displayName='After',
            name='after',
            type=Property.Type.NUMBER,
            displayOptions=DisplayOptions(
                show={
                    'object': ['contacts', 'deals'],
                    'method': ['list'],
                },
            ),
        ),
        Property(
            displayName='Object id',
            name='object_id',
            type=Property.Type.NUMBER,
            displayOptions=DisplayOptions(
                show={
                    'object': ['contacts', 'deals'],
                    'method': ['get', 'delete', 'update'],
                }
            )
        ),
        # Deal properties
        Property(
            displayName='Deal properties',
            name='deal_properties',
            type=Property.Type.COLLECTION,
            default={},
            placeholder='Add',
            displayOptions=DisplayOptions(
                show={
                    'object': ['deals'],
                    'method': ['create', 'update'],
                }
            ),
            options=[
                Property(
                    displayName=param.displayName,
                    name=param.name,
                    type=param.type,
                    default='',
                    description='temp_desc'
                )
                for param in deal_properties
            ]
        ),
        # Contact properties
        Property(
            displayName='Contact properties',
            name='contact_properties',
            type=Property.Type.COLLECTION,
            default={},
            placeholder='Add',
            displayOptions=DisplayOptions(
                show={
                    'object': ['contacts'],
                    'method': ['create', 'update'],
                }
            ),
            options=[
                Property(
                    displayName=param.displayName,
                    name=param.name,
                    type=param.type,
                    default='',
                    description='temp_desc'
                )
                for param in contact_properties
            ]
        ),
        # Association properties
        Property(
            displayName='Association category',
            name='association_category',
            type=Property.Type.OPTIONS,
            default={},
            displayOptions=DisplayOptions(
                show={
                    'object': ['association'],
                }
            ),
            options=[
                OptionValue(
                    name='HUBSPOT_DEFINED',
                    value='HUBSPOT_DEFINED',
                ),
                OptionValue(
                    name='USER_DEFINED',
                    value='USER_DEFINED',
                ),
                OptionValue(
                    name='INTEGRATOR_DEFINED',
                    value='INTEGRATOR_DEFINED',
                ),
            ],
        ),
        Property(
            displayName='Association type id',
            name='association_type_id',
            type=Property.Type.NUMBER,
            displayOptions=DisplayOptions(
                show={
                    'object': ['association'],
                }
            ),
        ),
        Property(
            displayName='Association properties',
            name='association_properties',
            type=Property.Type.COLLECTION,
            default={},
            placeholder='Add',
            displayOptions=DisplayOptions(
                show={
                    'object': ['association'],
                }
            ),
            options=[
                Property(
                    displayName=param.displayName,
                    name=param.name,
                    type=param.type,
                    default='',
                    description='temp_desc'
                )
                for param in association_properties
            ]
        ),
    ]
