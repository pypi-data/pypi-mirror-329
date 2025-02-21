# coding: utf-8

"""
    Platform API

    _OpenAPI specification for the **Platform API** of **Empire**, the allocation and nomination platform of BritNed_  ---  Additional documentation available in the API's [GitHub repository](https://github.com/britned/empire-platform-api) 

    The version of the OpenAPI document: 6.0.0
    Contact: britned.info@britned.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501

import warnings
from pydantic import validate_call, Field, StrictFloat, StrictStr, StrictInt
from typing import Any, Dict, List, Optional, Tuple, Union
from typing_extensions import Annotated

from pydantic import StrictBytes, StrictStr
from typing import Tuple, Union
from empire_platform_api_public_client.models.attachment import Attachment

from empire_platform_api_public_client.api_client import ApiClient, RequestSerialized
from empire_platform_api_public_client.api_response import ApiResponse
from empire_platform_api_public_client.rest import RESTResponseType


class AttachmentApi:
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None) -> None:
        if api_client is None:
            api_client = ApiClient.get_default()
        self.api_client = api_client


    @validate_call
    def upload_attachment(
        self,
        file_name: StrictStr,
        file: Union[StrictBytes, StrictStr, Tuple[StrictStr, StrictBytes]],
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> Attachment:
        """upload_attachment

        Upload a single Attachment (file)  On successful upload the file gets persisted and metadata for the Attachment is returned. The Attachment can be referenced by its identifier in other functions (e.g Organisation Documents)  **File size limit:** 50 MB  **File types accepted:**   * images:     - .jpg  | image/jpeg     - .png  | image/png   * documents:     - .doc  | application/msword     - .docx | application/vnd.openxmlformats-officedocument.wordprocessingml.document     - .xls  | application/vnd.ms-excel     - .xlsx | application/vnd.openxmlformats-officedocument.spreadsheetml.sheet     - .ppt  | application/vnd.ms-powerpoint     - .pptx | application/vnd.openxmlformats-officedocument.presentationml.presentation     - .pdf  | application/pdf   * text files:     - .txt  | text/plain     - .xml  | application/xml     - .json | application/json   * archives:     - .zip  | application/zip     - .rar  | application/vnd.rar  ---  __Requires Permission:__ (at least one)   * `MANAGE_CRISIS_ACTIONS`   * `INVITE_USERS`   * `MANAGE_OWN_MANUAL_FILE_UPLOAD_BIDS`   * `MANAGE_OWN_MANUAL_FILE_UPLOAD_NOMINATIONS`   * `MANAGE_ANY_MANUAL_FILE_UPLOAD`   * `MANAGE_ANY_ORGANISATION_DOCUMENTS`   * `MANAGE_OWN_ORGANISATION_DOCUMENTS`  __Generates Audit Log Entry:__ `UPLOAD_ATTACHMENT`

        :param file_name: (required)
        :type file_name: str
        :param file: (required)
        :type file: bytearray
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._upload_attachment_serialize(
            file_name=file_name,
            file=file,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '201': "Attachment",
            '401': "ErrorResponse",
            '403': "ErrorResponse",
            '413': None,
            '422': "ErrorResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        ).data


    @validate_call
    def upload_attachment_with_http_info(
        self,
        file_name: StrictStr,
        file: Union[StrictBytes, StrictStr, Tuple[StrictStr, StrictBytes]],
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> ApiResponse[Attachment]:
        """upload_attachment

        Upload a single Attachment (file)  On successful upload the file gets persisted and metadata for the Attachment is returned. The Attachment can be referenced by its identifier in other functions (e.g Organisation Documents)  **File size limit:** 50 MB  **File types accepted:**   * images:     - .jpg  | image/jpeg     - .png  | image/png   * documents:     - .doc  | application/msword     - .docx | application/vnd.openxmlformats-officedocument.wordprocessingml.document     - .xls  | application/vnd.ms-excel     - .xlsx | application/vnd.openxmlformats-officedocument.spreadsheetml.sheet     - .ppt  | application/vnd.ms-powerpoint     - .pptx | application/vnd.openxmlformats-officedocument.presentationml.presentation     - .pdf  | application/pdf   * text files:     - .txt  | text/plain     - .xml  | application/xml     - .json | application/json   * archives:     - .zip  | application/zip     - .rar  | application/vnd.rar  ---  __Requires Permission:__ (at least one)   * `MANAGE_CRISIS_ACTIONS`   * `INVITE_USERS`   * `MANAGE_OWN_MANUAL_FILE_UPLOAD_BIDS`   * `MANAGE_OWN_MANUAL_FILE_UPLOAD_NOMINATIONS`   * `MANAGE_ANY_MANUAL_FILE_UPLOAD`   * `MANAGE_ANY_ORGANISATION_DOCUMENTS`   * `MANAGE_OWN_ORGANISATION_DOCUMENTS`  __Generates Audit Log Entry:__ `UPLOAD_ATTACHMENT`

        :param file_name: (required)
        :type file_name: str
        :param file: (required)
        :type file: bytearray
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._upload_attachment_serialize(
            file_name=file_name,
            file=file,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '201': "Attachment",
            '401': "ErrorResponse",
            '403': "ErrorResponse",
            '413': None,
            '422': "ErrorResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        )


    @validate_call
    def upload_attachment_without_preload_content(
        self,
        file_name: StrictStr,
        file: Union[StrictBytes, StrictStr, Tuple[StrictStr, StrictBytes]],
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> RESTResponseType:
        """upload_attachment

        Upload a single Attachment (file)  On successful upload the file gets persisted and metadata for the Attachment is returned. The Attachment can be referenced by its identifier in other functions (e.g Organisation Documents)  **File size limit:** 50 MB  **File types accepted:**   * images:     - .jpg  | image/jpeg     - .png  | image/png   * documents:     - .doc  | application/msword     - .docx | application/vnd.openxmlformats-officedocument.wordprocessingml.document     - .xls  | application/vnd.ms-excel     - .xlsx | application/vnd.openxmlformats-officedocument.spreadsheetml.sheet     - .ppt  | application/vnd.ms-powerpoint     - .pptx | application/vnd.openxmlformats-officedocument.presentationml.presentation     - .pdf  | application/pdf   * text files:     - .txt  | text/plain     - .xml  | application/xml     - .json | application/json   * archives:     - .zip  | application/zip     - .rar  | application/vnd.rar  ---  __Requires Permission:__ (at least one)   * `MANAGE_CRISIS_ACTIONS`   * `INVITE_USERS`   * `MANAGE_OWN_MANUAL_FILE_UPLOAD_BIDS`   * `MANAGE_OWN_MANUAL_FILE_UPLOAD_NOMINATIONS`   * `MANAGE_ANY_MANUAL_FILE_UPLOAD`   * `MANAGE_ANY_ORGANISATION_DOCUMENTS`   * `MANAGE_OWN_ORGANISATION_DOCUMENTS`  __Generates Audit Log Entry:__ `UPLOAD_ATTACHMENT`

        :param file_name: (required)
        :type file_name: str
        :param file: (required)
        :type file: bytearray
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._upload_attachment_serialize(
            file_name=file_name,
            file=file,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '201': "Attachment",
            '401': "ErrorResponse",
            '403': "ErrorResponse",
            '413': None,
            '422': "ErrorResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        return response_data.response


    def _upload_attachment_serialize(
        self,
        file_name,
        file,
        _request_auth,
        _content_type,
        _headers,
        _host_index,
    ) -> RequestSerialized:

        _host = None

        _collection_formats: Dict[str, str] = {
        }

        _path_params: Dict[str, str] = {}
        _query_params: List[Tuple[str, str]] = []
        _header_params: Dict[str, Optional[str]] = _headers or {}
        _form_params: List[Tuple[str, str]] = []
        _files: Dict[
            str, Union[str, bytes, List[str], List[bytes], List[Tuple[str, bytes]]]
        ] = {}
        _body_params: Optional[bytes] = None

        # process the path parameters
        # process the query parameters
        # process the header parameters
        # process the form parameters
        if file_name is not None:
            _form_params.append(('fileName', file_name))
        if file is not None:
            _files['file'] = file
        # process the body parameter


        # set the HTTP header `Accept`
        if 'Accept' not in _header_params:
            _header_params['Accept'] = self.api_client.select_header_accept(
                [
                    'application/json'
                ]
            )

        # set the HTTP header `Content-Type`
        if _content_type:
            _header_params['Content-Type'] = _content_type
        else:
            _default_content_type = (
                self.api_client.select_header_content_type(
                    [
                        'multipart/form-data'
                    ]
                )
            )
            if _default_content_type is not None:
                _header_params['Content-Type'] = _default_content_type

        # authentication setting
        _auth_settings: List[str] = [
            'ApiKey', 
            'AuthToken'
        ]

        return self.api_client.param_serialize(
            method='POST',
            resource_path='/v1/attachments',
            path_params=_path_params,
            query_params=_query_params,
            header_params=_header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            auth_settings=_auth_settings,
            collection_formats=_collection_formats,
            _host=_host,
            _request_auth=_request_auth
        )


