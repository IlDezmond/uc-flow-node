from uc_flow_nodes.schemas import NodeRunContext
from uc_http_requester.requester import Request


def params_normalize(params):
    return {param: params[param][0][param] for param in params if params[param]}


async def handle_auth(json: NodeRunContext, headers: dict):
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


async def handle_customer(json: NodeRunContext, headers: dict):
    host = json.node.data.properties['host']
    branch = json.node.data.properties['branch']
    id = json.node.data.properties.get('id', None)
    operation = json.node.data.properties['operation']
    token = json.node.data.properties['token']['token']
    headers['X-ALFACRM-TOKEN'] = token

    url = {
        'index': f'https://{host}/v2api/{branch}/customer/index',
        'create': f'https://{host}/v2api/{branch}/customer/create',
        'update': f'https://{host}/v2api/{branch}/customer/update?id={id}',
    }
    params = params_normalize(json.node.data.properties['params'])
    response = await Request(
        url=url[operation],
        method=Request.Method.post,
        headers=headers,
        json=params
    ).execute()
    await json.save_result(
        {
            'result': response.json()
        }
    )
