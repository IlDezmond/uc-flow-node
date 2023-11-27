from datetime import datetime, timezone

from uc_flow_nodes.schemas import NodeRunContext
from uc_http_requester.requester import Request, Response


def date_fix(date_string):
    date_format = "%Y-%m-%dT%H:%M"

    date_object = datetime.strptime(date_string, date_format)
    date_object = date_object.replace(tzinfo=timezone.utc)
    formatted_date = date_object.isoformat(timespec='milliseconds')
    return formatted_date


def params_normalize(params, properties_flag=True):
    properties = {param: params[param][0][param] for param in params if params[param]}
    if properties.get('closedate', None):
        properties['closedate'] = date_fix(properties['closedate'])

    if properties_flag:
        return {'properties': properties}
    else:
        return properties


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
            method=Request.Method.patch,
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
    try:
        await json.save_result({'result': response.json()})
    except Exception:
        await json.save_result({'result': f'status code: {response.status_code}'})


async def handle_association(json: NodeRunContext, token):
    headers = {
        'authorization': f'Bearer {token}',
    }
    properties = params_normalize(json.node.data.properties['association_properties'], False)
    from_object_type_id = properties['fromObjectTypeId']
    to_object_type_id = properties['toObjectTypeId']
    from_object_id = properties['fromObjectId']
    to_object_id = properties['toObjectId']

    url = (f'https://api.hubapi.com/crm/v4/objects/{from_object_type_id}/'
           f'{from_object_id}/associations/default/{to_object_type_id}/{to_object_id}')
    response = await Request(
        url=url,
        method=Request.Method.put,
        headers=headers,
    ).execute()

    await json.save_result({'result': response.json()})
