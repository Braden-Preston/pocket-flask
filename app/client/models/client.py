import time
import requests

from box import Box
from flask import redirect, session


class PocketBase:

    base_url: str
    auth_store: str
    token: str

    def __init__(self, base_url='http://127.0.0.1:8090'):
        self.base_url = base_url
        self.sender = requests.Session()

    @property
    def token(self):
        return session.get('token', None)

    def send(self, url='', method='get', body={}, guest=False, **kwargs):

        target_url = f'{self.base_url}/api{url}'

        if method == 'get':
            sender = self.sender.get
        elif method == 'post':
            sender = self.sender.post
        elif method == 'patch':
            sender = self.sender.patch

        if self.token:
            self.sender.headers[
                'Authorization'] = f'Admin {self.token["value"]}'
        if guest:
            self.sender.headers['Authorization'] = ''

        response = sender(target_url, **kwargs, timeout=5)
        code = response.status_code
        data = Box(response.json())

        if code != 200:
            return data, code

        return data, code

    # ----------- Admins - Auth via Email ---------- #

    def admin_auth_via_email(self, email='', password=''):
        data, code = self.send(url='/admins/auth-via-email',
                         method='post',
                         guest=True,
                         json={ 'email': email, 'password': password }) # yapf: disable
        return data, code

    # --------------- Records - List --------------- #

    def records_get_list(self, collection: str, page=1, per_page=30,
        sort='', filters='', expand=''): # yapf: disable

        target_url = f'/collections/{collection}/records'
        params = {
            'page': page,
            'perPage': per_page,
            'sort': sort,
            'filter': filters,
            'expand': expand
        }
        data, code = self.send(url=target_url, method='get', params=params)
        return data

    # ------------- Records - List All ------------- #

    def records_get_full_list(self, collection: str, batchSize=100,
        sort='', filters='', expand=''): # yapf: disable
        # https://github.com/pocketbase/js-sdk/blob/f1f5089e63b129012e9d2fd9203a0d864b8412bb/src/services/utils/BaseCrudService.ts#L17
        pass

    # --------------- Records - View --------------- #

    def records_get_one(self, collection: str, record_id: str = '',
        expand=''): # yapf: disable

        params = {'expand': expand}
        target_url = f'/collections/{collection}/records/{record_id}'
        data, code = self.send(url=target_url, method='get', params=params)
        return data

    # TODO -------------- Records - Create -------------- #

    def records_update(self, collection: str,record_id: str,
        json: dict, expand=''): # yapf: disable

        params = {'expand': expand}
        target_url = f'/collections/{collection}/records/{record_id}'
        data, code = self.send(url=target_url,
                               method='post',
                               json=json,
                               params=params)
        return data

    # -------------- Records - Update -------------- #

    def records_update(self, collection: str,record_id: str,
        json: dict, expand=''): # yapf: disable

        params = {'expand': expand}
        target_url = f'/collections/{collection}/records/{record_id}'
        data, code = self.send(url=target_url,
                               method='patch',
                               json=json,
                               params=params)
        return data

    # TODO -------------- Records - Delete -------------- #