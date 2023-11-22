from uc_flow_nodes.schemas import NodeRunContext
from uc_http_requester.requester import Request, Response


def params_normalize(params):
    return {param: params[param][0][param] for param in params if params[param]}


class CRUD:
    def __init__(self, token: str, object_type: str):
        self.object_type = object_type
        self.headers = {'authorization': f'Bearer {token}'}

    async def get(self, object_id: int) -> Response:
        url = f'https://api.hubapi.com/crm/v3/objects/{self.object_type}/{object_id}'
        response = await Request(
            url=url,
            method=Request.Method.get,
            headers=self.headers
        ).execute()
        return response

    async def list(self, limit: int, after: int) -> Response:
        url = f'https://api.hubapi.com/crm/v3/objects/{self.object_type}'
        if limit:
            url += f'?limit={limit}'
        if after:
            url += f'&after={after}'
        response = await Request(
            url=url,
            method=Request.Method.get,
            headers=self.headers
        ).execute()
        return response

    async def create(self, properties) -> Response:
        url = f'https://api.hubapi.com/crm/v3/objects/{self.object_type}'
        self.headers['Content-Type'] = 'application/json'
        response = await Request(
            url=url,
            method=Request.Method.post,
            headers=self.headers,
            json=properties
        ).execute()
        return response

    async def update(self, object_id: int, properties) -> Response:
        url = f'https://api.hubapi.com/crm/v3/objects/{self.object_type}/{object_id}'
        self.headers['Content-Type'] = 'application/json'
        response = await Request(
            url=url,
            method=Request.Method.put,
            headers=self.headers,
            json=properties
        ).execute()
        return response

    async def delete(self, object_id: int) -> Response:
        url = f'https://api.hubapi.com/crm/v3/objects/{self.object_type}/{object_id}'
        response = await Request(
            url=url,
            method=Request.Method.delete,
            headers=self.headers,
        ).execute()
        return response


async def handle_object(json: NodeRunContext, token, method, object_type):
    object_crud = CRUD(token=token, object_type=object_type)
    if object_type == 'contacts':
        object_properties = 'contact_properties'
    elif object_type == 'deals':
        object_properties = 'deal_properties'
    else:
        raise Exception(f'Unknown object type {object_type}')

    match method:
        case 'create':
            properties = params_normalize(json.node.data.properties[object_properties])
            response: Response = await object_crud.create(properties)
        case 'update':
            object_id = json.node.data.properties['object_id']
            properties = params_normalize(json.node.data.properties[object_properties])
            response: Response = await object_crud.update(object_id, properties)
        case 'delete':
            object_id = json.node.data.properties['object_id']
            response: Response = await object_crud.delete(object_id)
        case 'list':
            limit = json.node.data.properties.get('limit', None)
            after = json.node.data.properties.get('after', None)
            response: Response = await object_crud.list(limit, after)
        case 'get':
            object_id = json.node.data.properties['object_id']
            response: Response = await object_crud.get(object_id)
        case _:
            raise Exception(f'Unknown method {method}')

    await json.save_result({'result': response.json()})


async def handle_association(json: NodeRunContext, token):
    headers = {
        'authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    from_object_type_id = json.node.data.properties['fromObjectTypeId']
    to_object_type_id = json.node.data.properties['toObjectTypeId']
    from_object_id = json.node.data.properties['fromObjectId']
    to_object_id = json.node.data.properties['toObjectId']

    url = (f'https://api.hubapi.com/crm/v4/objects/{from_object_type_id}/'
           f'{from_object_id}/associations/{to_object_type_id}/{to_object_id}')
    data = {
        'associationCategory': json.node.data.properties['associationCategory'],
        'associationTypeId': json.node.data.properties['associationTypeId'],
    }
    response = await Request(
        url=url,
        method=Request.Method.put,
        headers=headers,
        json=data
    ).execute()

    await json.save_result({'result': response.json()})
