import ujson
from typing import List, Tuple

from uc_flow_nodes.schemas import NodeRunContext
from uc_flow_nodes.service import NodeService
from uc_flow_nodes.views import info, execute
from uc_flow_schemas import flow
from uc_flow_schemas.flow import Property, CredentialProtocol, RunState, OptionValue, DisplayOptions
from uc_http_requester.requester import Request


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
            displayName='Адрес CRM',
            name='host',
            type=Property.Type.STRING,
            default='uiscom.s20.online',
            displayOptions=DisplayOptions(
                show={
                    'action': ['authentication'],
                },
            ),
        ),
        Property(
            displayName='Email',
            name='email',
            type=Property.Type.EMAIL,
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
            displayOptions=DisplayOptions(
                show={
                    'action': ['authentication'],
                }
            )
        ),
        # Customer properties
        Property(
            displayName='ID филиала',
            name='branch',
            type=Property.Type.NUMBER,
            default=1,
            displayOptions=DisplayOptions(
                show={
                    'action': ['customer'],
                },
            ),
        ),

    ]


class InfoView(info.Info):
    class Response(info.Info.Response):
        node_type: NodeType


class ExecuteView(execute.Execute):
    async def post(self, json: NodeRunContext) -> NodeRunContext:
        try:
            action = json.node.data.properties['action']
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
            if action == 'authentication':
                host = json.node.data.properties['host']
                data = {
                    'email': json.node.data.properties['email'],
                    'api_key': json.node.data.properties['api_key'],
                }
                url = f'https://{host}/v2api/auth/login'
                response = await Request(
                    url=url,
                    method=Request.Method.post,
                    headers=headers,
                    json=data
                ).execute()
                token = response.json()['token']
                await json.save_result(
                    {
                        'token': token
                    }
                )
            elif action == 'customer':
                pass
            json.state = RunState.complete
        except Exception as e:
            self.log.warning(f'Error {e}')
            await json.save_error(str(e))
            json.state = RunState.error
        return json


class Service(NodeService):
    class Routes(NodeService.Routes):
        Info = InfoView
        Execute = ExecuteView
