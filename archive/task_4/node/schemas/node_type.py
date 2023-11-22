from typing import List

from uc_flow_schemas import flow
from uc_flow_schemas.flow import DisplayOptions, OptionValue, Property

from node.schemas.properties import params


class NodeType(flow.NodeType):
    id: str = '8ea154e3-af9b-491d-837c-1c0058369536'
    type: flow.NodeType.Type = flow.NodeType.Type.action
    name: str = 'AlfaCRM_8ea1'
    is_public: bool = False
    displayName: str = 'AlfaCRM_8ea1'
    icon: str = '<svg><text x="8" y="50" font-size="50">🤖</text></svg>'
    description: str = 'AlfaCRM'
    properties: List[Property] = [
        Property(
            displayName='Action',
            name='action',
            type=Property.Type.OPTIONS,
            required=True,
            noDataExpression=True,
            options=[
                OptionValue(
                    name='authentication',
                    value='authentication',
                ),
                OptionValue(
                    name='customer',
                    value='customer',
                ),
            ],
        ),
        # Auth properties
        Property(
            displayName='CRM host',
            name='host',
            type=Property.Type.STRING,
            default='uiscom.s20.online',
            displayOptions=DisplayOptions(
                show={
                    'action': ['authentication', 'customer'],
                },
            ),
        ),
        Property(
            displayName='Email',
            name='email',
            type=Property.Type.EMAIL,
            default='vehemop789@weirby.com',
            displayOptions=DisplayOptions(
                show={
                    'action': ['authentication'],
                },
            ),
        ),
        Property(
            displayName='API key',
            name='api_key',
            type=Property.Type.STRING,
            default='7acaf091-77b5-11ee-8640-3cecef7ebd64',
            displayOptions=DisplayOptions(
                show={
                    'action': ['authentication'],
                }
            )
        ),
        # Customer properties
        Property(
          displayName='Token',
          name='token',
          type=Property.Type.JSON,
          displayOptions=DisplayOptions(
              show={
                  'action': ['customer'],
              }
          )
        ),
        Property(
            displayName='Branch',
            name='branch',
            type=Property.Type.NUMBER,
            default=1,
            displayOptions=DisplayOptions(
                show={
                    'action': ['customer'],
                },
            ),
        ),
        Property(
            displayName='Operation',
            name='operation',
            type=Property.Type.OPTIONS,
            noDataExpression=True,
            displayOptions=DisplayOptions(
                show={
                    'action': ['customer'],
                },
            ),
            options=[
                OptionValue(
                    name='index',
                    value='index',
                ),
                OptionValue(
                    name='create',
                    value='create',
                ),
                OptionValue(
                    name='update',
                    value='update',
                )
            ]
        ),
        Property(
            displayName='Parameters',
            name='params',
            type=Property.Type.COLLECTION,
            placeholder='Add',
            default={},
            displayOptions=DisplayOptions(
                show={
                    'action': ['customer'],
                }
            ),
            options=[
                Property(
                    displayName=param.displayName,
                    name=param.name,
                    type=param.type,
                    description=param.description,
                    default='',
                )
                for param in params
            ]
        )
    ]
