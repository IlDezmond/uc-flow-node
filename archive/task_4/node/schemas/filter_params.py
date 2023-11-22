from collections import namedtuple
from uc_flow_schemas.flow import Property

Param = namedtuple('Param', ['displayName', 'name', 'type', 'description'])

params = [
    Param('id', 'id', Property.Type.NUMBER, 'Идентификатор'),
    Param('page', 'page', Property.Type.NUMBER, 'Страница'),
    Param('name', 'name', Property.Type.STRING, 'Полное имя'),
    Param('is_study', 'is_study', Property.Type.BOOLEAN, 'Флаг обучения'),
    Param('company_id', 'company_id', Property.Type.NUMBER, 'Компания'),
    Param('dob_from', 'dob_from', Property.Type.DATE, 'Дата рождения от'),
    Param('dob_to', 'dob_to', Property.Type.DATE, 'Дата рождения до'),
    Param('balance_contract_from', 'balance_contract_from', Property.Type.NUMBER, 'Баланс договора от'),
    Param('phone', 'phone', Property.Type.STRING, 'Массив с телефонами'),
]
