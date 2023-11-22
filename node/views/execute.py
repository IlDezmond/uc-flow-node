from uc_flow_nodes.schemas import NodeRunContext
from uc_flow_nodes.views import execute
from uc_flow_schemas.flow import RunState

from node.views.execute_handlers import handle_association, handle_object


class ExecuteView(execute.Execute):
    async def post(self, json: NodeRunContext) -> NodeRunContext:
        try:
            hub_object = json.node.data.properties['object']
            token = json.node.data.properties['token']

            if hub_object == 'contacts':
                method = json.node.data.properties['method']
                await handle_object(json, token, method, hub_object)
            elif hub_object == 'deals':
                method = json.node.data.properties['method']
                await handle_object(json, token, method, hub_object)
            elif hub_object == 'association':
                await handle_association(json, token)

            json.state = RunState.complete
        except Exception as e:
            self.log.warning(f'Error {e}')
            await json.save_error(str(e))
            json.state = RunState.error
        return json
