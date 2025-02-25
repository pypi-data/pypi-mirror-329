from contextlib import suppress
import importlib.metadata
import json
from http import HTTPStatus

import lz4.frame
from pathlib import Path
import httpx
from typing import Mapping
import validators

from hhdm_apiclient_wrapper.authentication_manager import AuthenticationManager
from hhdm_apiclient_wrapper.models import *


class ApiClient:
    # By default, requests library will not timeout if timeout is set to None
    # Timeout can also be passed as a tuple (connect_timeout_seconds, response_timeout_seconds)
    MAX_TIMEOUT_SECONDS = None  # 20 * 60

    def __init__(self, authentication_manager: AuthenticationManager, api_host: str | None = None, feature_flag: str | None = None) -> None:
        self._is_dev = False
        self._feature_flag = feature_flag

        if api_host:
            if 'localhost' in api_host:
                self._is_dev = True
                self.api_endpoint = api_host
            elif validators.url(api_host):
                self.api_endpoint = api_host
            elif validators.url('https://' + api_host):
                self.api_endpoint = 'https://' + api_host
            else:
                raise ValueError(f'Passed argument apiHost ({api_host}) is not a valid URI.')
            if self.api_endpoint[-1] != '/':
                self.api_endpoint += '/'
        else:
            self.api_endpoint = 'https://hhdm-api.hh-dev.com/'

        self._authentication_manager = authentication_manager

        self._aclient = httpx.AsyncClient(verify=not self._is_dev)

    async def close(self):
        await self._aclient.aclose()

# region Manual Endpoints

    async def get_part_item_mileages_by_event(self, account_id: str, part_item_ids: List[str]) -> ApiGetResult[List[MileageRecordByEvent]]:
        if isinstance(part_item_ids, str):
            part_item_ids = [part_item_ids]
        if not isinstance(part_item_ids, List):
            raise TypeError('part_item_ids must be either a list of ids or a string containing a single id')
        
        return await self._get_item_mileages_by_event(account_id, ItemMileageRequest(part_item_ids=part_item_ids))
        
    async def get_assembly_iteration_mileages_by_event(self, account_id: str, assembly_iteration_ids: List[str]) -> ApiGetResult[List[MileageRecordByEvent]]:
        if isinstance(assembly_iteration_ids, str):
            assembly_iteration_ids = [assembly_iteration_ids]
        if not isinstance(assembly_iteration_ids, List):
            raise TypeError('assembly_iteration_ids must be either a list of ids or a string containing a single id')
        
        return await self._get_item_mileages_by_event(account_id, ItemMileageRequest(assembly_iteration_ids=assembly_iteration_ids))

    async def _get_item_mileages_by_event(self, account_id: str, item_mileage_request: ItemMileageRequest) -> ApiGetResult[List[MileageRecordByEvent] | None]:
        try:
            url = f'{self.api_endpoint}Mileage/PartItems?{self.build_url_parameters(None, {"byEvent": True})}'
            response = await self.get_request(account_id, url, item_mileage_request, self.MAX_TIMEOUT_SECONDS)

            if not response.is_success:
                return ApiGetResult(None, False, response.reason_phrase, response.status_code)

            response_string = response.content.decode()
            if not response_string:
                return ApiGetResult(None, False, 'The mileage items requested were not found.', response.status_code)
            
            response_json = json.loads(response_string)
            response_object = [MileageRecordByEvent.deserialize(**o) for o in response_json]

            return ApiGetResult(response_object, True, None, response.status_code)
        except Exception as e:
            return ApiGetResult(None, False, f'Internal server error: {e}', HTTPStatus.INTERNAL_SERVER_ERROR)
        
    async def get_all_mileages_by_event(self, account_id: str) -> ApiGetResult[MileagesResult[MileageRecordByEvent] | None]:
        try:
            url = f'{self.api_endpoint}Mileage/All?{self.build_url_parameters(None, {"accountId": account_id, "byEvent": True})}'
            response = await self.get_request(account_id, url, timeout=self.MAX_TIMEOUT_SECONDS)

            if not response.is_success:
                return ApiGetResult(None, False, response.reason_phrase, response.status_code)

            response_string = response.content.decode()
            if not response_string:
                return ApiGetResult(None, False, 'No items with mileages were found on the requested account.', response.status_code)

            response_json = json.loads(response_string)
            response_object = MileagesResult.deserialize(**response_json)

            return ApiGetResult(response_object, True, None, response.status_code)
        except Exception as e:
            return ApiGetResult(None, False, f'Internal server error: {e}', HTTPStatus.INTERNAL_SERVER_ERROR)

    async def get_all_accounts(self) -> ApiGetResult[List[Mapping[str, str]] | None]:
        url = f'{self.api_endpoint}Accounts/GetAll'
        response = await self.get_request(None, url)

        if not response.is_success:
            return ApiGetResult(None, False, response.reason_phrase)

        response_string = response.content.decode()
        if not response_string:
            return ApiGetResult(None, False, 'Failed to retrieve any accounts.', response.status_code)

        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None, response.status_code)


    #### NOT REQUIRED FOR V1 ####
    '''
    async def get_account_options_by_id(self, account_id: str, options: ApiGetOptions) -> Future[ApiGetResult[ApiAccountOptionsModel]]:
        url = f'{self.api_endpoint}AccountOptions/{account_id}'

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += '?' + url_parameters

        response: requests.Response = await requests.get(url)

        if not response.ok:
            return ApiGetResult[ApiAccountOptionsModel](None, False, response.reason)

        response_string = response.content.decode()
        response_object = ApiAccountOptionsModel(**(json.loads(response_string)))
        return ApiGetResult[ApiAccountOptionsModel](response_object, True, None)
    '''

# endregion

# region Network Functions

    async def get_request(self, account_id: str | None, uri: str, body: IApiModel | None = None, timeout: float | tuple[float] | None = None) -> httpx.Response:
        headers = await self.prepare_request(account_id)
        if body is None:
            return await self._aclient.get(uri, headers=headers, timeout=timeout)
        else:
            content = body.serialize()
            return await self._aclient.request("GET", uri, json=content, headers=headers, timeout=timeout)

    async def post_request(self, account_id: str, uri: str, body: IApiModel | None = None) -> httpx.Response:
        content = body.serialize() if body is not None else {}
        headers = await self.prepare_request(account_id)

        return await self._aclient.post(uri, json=content, headers=headers)

    async def put_request(self, account_id: str, uri: str, body: IApiModel | None = None) -> httpx.Response:
        content = body.serialize() if body is not None else {}
        # Content-Type is only required for put request for some reason
        headers = await self.prepare_request(account_id, {'Content-Type': 'application/json'})

        return await self._aclient.put(uri, json=content, headers=headers)

    async def delete_request(self, account_id: str, uri: str) -> httpx.Response:
        headers = await self.prepare_request(account_id)

        return await self._aclient.delete(uri, headers=headers)
    
    async def upload_file(self, uri: str, file, headers: Mapping[str, str]) -> bool:
        r"""Uploads a file without compressing it.

        :param uri: URL to upload to.
        :param file: path of the file to upload on the local filesystem, or stream-like object to upload.
        :param headers: Dictionary of headers to create the request with.
        :return: whether the upload request succeeds or not.
        :rtype: bool
        """

        if isinstance(file, str):
            with open(file, 'rb') as f:
                response = await self._aclient.put(uri, content=f, headers=headers)
                return response.is_success
        else:
            response = await self._aclient.put(uri, content=file, headers=headers)
            return response.is_success
        
    async def compress_and_upload_file(self, uri: str, file, headers: Mapping[str, str]) -> bool:
        r"""Compresses an entire file or filestream before uploading it.

        :param uri: URL to upload to.
        :param file: path of the file to upload on the local filesystem, or bytes-like object to upload.
        :param headers: Dictionary of headers to create the request with.
        :return: whether the upload request succeeds or not.
        :rtype: bool
        """

        if isinstance(file, str):
            with open(file, 'rb') as f:
                compressed = lz4.frame.compress(f.read())
                response = await self._aclient.put(uri, content=compressed, headers=headers)
                return response.is_success
        else:
            compressed = lz4.frame.compress(file)
            response = await self._aclient.put(uri, content=compressed, headers=headers)
            return response.is_success

    async def prepare_request(self, account_id: str, other_headers: Mapping = None) -> Mapping:
        headers = {
            "AccountId": account_id or '',
            **(await self._authentication_manager.get_http_request_auth())
        }
        if other_headers:
            headers = {**headers, **other_headers}
        if self._feature_flag:
            headers["FeatureFlag"] = self._feature_flag
        
        return headers

    def _serialize_body(self, body: Mapping) -> bytes:
        return json.dumps(body).encode('utf8') if body is not None else None

    def build_url_parameters(self, options: ApiGetOptions | None, additional_parameters: Dict[str, str | bool] = {}) -> str:
        if options is not None:
            if options.parameters_to_include is not None and len(options.parameters_to_include) > 0:
                additional_parameters['parametersToInclude'] = ','.join(options.parameters_to_include)
        
        return '&'.join([f'{k}={v}' for k, v in list(additional_parameters.items())])

    async def _send_debug_request(self, method: str, uri: str, json: Mapping, headers: Mapping) -> httpx.Response:
        request = self._aclient.build_request(method, uri, json=json, headers=headers)

        print('{}\n{}\r\n{}\r\n\r\n{}'.format(
                '-----------START-----------',
                request.method + ' ' + request.url,
                '\r\n'.join('{}: {}'.format(k, v) for k, v in request.headers.items()),
                request.content.decode(),
            ))

        return await self._aclient.send(request)

# endregion

    @staticmethod
    def get_version(include_found_dir: bool = False) -> str:
        """Returns either the version found in the parent pyproject.toml file, or the installed package"""
        with suppress(FileNotFoundError, StopIteration):
            with open(f'{(root_dir := Path(__file__).parent.parent)}/pyproject.toml', encoding='utf-8') as pyproject_toml:
                version = (
                    next(line for line in pyproject_toml if line.startswith('version'))
                    .split('=')[1]
                    .strip('\'"\n ')
                )
                return f'{version} (local dev){f" ({root_dir})" if include_found_dir else ""}'
        return importlib.metadata.version(__name__.split(".", maxsplit=1)[0])

    
