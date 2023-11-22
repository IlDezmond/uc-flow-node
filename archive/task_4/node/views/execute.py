from uc_flow_nodes.schemas import NodeRunContext
from uc_flow_nodes.views import execute
from uc_flow_schemas.flow import RunState

from node.views.execute_handlers import handle_auth, handle_customer


class ExecuteView(execute.Execute):
    async def post(self, json: NodeRunContext) -> NodeRunContext:
        try:
            action = json.node.data.properties['action']
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
            if action == 'authentication':
                await handle_auth(json, headers)
            elif action == 'customer':
                await handle_customer(json, headers)
            json.state = RunState.complete
        except Exception as e:
            self.log.warning(f'Error {e}')
            await json.save_error(str(e))
            json.state = RunState.error
        return json
