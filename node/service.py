import ujson
from typing import List, Tuple

from uc_flow_nodes.schemas import NodeRunContext
from uc_flow_nodes.service import NodeService
from uc_flow_nodes.views import info, execute
from uc_flow_schemas import flow
from uc_flow_schemas.flow import Property, CredentialProtocol, RunState
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
            displayName='Текстовое поле',
            name='text_field',
            type=Property.Type.STRING,
            placeholder='Text placeholder',
            description='Text description',
            required=True,
            default='Text data',
        ),
        Property(
            displayName='Числовое поле',
            name='integer_field',
            type=Property.Type.NUMBER,
            placeholder='Int placeholder',
            description='Int description',
            required=True,
            default=0,
        ),
        Property(
            displayName='Переключатель',
            name='switcher',
            type=Property.Type.BOOLEAN,
            description='Число / Текст',
            required=True,
            default=False,
        )
    ]


class InfoView(info.Info):
    class Response(info.Info.Response):
        node_type: NodeType


class ExecuteView(execute.Execute):
    async def post(self, json: NodeRunContext) -> NodeRunContext:
        try:
            try:
                num1 = int(json.node.data.properties['text_field'])
            except ValueError:
                raise ValueError('В текстовом поле должно быть числовое значение')

            num2 = json.node.data.properties['integer_field']
            result = num1 + num2
            if json.node.data.properties['switcher']:
                result = str(result)
            await json.save_result({
                "result": result
            })
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
