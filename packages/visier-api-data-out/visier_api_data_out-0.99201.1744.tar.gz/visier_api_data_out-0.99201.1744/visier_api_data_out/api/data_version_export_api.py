# coding: utf-8

"""
    Visier Data Out APIs

    Visier APIs for getting data out of Visier, such as aggregate data and data version information.

    The version of the OpenAPI document: 22222222.99201.1744
    Contact: alpine@visier.com

    Please note that this SDK is currently in beta.
    Functionality and behavior may change in future releases.
    We encourage you to provide feedback and report any issues encountered during your use.
"""  # noqa: E501

import warnings
from pydantic import validate_call, Field, StrictFloat, StrictStr, StrictInt
from typing import Any, Dict, List, Optional, Tuple, Union
from typing_extensions import Annotated

from visier_api_core import ApiClient, ApiResponse, RequestSerialized, RESTResponseType

from pydantic import Field, StrictBytes, StrictInt, StrictStr
from typing import Optional, Tuple, Union
from typing_extensions import Annotated
from visier_api_data_out.models.data_version_export_dto import DataVersionExportDTO
from visier_api_data_out.models.data_version_export_data_versions_dto import DataVersionExportDataVersionsDTO
from visier_api_data_out.models.data_version_export_job_status_dto import DataVersionExportJobStatusDTO
from visier_api_data_out.models.data_version_export_schedule_job_request_dto import DataVersionExportScheduleJobRequestDTO
from visier_api_data_out.models.data_version_export_schedule_job_response_dto import DataVersionExportScheduleJobResponseDTO
from visier_api_data_out.models.data_version_exports_dto import DataVersionExportsDTO
import visier_api_data_out.models


class DataVersionExportApi:
    """
    This class provides methods to make requests to the Visier API.
    It uses the ApiClient to handle the HTTP requests and responses.
    """

    def __init__(self, api_client=None) -> None:
        if api_client is None:
            api_client = ApiClient.get_default()
        self.api_client = api_client


    @validate_call
    def call_1_alpha_download_file(
        self,
        export_uuid: Annotated[StrictStr, Field(description="The unique identifier of the data version export.")],
        file_id: Annotated[StrictInt, Field(description="The unique integer identifier of the file within the data version export.")],
        target_tenant_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.")] = None,
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
    ) -> bytearray:
        """Download a file from a data version export

        This API allows you to download a file from a data version export. Data version export files are in CSV format, compressed with gzip.

        :param export_uuid: The unique identifier of the data version export. (required)
        :type export_uuid: str
        :param file_id: The unique integer identifier of the file within the data version export. (required)
        :type file_id: int
        :param target_tenant_id: Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.
        :type target_tenant_id: str
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

        _param = self._call_1_alpha_download_file_serialize(
            export_uuid=export_uuid,
            file_id=file_id,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "bytearray",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_out.models,
            response_data=response_data,
            response_types_map=_response_types_map
        ).data


    @validate_call
    def call_1_alpha_download_file_with_http_info(
        self,
        export_uuid: Annotated[StrictStr, Field(description="The unique identifier of the data version export.")],
        file_id: Annotated[StrictInt, Field(description="The unique integer identifier of the file within the data version export.")],
        target_tenant_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.")] = None,
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
    ) -> ApiResponse[bytearray]:
        """Download a file from a data version export

        This API allows you to download a file from a data version export. Data version export files are in CSV format, compressed with gzip.

        :param export_uuid: The unique identifier of the data version export. (required)
        :type export_uuid: str
        :param file_id: The unique integer identifier of the file within the data version export. (required)
        :type file_id: int
        :param target_tenant_id: Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.
        :type target_tenant_id: str
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

        _param = self._call_1_alpha_download_file_serialize(
            export_uuid=export_uuid,
            file_id=file_id,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "bytearray",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_out.models,
            response_data=response_data,
            response_types_map=_response_types_map
        )


    @validate_call
    def call_1_alpha_download_file_without_preload_content(
        self,
        export_uuid: Annotated[StrictStr, Field(description="The unique identifier of the data version export.")],
        file_id: Annotated[StrictInt, Field(description="The unique integer identifier of the file within the data version export.")],
        target_tenant_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.")] = None,
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
        """Download a file from a data version export

        This API allows you to download a file from a data version export. Data version export files are in CSV format, compressed with gzip.

        :param export_uuid: The unique identifier of the data version export. (required)
        :type export_uuid: str
        :param file_id: The unique integer identifier of the file within the data version export. (required)
        :type file_id: int
        :param target_tenant_id: Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.
        :type target_tenant_id: str
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

        _param = self._call_1_alpha_download_file_serialize(
            export_uuid=export_uuid,
            file_id=file_id,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "bytearray",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        return response_data.response


    def _call_1_alpha_download_file_serialize(
        self,
        export_uuid,
        file_id,
        target_tenant_id,
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
        _files: Dict[str, Union[str, bytes]] = {}
        _body_params: Optional[bytes] = None

        # process the path parameters
        if export_uuid is not None:
            _path_params['exportUuid'] = export_uuid
        if file_id is not None:
            _path_params['fileId'] = file_id
        # process the query parameters
        # process the header parameters
        if target_tenant_id is not None:
            _header_params['TargetTenantID'] = target_tenant_id
        # process the form parameters
        # process the body parameter


        # set the HTTP header `Accept`
        if 'Accept' not in _header_params:
            _header_params['Accept'] = self.api_client.select_header_accept(
                [
                    'application/gzip', 
                    'application/json'
                ]
            )


        # authentication setting
        _auth_settings: List[str] = [
            'CookieAuth', 
            'ApiKeyAuth', 
            'OAuth2Auth', 
            'OAuth2Auth', 
            'BearerAuth'
        ]

        return self.api_client.param_serialize(
            method='GET',
            resource_path='/v1alpha/data/data-version-exports/exports/{exportUuid}/files/{fileId}',
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




    @validate_call
    def get_available_data_versions(
        self,
        target_tenant_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.")] = None,
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
    ) -> DataVersionExportDataVersionsDTO:
        """Retrieve a list of all data versions

        Retrieve a list of all data versions in the tenant.   **Note:** <em>This API is in **alpha**. While in alpha, APIs may change in a breaking way without notice; functionality may be removed, and no deprecation notices will be issued.  If you are interested in using this API, please contact your Customer Success Manager (CSM).</em>

        :param target_tenant_id: Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.
        :type target_tenant_id: str
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

        _param = self._get_available_data_versions_serialize(
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "DataVersionExportDataVersionsDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_out.models,
            response_data=response_data,
            response_types_map=_response_types_map
        ).data


    @validate_call
    def get_available_data_versions_with_http_info(
        self,
        target_tenant_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.")] = None,
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
    ) -> ApiResponse[DataVersionExportDataVersionsDTO]:
        """Retrieve a list of all data versions

        Retrieve a list of all data versions in the tenant.   **Note:** <em>This API is in **alpha**. While in alpha, APIs may change in a breaking way without notice; functionality may be removed, and no deprecation notices will be issued.  If you are interested in using this API, please contact your Customer Success Manager (CSM).</em>

        :param target_tenant_id: Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.
        :type target_tenant_id: str
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

        _param = self._get_available_data_versions_serialize(
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "DataVersionExportDataVersionsDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_out.models,
            response_data=response_data,
            response_types_map=_response_types_map
        )


    @validate_call
    def get_available_data_versions_without_preload_content(
        self,
        target_tenant_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.")] = None,
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
        """Retrieve a list of all data versions

        Retrieve a list of all data versions in the tenant.   **Note:** <em>This API is in **alpha**. While in alpha, APIs may change in a breaking way without notice; functionality may be removed, and no deprecation notices will be issued.  If you are interested in using this API, please contact your Customer Success Manager (CSM).</em>

        :param target_tenant_id: Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.
        :type target_tenant_id: str
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

        _param = self._get_available_data_versions_serialize(
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "DataVersionExportDataVersionsDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        return response_data.response


    def _get_available_data_versions_serialize(
        self,
        target_tenant_id,
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
        _files: Dict[str, Union[str, bytes]] = {}
        _body_params: Optional[bytes] = None

        # process the path parameters
        # process the query parameters
        # process the header parameters
        if target_tenant_id is not None:
            _header_params['TargetTenantID'] = target_tenant_id
        # process the form parameters
        # process the body parameter


        # set the HTTP header `Accept`
        if 'Accept' not in _header_params:
            _header_params['Accept'] = self.api_client.select_header_accept(
                [
                    'application/json'
                ]
            )


        # authentication setting
        _auth_settings: List[str] = [
            'CookieAuth', 
            'ApiKeyAuth', 
            'OAuth2Auth', 
            'OAuth2Auth', 
            'BearerAuth'
        ]

        return self.api_client.param_serialize(
            method='GET',
            resource_path='/v1alpha/data/data-version-exports/data-versions',
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




    @validate_call
    def get_available_exports(
        self,
        target_tenant_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.")] = None,
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
    ) -> DataVersionExportsDTO:
        """Retrieve the details of all data version exports

        Retrieve the information for all available data version exports.  **Note:** Data version exports are available for 14 days after export job completes.   **Note:** <em>This API is in **alpha**. While in alpha, APIs may change in a breaking way without notice; functionality may be removed, and no deprecation notices will be issued.  If you are interested in using this API, please contact your Customer Success Manager (CSM).</em>

        :param target_tenant_id: Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.
        :type target_tenant_id: str
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

        _param = self._get_available_exports_serialize(
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "DataVersionExportsDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_out.models,
            response_data=response_data,
            response_types_map=_response_types_map
        ).data


    @validate_call
    def get_available_exports_with_http_info(
        self,
        target_tenant_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.")] = None,
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
    ) -> ApiResponse[DataVersionExportsDTO]:
        """Retrieve the details of all data version exports

        Retrieve the information for all available data version exports.  **Note:** Data version exports are available for 14 days after export job completes.   **Note:** <em>This API is in **alpha**. While in alpha, APIs may change in a breaking way without notice; functionality may be removed, and no deprecation notices will be issued.  If you are interested in using this API, please contact your Customer Success Manager (CSM).</em>

        :param target_tenant_id: Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.
        :type target_tenant_id: str
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

        _param = self._get_available_exports_serialize(
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "DataVersionExportsDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_out.models,
            response_data=response_data,
            response_types_map=_response_types_map
        )


    @validate_call
    def get_available_exports_without_preload_content(
        self,
        target_tenant_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.")] = None,
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
        """Retrieve the details of all data version exports

        Retrieve the information for all available data version exports.  **Note:** Data version exports are available for 14 days after export job completes.   **Note:** <em>This API is in **alpha**. While in alpha, APIs may change in a breaking way without notice; functionality may be removed, and no deprecation notices will be issued.  If you are interested in using this API, please contact your Customer Success Manager (CSM).</em>

        :param target_tenant_id: Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.
        :type target_tenant_id: str
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

        _param = self._get_available_exports_serialize(
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "DataVersionExportsDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        return response_data.response


    def _get_available_exports_serialize(
        self,
        target_tenant_id,
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
        _files: Dict[str, Union[str, bytes]] = {}
        _body_params: Optional[bytes] = None

        # process the path parameters
        # process the query parameters
        # process the header parameters
        if target_tenant_id is not None:
            _header_params['TargetTenantID'] = target_tenant_id
        # process the form parameters
        # process the body parameter


        # set the HTTP header `Accept`
        if 'Accept' not in _header_params:
            _header_params['Accept'] = self.api_client.select_header_accept(
                [
                    'application/json'
                ]
            )


        # authentication setting
        _auth_settings: List[str] = [
            'CookieAuth', 
            'ApiKeyAuth', 
            'OAuth2Auth', 
            'OAuth2Auth', 
            'BearerAuth'
        ]

        return self.api_client.param_serialize(
            method='GET',
            resource_path='/v1alpha/data/data-version-exports/exports',
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




    @validate_call
    def get_export(
        self,
        export_uuid: Annotated[StrictStr, Field(description="The unique identifier of the data version export.")],
        target_tenant_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.")] = None,
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
    ) -> DataVersionExportDTO:
        """Retrieve the details of a data version export

        Retrieve information for a specific data version export.  **Note:** Data version exports are available for 14 days after export job completes.   **Note:** <em>This API is in **alpha**. While in alpha, APIs may change in a breaking way without notice; functionality may be removed, and no deprecation notices will be issued.  If you are interested in using this API, please contact your Customer Success Manager (CSM).</em>

        :param export_uuid: The unique identifier of the data version export. (required)
        :type export_uuid: str
        :param target_tenant_id: Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.
        :type target_tenant_id: str
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

        _param = self._get_export_serialize(
            export_uuid=export_uuid,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "DataVersionExportDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_out.models,
            response_data=response_data,
            response_types_map=_response_types_map
        ).data


    @validate_call
    def get_export_with_http_info(
        self,
        export_uuid: Annotated[StrictStr, Field(description="The unique identifier of the data version export.")],
        target_tenant_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.")] = None,
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
    ) -> ApiResponse[DataVersionExportDTO]:
        """Retrieve the details of a data version export

        Retrieve information for a specific data version export.  **Note:** Data version exports are available for 14 days after export job completes.   **Note:** <em>This API is in **alpha**. While in alpha, APIs may change in a breaking way without notice; functionality may be removed, and no deprecation notices will be issued.  If you are interested in using this API, please contact your Customer Success Manager (CSM).</em>

        :param export_uuid: The unique identifier of the data version export. (required)
        :type export_uuid: str
        :param target_tenant_id: Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.
        :type target_tenant_id: str
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

        _param = self._get_export_serialize(
            export_uuid=export_uuid,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "DataVersionExportDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_out.models,
            response_data=response_data,
            response_types_map=_response_types_map
        )


    @validate_call
    def get_export_without_preload_content(
        self,
        export_uuid: Annotated[StrictStr, Field(description="The unique identifier of the data version export.")],
        target_tenant_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.")] = None,
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
        """Retrieve the details of a data version export

        Retrieve information for a specific data version export.  **Note:** Data version exports are available for 14 days after export job completes.   **Note:** <em>This API is in **alpha**. While in alpha, APIs may change in a breaking way without notice; functionality may be removed, and no deprecation notices will be issued.  If you are interested in using this API, please contact your Customer Success Manager (CSM).</em>

        :param export_uuid: The unique identifier of the data version export. (required)
        :type export_uuid: str
        :param target_tenant_id: Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.
        :type target_tenant_id: str
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

        _param = self._get_export_serialize(
            export_uuid=export_uuid,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "DataVersionExportDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        return response_data.response


    def _get_export_serialize(
        self,
        export_uuid,
        target_tenant_id,
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
        _files: Dict[str, Union[str, bytes]] = {}
        _body_params: Optional[bytes] = None

        # process the path parameters
        if export_uuid is not None:
            _path_params['exportUuid'] = export_uuid
        # process the query parameters
        # process the header parameters
        if target_tenant_id is not None:
            _header_params['TargetTenantID'] = target_tenant_id
        # process the form parameters
        # process the body parameter


        # set the HTTP header `Accept`
        if 'Accept' not in _header_params:
            _header_params['Accept'] = self.api_client.select_header_accept(
                [
                    'application/json'
                ]
            )


        # authentication setting
        _auth_settings: List[str] = [
            'CookieAuth', 
            'ApiKeyAuth', 
            'OAuth2Auth', 
            'OAuth2Auth', 
            'BearerAuth'
        ]

        return self.api_client.param_serialize(
            method='GET',
            resource_path='/v1alpha/data/data-version-exports/exports/{exportUuid}',
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




    @validate_call
    def get_export_job_status(
        self,
        job_uuid: Annotated[StrictStr, Field(description="The unique identifier of the data version export job.")],
        target_tenant_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.")] = None,
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
    ) -> DataVersionExportJobStatusDTO:
        """Retrieve a data version export job's status

        Retrieve the status of a data version export job. After the job completes successfully, this endpoint returns an `exportUuid` that you can use to retrieve the export information and download export files.   **Note:** <em>This API is in **alpha**. While in alpha, APIs may change in a breaking way without notice; functionality may be removed, and no deprecation notices will be issued.  If you are interested in using this API, please contact your Customer Success Manager (CSM).</em>

        :param job_uuid: The unique identifier of the data version export job. (required)
        :type job_uuid: str
        :param target_tenant_id: Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.
        :type target_tenant_id: str
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

        _param = self._get_export_job_status_serialize(
            job_uuid=job_uuid,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "DataVersionExportJobStatusDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_out.models,
            response_data=response_data,
            response_types_map=_response_types_map
        ).data


    @validate_call
    def get_export_job_status_with_http_info(
        self,
        job_uuid: Annotated[StrictStr, Field(description="The unique identifier of the data version export job.")],
        target_tenant_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.")] = None,
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
    ) -> ApiResponse[DataVersionExportJobStatusDTO]:
        """Retrieve a data version export job's status

        Retrieve the status of a data version export job. After the job completes successfully, this endpoint returns an `exportUuid` that you can use to retrieve the export information and download export files.   **Note:** <em>This API is in **alpha**. While in alpha, APIs may change in a breaking way without notice; functionality may be removed, and no deprecation notices will be issued.  If you are interested in using this API, please contact your Customer Success Manager (CSM).</em>

        :param job_uuid: The unique identifier of the data version export job. (required)
        :type job_uuid: str
        :param target_tenant_id: Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.
        :type target_tenant_id: str
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

        _param = self._get_export_job_status_serialize(
            job_uuid=job_uuid,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "DataVersionExportJobStatusDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_out.models,
            response_data=response_data,
            response_types_map=_response_types_map
        )


    @validate_call
    def get_export_job_status_without_preload_content(
        self,
        job_uuid: Annotated[StrictStr, Field(description="The unique identifier of the data version export job.")],
        target_tenant_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.")] = None,
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
        """Retrieve a data version export job's status

        Retrieve the status of a data version export job. After the job completes successfully, this endpoint returns an `exportUuid` that you can use to retrieve the export information and download export files.   **Note:** <em>This API is in **alpha**. While in alpha, APIs may change in a breaking way without notice; functionality may be removed, and no deprecation notices will be issued.  If you are interested in using this API, please contact your Customer Success Manager (CSM).</em>

        :param job_uuid: The unique identifier of the data version export job. (required)
        :type job_uuid: str
        :param target_tenant_id: Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.
        :type target_tenant_id: str
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

        _param = self._get_export_job_status_serialize(
            job_uuid=job_uuid,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "DataVersionExportJobStatusDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        return response_data.response


    def _get_export_job_status_serialize(
        self,
        job_uuid,
        target_tenant_id,
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
        _files: Dict[str, Union[str, bytes]] = {}
        _body_params: Optional[bytes] = None

        # process the path parameters
        if job_uuid is not None:
            _path_params['jobUuid'] = job_uuid
        # process the query parameters
        # process the header parameters
        if target_tenant_id is not None:
            _header_params['TargetTenantID'] = target_tenant_id
        # process the form parameters
        # process the body parameter


        # set the HTTP header `Accept`
        if 'Accept' not in _header_params:
            _header_params['Accept'] = self.api_client.select_header_accept(
                [
                    'application/json'
                ]
            )


        # authentication setting
        _auth_settings: List[str] = [
            'CookieAuth', 
            'ApiKeyAuth', 
            'OAuth2Auth', 
            'OAuth2Auth', 
            'BearerAuth'
        ]

        return self.api_client.param_serialize(
            method='GET',
            resource_path='/v1alpha/data/data-version-exports/jobs/{jobUuid}',
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




    @validate_call
    def schedule_export_job(
        self,
        data_version_export_schedule_job_request_dto: DataVersionExportScheduleJobRequestDTO,
        target_tenant_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.")] = None,
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
    ) -> DataVersionExportScheduleJobResponseDTO:
        """Schedule a data version export job

        Schedule a data version export job. The job schedules immediately and will begin when resources are available. The response returns a `jobUuid` that you can use to check the export job status.   **Note:** There is a limit of 10 export jobs per tenant per day.   **Note:** <em>This API is in **alpha**. While in alpha, APIs may change in a breaking way without notice; functionality may be removed, and no deprecation notices will be issued.  If you are interested in using this API, please contact your Customer Success Manager (CSM).</em>

        :param data_version_export_schedule_job_request_dto: (required)
        :type data_version_export_schedule_job_request_dto: DataVersionExportScheduleJobRequestDTO
        :param target_tenant_id: Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.
        :type target_tenant_id: str
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

        _param = self._schedule_export_job_serialize(
            data_version_export_schedule_job_request_dto=data_version_export_schedule_job_request_dto,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "DataVersionExportScheduleJobResponseDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_out.models,
            response_data=response_data,
            response_types_map=_response_types_map
        ).data


    @validate_call
    def schedule_export_job_with_http_info(
        self,
        data_version_export_schedule_job_request_dto: DataVersionExportScheduleJobRequestDTO,
        target_tenant_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.")] = None,
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
    ) -> ApiResponse[DataVersionExportScheduleJobResponseDTO]:
        """Schedule a data version export job

        Schedule a data version export job. The job schedules immediately and will begin when resources are available. The response returns a `jobUuid` that you can use to check the export job status.   **Note:** There is a limit of 10 export jobs per tenant per day.   **Note:** <em>This API is in **alpha**. While in alpha, APIs may change in a breaking way without notice; functionality may be removed, and no deprecation notices will be issued.  If you are interested in using this API, please contact your Customer Success Manager (CSM).</em>

        :param data_version_export_schedule_job_request_dto: (required)
        :type data_version_export_schedule_job_request_dto: DataVersionExportScheduleJobRequestDTO
        :param target_tenant_id: Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.
        :type target_tenant_id: str
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

        _param = self._schedule_export_job_serialize(
            data_version_export_schedule_job_request_dto=data_version_export_schedule_job_request_dto,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "DataVersionExportScheduleJobResponseDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_out.models,
            response_data=response_data,
            response_types_map=_response_types_map
        )


    @validate_call
    def schedule_export_job_without_preload_content(
        self,
        data_version_export_schedule_job_request_dto: DataVersionExportScheduleJobRequestDTO,
        target_tenant_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.")] = None,
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
        """Schedule a data version export job

        Schedule a data version export job. The job schedules immediately and will begin when resources are available. The response returns a `jobUuid` that you can use to check the export job status.   **Note:** There is a limit of 10 export jobs per tenant per day.   **Note:** <em>This API is in **alpha**. While in alpha, APIs may change in a breaking way without notice; functionality may be removed, and no deprecation notices will be issued.  If you are interested in using this API, please contact your Customer Success Manager (CSM).</em>

        :param data_version_export_schedule_job_request_dto: (required)
        :type data_version_export_schedule_job_request_dto: DataVersionExportScheduleJobRequestDTO
        :param target_tenant_id: Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.
        :type target_tenant_id: str
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

        _param = self._schedule_export_job_serialize(
            data_version_export_schedule_job_request_dto=data_version_export_schedule_job_request_dto,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "DataVersionExportScheduleJobResponseDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        return response_data.response


    def _schedule_export_job_serialize(
        self,
        data_version_export_schedule_job_request_dto,
        target_tenant_id,
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
        _files: Dict[str, Union[str, bytes]] = {}
        _body_params: Optional[bytes] = None

        # process the path parameters
        # process the query parameters
        # process the header parameters
        if target_tenant_id is not None:
            _header_params['TargetTenantID'] = target_tenant_id
        # process the form parameters
        # process the body parameter
        if data_version_export_schedule_job_request_dto is not None:
            _body_params = data_version_export_schedule_job_request_dto


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
                        'application/json'
                    ]
                )
            )
            if _default_content_type is not None:
                _header_params['Content-Type'] = _default_content_type

        # authentication setting
        _auth_settings: List[str] = [
            'CookieAuth', 
            'ApiKeyAuth', 
            'OAuth2Auth', 
            'OAuth2Auth', 
            'BearerAuth'
        ]

        return self.api_client.param_serialize(
            method='POST',
            resource_path='/v1alpha/data/data-version-exports/jobs',
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


