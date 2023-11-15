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
    name: str = 'Sum_8ea1'
    is_public: bool = False
    displayName: str = 'Sum_8ea1'
    icon: str = '<svg><text x="8" y="50" font-size="50">🤖</text></svg>'
    description: str = 'Sum'
    properties: List[Property] = [
        Property(
            displayName='Переключатель',
            name='switcher',
            type=Property.Type.BOOLEAN,
            required=True,
            default=False,
        ),
        Property(
            displayName='Поле 1',
            name='field_1',
            type=Property.Type.OPTIONS,
            required=True,
            noDataExpression=True,
            options=[
                OptionValue(
                    name='value_1',
                    value='value_1',
                ),
                OptionValue(
                    name='value_2',
                    value='value_2',
                ),
            ],
            displayOptions=DisplayOptions(
                show={
                    'switcher': [True],
                },
            ),
        ),
        Property(
            displayName='Поле 2',
            name='field_2',
            type=Property.Type.OPTIONS,
            required=True,
            noDataExpression=True,
            options=[
                OptionValue(
                    name='value_1',
                    value='value_1',
                ),
                OptionValue(
                    name='value_2',
                    value='value_2',
                ),
            ],
            displayOptions=DisplayOptions(
                show={
                    'switcher': [True],
                },
            ),
        ),
        Property(
            displayName='Почта',
            name='email_field',
            type=Property.Type.EMAIL,
            displayOptions=DisplayOptions(
                show={
                    'switcher': [True],
                    'field_1': ['value_1'],
                    'field_2': ['value_1'],
                },
            ),
        ),
        Property(
            displayName='Дата и время',
            name='datetime_field',
            type=Property.Type.DATETIME,
            displayOptions=DisplayOptions(
                show={
                    'switcher': [True],
                    'field_1': ['value_2'],
                    'field_2': ['value_2'],
                },
            ),
        )
    ]


class InfoView(info.Info):
    class Response(info.Info.Response):
        node_type: NodeType


class ExecuteView(execute.Execute):
    async def post(self, json: NodeRunContext) -> NodeRunContext:
        try:
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
