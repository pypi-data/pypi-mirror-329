# coding: utf-8

"""
    Visier Data In APIs

    Visier APIs for sending data to Visier and running data load jobs.

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

from pydantic import Field, StrictBool, StrictInt, StrictStr
from typing import Optional
from typing_extensions import Annotated
from visier_api_data_in.models.assign_connector_credential_request import AssignConnectorCredentialRequest
from visier_api_data_in.models.assign_connector_credentials_response_dto import AssignConnectorCredentialsResponseDTO
from visier_api_data_in.models.cancel_job_batch_from_job_id_dto import CancelJobBatchFromJobIdDTO
from visier_api_data_in.models.consolidated_analytics_job_request_dto import ConsolidatedAnalyticsJobRequestDTO
from visier_api_data_in.models.credential_creation_api_response_dto import CredentialCreationAPIResponseDTO
from visier_api_data_in.models.data_categories_response_dto import DataCategoriesResponseDTO
from visier_api_data_in.models.data_load_request import DataLoadRequest
from visier_api_data_in.models.data_load_response import DataLoadResponse
from visier_api_data_in.models.data_provider_auth_information_dto import DataProviderAuthInformationDTO
from visier_api_data_in.models.disable_dv_request import DisableDVRequest
from visier_api_data_in.models.disable_dv_response import DisableDVResponse
from visier_api_data_in.models.dispatching_job_status_response import DispatchingJobStatusResponse
from visier_api_data_in.models.exclude_data_uploads_request import ExcludeDataUploadsRequest
from visier_api_data_in.models.extract_data_and_load_dto import ExtractDataAndLoadDTO
from visier_api_data_in.models.extraction_job_and_status_response import ExtractionJobAndStatusResponse
from visier_api_data_in.models.extractor_credentials_apidto import ExtractorCredentialsAPIDTO
from visier_api_data_in.models.extractor_settings_apidto import ExtractorSettingsAPIDTO
from visier_api_data_in.models.import_definitions_apidto import ImportDefinitionsAPIDTO
from visier_api_data_in.models.include_data_uploads_request import IncludeDataUploadsRequest
from visier_api_data_in.models.job_cancellation_results_dto import JobCancellationResultsDTO
from visier_api_data_in.models.job_id_response import JobIdResponse
from visier_api_data_in.models.job_status_list_response import JobStatusListResponse
from visier_api_data_in.models.multiple_tenant_data_versions_list_dto import MultipleTenantDataVersionsListDTO
from visier_api_data_in.models.processing_job_and_status_response import ProcessingJobAndStatusResponse
from visier_api_data_in.models.processing_job_request_dto import ProcessingJobRequestDTO
from visier_api_data_in.models.processing_job_status_response import ProcessingJobStatusResponse
from visier_api_data_in.models.receiving_job_and_status_response import ReceivingJobAndStatusResponse
from visier_api_data_in.models.receiving_job_status_response import ReceivingJobStatusResponse
from visier_api_data_in.models.set_connector_settings_request_dto import SetConnectorSettingsRequestDTO
from visier_api_data_in.models.set_connector_settings_response_dto import SetConnectorSettingsResponseDTO
from visier_api_data_in.models.start_extraction_response import StartExtractionResponse
from visier_api_data_in.models.tenant_data_uploads_list_response_dto import TenantDataUploadsListResponseDTO
from visier_api_data_in.models.tenant_data_uploads_update_response_dto import TenantDataUploadsUpdateResponseDTO
import visier_api_data_in.models


class DataAndJobHandlingApi:
    """
    This class provides methods to make requests to the Visier API.
    It uses the ApiClient to handle the HTTP requests and responses.
    """

    def __init__(self, api_client=None) -> None:
        if api_client is None:
            api_client = ApiClient.get_default()
        self.api_client = api_client


    @validate_call
    def adhoc_consolidated_analytics_job(
        self,
        consolidated_analytics_job_request_dto: ConsolidatedAnalyticsJobRequestDTO,
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
    ) -> JobIdResponse:
        """Run a consolidated analytics job

        Run a job for a consolidated analytics tenant. This request retrieves data for all source tenants in a consolidated analytics tenant. After the job completes, you can run a processing job to generate a data version for the consolidated analytics tenant. To run a processing job, see `POST /v1alpha/op/jobs/processing-jobs`.

        :param consolidated_analytics_job_request_dto: (required)
        :type consolidated_analytics_job_request_dto: ConsolidatedAnalyticsJobRequestDTO
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

        _param = self._adhoc_consolidated_analytics_job_serialize(
            consolidated_analytics_job_request_dto=consolidated_analytics_job_request_dto,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "JobIdResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        ).data


    @validate_call
    def adhoc_consolidated_analytics_job_with_http_info(
        self,
        consolidated_analytics_job_request_dto: ConsolidatedAnalyticsJobRequestDTO,
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
    ) -> ApiResponse[JobIdResponse]:
        """Run a consolidated analytics job

        Run a job for a consolidated analytics tenant. This request retrieves data for all source tenants in a consolidated analytics tenant. After the job completes, you can run a processing job to generate a data version for the consolidated analytics tenant. To run a processing job, see `POST /v1alpha/op/jobs/processing-jobs`.

        :param consolidated_analytics_job_request_dto: (required)
        :type consolidated_analytics_job_request_dto: ConsolidatedAnalyticsJobRequestDTO
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

        _param = self._adhoc_consolidated_analytics_job_serialize(
            consolidated_analytics_job_request_dto=consolidated_analytics_job_request_dto,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "JobIdResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        )


    @validate_call
    def adhoc_consolidated_analytics_job_without_preload_content(
        self,
        consolidated_analytics_job_request_dto: ConsolidatedAnalyticsJobRequestDTO,
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
        """Run a consolidated analytics job

        Run a job for a consolidated analytics tenant. This request retrieves data for all source tenants in a consolidated analytics tenant. After the job completes, you can run a processing job to generate a data version for the consolidated analytics tenant. To run a processing job, see `POST /v1alpha/op/jobs/processing-jobs`.

        :param consolidated_analytics_job_request_dto: (required)
        :type consolidated_analytics_job_request_dto: ConsolidatedAnalyticsJobRequestDTO
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

        _param = self._adhoc_consolidated_analytics_job_serialize(
            consolidated_analytics_job_request_dto=consolidated_analytics_job_request_dto,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "JobIdResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        return response_data.response


    def _adhoc_consolidated_analytics_job_serialize(
        self,
        consolidated_analytics_job_request_dto,
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
        if consolidated_analytics_job_request_dto is not None:
            _body_params = consolidated_analytics_job_request_dto


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
            resource_path='/v1alpha/op/jobs/consolidated-analytics-jobs',
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
    def adhoc_extraction_job(
        self,
        extract_data_and_load_dto: ExtractDataAndLoadDTO,
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
    ) -> JobIdResponse:
        """Run a data connector extraction job

        Run an extraction job to retrieve data through a Visier data connector and generate a new data version. Administrating tenants can run extraction jobs for all analytic tenants, a list of analytic tenants, or the administrating tenant.  If running extraction jobs for an administrating tenant or their analytic tenants, this request starts a dispatching job that generates one extraction job per tenant. The response returns the job ID of the extraction job or dispatching job.

        :param extract_data_and_load_dto: (required)
        :type extract_data_and_load_dto: ExtractDataAndLoadDTO
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

        _param = self._adhoc_extraction_job_serialize(
            extract_data_and_load_dto=extract_data_and_load_dto,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "JobIdResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        ).data


    @validate_call
    def adhoc_extraction_job_with_http_info(
        self,
        extract_data_and_load_dto: ExtractDataAndLoadDTO,
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
    ) -> ApiResponse[JobIdResponse]:
        """Run a data connector extraction job

        Run an extraction job to retrieve data through a Visier data connector and generate a new data version. Administrating tenants can run extraction jobs for all analytic tenants, a list of analytic tenants, or the administrating tenant.  If running extraction jobs for an administrating tenant or their analytic tenants, this request starts a dispatching job that generates one extraction job per tenant. The response returns the job ID of the extraction job or dispatching job.

        :param extract_data_and_load_dto: (required)
        :type extract_data_and_load_dto: ExtractDataAndLoadDTO
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

        _param = self._adhoc_extraction_job_serialize(
            extract_data_and_load_dto=extract_data_and_load_dto,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "JobIdResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        )


    @validate_call
    def adhoc_extraction_job_without_preload_content(
        self,
        extract_data_and_load_dto: ExtractDataAndLoadDTO,
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
        """Run a data connector extraction job

        Run an extraction job to retrieve data through a Visier data connector and generate a new data version. Administrating tenants can run extraction jobs for all analytic tenants, a list of analytic tenants, or the administrating tenant.  If running extraction jobs for an administrating tenant or their analytic tenants, this request starts a dispatching job that generates one extraction job per tenant. The response returns the job ID of the extraction job or dispatching job.

        :param extract_data_and_load_dto: (required)
        :type extract_data_and_load_dto: ExtractDataAndLoadDTO
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

        _param = self._adhoc_extraction_job_serialize(
            extract_data_and_load_dto=extract_data_and_load_dto,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "JobIdResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        return response_data.response


    def _adhoc_extraction_job_serialize(
        self,
        extract_data_and_load_dto,
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
        if extract_data_and_load_dto is not None:
            _body_params = extract_data_and_load_dto


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
            resource_path='/v1alpha/op/jobs/extraction-jobs',
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
    def adhoc_processing_jobs(
        self,
        processing_job_request_dto: ProcessingJobRequestDTO,
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
    ) -> JobIdResponse:
        """Run a processing job

        Run a processing job to generate a new data version. Administrating tenants can run processing jobs for all analytic tenants, a list of analytic tenants, or the administrating tenant.  If running processing jobs for an administrating tenant or their analytic tenants, this request starts a dispatching job that generates one processing job per tenant. The response returns the job ID of the processing job or dispatching job.

        :param processing_job_request_dto: (required)
        :type processing_job_request_dto: ProcessingJobRequestDTO
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

        _param = self._adhoc_processing_jobs_serialize(
            processing_job_request_dto=processing_job_request_dto,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "JobIdResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        ).data


    @validate_call
    def adhoc_processing_jobs_with_http_info(
        self,
        processing_job_request_dto: ProcessingJobRequestDTO,
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
    ) -> ApiResponse[JobIdResponse]:
        """Run a processing job

        Run a processing job to generate a new data version. Administrating tenants can run processing jobs for all analytic tenants, a list of analytic tenants, or the administrating tenant.  If running processing jobs for an administrating tenant or their analytic tenants, this request starts a dispatching job that generates one processing job per tenant. The response returns the job ID of the processing job or dispatching job.

        :param processing_job_request_dto: (required)
        :type processing_job_request_dto: ProcessingJobRequestDTO
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

        _param = self._adhoc_processing_jobs_serialize(
            processing_job_request_dto=processing_job_request_dto,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "JobIdResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        )


    @validate_call
    def adhoc_processing_jobs_without_preload_content(
        self,
        processing_job_request_dto: ProcessingJobRequestDTO,
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
        """Run a processing job

        Run a processing job to generate a new data version. Administrating tenants can run processing jobs for all analytic tenants, a list of analytic tenants, or the administrating tenant.  If running processing jobs for an administrating tenant or their analytic tenants, this request starts a dispatching job that generates one processing job per tenant. The response returns the job ID of the processing job or dispatching job.

        :param processing_job_request_dto: (required)
        :type processing_job_request_dto: ProcessingJobRequestDTO
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

        _param = self._adhoc_processing_jobs_serialize(
            processing_job_request_dto=processing_job_request_dto,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "JobIdResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        return response_data.response


    def _adhoc_processing_jobs_serialize(
        self,
        processing_job_request_dto,
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
        if processing_job_request_dto is not None:
            _body_params = processing_job_request_dto


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
            resource_path='/v1alpha/op/jobs/processing-jobs',
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
    def assign_connector_credential(
        self,
        assign_connector_credential_request: AssignConnectorCredentialRequest,
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
    ) -> AssignConnectorCredentialsResponseDTO:
        """Assign connector credentials to data connectors

        Assign a connector credential to a data connector.

        :param assign_connector_credential_request: (required)
        :type assign_connector_credential_request: AssignConnectorCredentialRequest
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

        _param = self._assign_connector_credential_serialize(
            assign_connector_credential_request=assign_connector_credential_request,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "AssignConnectorCredentialsResponseDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        ).data


    @validate_call
    def assign_connector_credential_with_http_info(
        self,
        assign_connector_credential_request: AssignConnectorCredentialRequest,
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
    ) -> ApiResponse[AssignConnectorCredentialsResponseDTO]:
        """Assign connector credentials to data connectors

        Assign a connector credential to a data connector.

        :param assign_connector_credential_request: (required)
        :type assign_connector_credential_request: AssignConnectorCredentialRequest
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

        _param = self._assign_connector_credential_serialize(
            assign_connector_credential_request=assign_connector_credential_request,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "AssignConnectorCredentialsResponseDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        )


    @validate_call
    def assign_connector_credential_without_preload_content(
        self,
        assign_connector_credential_request: AssignConnectorCredentialRequest,
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
        """Assign connector credentials to data connectors

        Assign a connector credential to a data connector.

        :param assign_connector_credential_request: (required)
        :type assign_connector_credential_request: AssignConnectorCredentialRequest
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

        _param = self._assign_connector_credential_serialize(
            assign_connector_credential_request=assign_connector_credential_request,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "AssignConnectorCredentialsResponseDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        return response_data.response


    def _assign_connector_credential_serialize(
        self,
        assign_connector_credential_request,
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
        if assign_connector_credential_request is not None:
            _body_params = assign_connector_credential_request


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
            resource_path='/v1/op/data-connectors/assignCredentials',
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
    def cancel_jobs(
        self,
        cancel_job_batch_from_job_id_dto: CancelJobBatchFromJobIdDTO,
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
    ) -> JobCancellationResultsDTO:
        """Cancel a list of jobs

        Cancel a list of processing jobs, upload jobs, receiving jobs, and extraction jobs.   **Note:** Receiving jobs with the Running status cannot be cancelled.

        :param cancel_job_batch_from_job_id_dto: (required)
        :type cancel_job_batch_from_job_id_dto: CancelJobBatchFromJobIdDTO
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

        _param = self._cancel_jobs_serialize(
            cancel_job_batch_from_job_id_dto=cancel_job_batch_from_job_id_dto,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "JobCancellationResultsDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        ).data


    @validate_call
    def cancel_jobs_with_http_info(
        self,
        cancel_job_batch_from_job_id_dto: CancelJobBatchFromJobIdDTO,
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
    ) -> ApiResponse[JobCancellationResultsDTO]:
        """Cancel a list of jobs

        Cancel a list of processing jobs, upload jobs, receiving jobs, and extraction jobs.   **Note:** Receiving jobs with the Running status cannot be cancelled.

        :param cancel_job_batch_from_job_id_dto: (required)
        :type cancel_job_batch_from_job_id_dto: CancelJobBatchFromJobIdDTO
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

        _param = self._cancel_jobs_serialize(
            cancel_job_batch_from_job_id_dto=cancel_job_batch_from_job_id_dto,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "JobCancellationResultsDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        )


    @validate_call
    def cancel_jobs_without_preload_content(
        self,
        cancel_job_batch_from_job_id_dto: CancelJobBatchFromJobIdDTO,
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
        """Cancel a list of jobs

        Cancel a list of processing jobs, upload jobs, receiving jobs, and extraction jobs.   **Note:** Receiving jobs with the Running status cannot be cancelled.

        :param cancel_job_batch_from_job_id_dto: (required)
        :type cancel_job_batch_from_job_id_dto: CancelJobBatchFromJobIdDTO
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

        _param = self._cancel_jobs_serialize(
            cancel_job_batch_from_job_id_dto=cancel_job_batch_from_job_id_dto,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "JobCancellationResultsDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        return response_data.response


    def _cancel_jobs_serialize(
        self,
        cancel_job_batch_from_job_id_dto,
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
        if cancel_job_batch_from_job_id_dto is not None:
            _body_params = cancel_job_batch_from_job_id_dto


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
            resource_path='/v1/op/jobs/cancel',
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
    def create_connector_credential(
        self,
        data_provider_auth_information_dto: DataProviderAuthInformationDTO,
        tenant_code: Annotated[Optional[StrictStr], Field(description="The tenant code of a specific analytic tenant that you want to create the credential for.")] = None,
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
    ) -> CredentialCreationAPIResponseDTO:
        """Create a connector credential

        Create credentials for a data connector. Connector credentials allow Visier to retrieve data from your source systems through an integration user in the source system.     In the request body, specify one data provider in the `dataProviderAuthParams` parameter. For example, to create connector credentials for a UKG data connector, your request body might look like the following sample.  ```json  {    model={      \"dataProviderAuthParams\": {         \"provider\": \"UKG\",         \"ultimateAuthParams\": {            \"hostDomainName\": \"exampleHostDomain\",            \"apiKey\": \"apiKey1234\",            \"username\": \"username1234\",            \"password\": \"password1234\",            \"userAccessKey\": \"accessKey1234\"         }      },      \"dataProviderBasicInformation\": {         \"displayName\": \"exampleDisplayName\",         \"description\": \"exampleDescription\"      }  }  ```

        :param data_provider_auth_information_dto: (required)
        :type data_provider_auth_information_dto: DataProviderAuthInformationDTO
        :param tenant_code: The tenant code of a specific analytic tenant that you want to create the credential for.
        :type tenant_code: str
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

        _param = self._create_connector_credential_serialize(
            data_provider_auth_information_dto=data_provider_auth_information_dto,
            tenant_code=tenant_code,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "CredentialCreationAPIResponseDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        ).data


    @validate_call
    def create_connector_credential_with_http_info(
        self,
        data_provider_auth_information_dto: DataProviderAuthInformationDTO,
        tenant_code: Annotated[Optional[StrictStr], Field(description="The tenant code of a specific analytic tenant that you want to create the credential for.")] = None,
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
    ) -> ApiResponse[CredentialCreationAPIResponseDTO]:
        """Create a connector credential

        Create credentials for a data connector. Connector credentials allow Visier to retrieve data from your source systems through an integration user in the source system.     In the request body, specify one data provider in the `dataProviderAuthParams` parameter. For example, to create connector credentials for a UKG data connector, your request body might look like the following sample.  ```json  {    model={      \"dataProviderAuthParams\": {         \"provider\": \"UKG\",         \"ultimateAuthParams\": {            \"hostDomainName\": \"exampleHostDomain\",            \"apiKey\": \"apiKey1234\",            \"username\": \"username1234\",            \"password\": \"password1234\",            \"userAccessKey\": \"accessKey1234\"         }      },      \"dataProviderBasicInformation\": {         \"displayName\": \"exampleDisplayName\",         \"description\": \"exampleDescription\"      }  }  ```

        :param data_provider_auth_information_dto: (required)
        :type data_provider_auth_information_dto: DataProviderAuthInformationDTO
        :param tenant_code: The tenant code of a specific analytic tenant that you want to create the credential for.
        :type tenant_code: str
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

        _param = self._create_connector_credential_serialize(
            data_provider_auth_information_dto=data_provider_auth_information_dto,
            tenant_code=tenant_code,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "CredentialCreationAPIResponseDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        )


    @validate_call
    def create_connector_credential_without_preload_content(
        self,
        data_provider_auth_information_dto: DataProviderAuthInformationDTO,
        tenant_code: Annotated[Optional[StrictStr], Field(description="The tenant code of a specific analytic tenant that you want to create the credential for.")] = None,
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
        """Create a connector credential

        Create credentials for a data connector. Connector credentials allow Visier to retrieve data from your source systems through an integration user in the source system.     In the request body, specify one data provider in the `dataProviderAuthParams` parameter. For example, to create connector credentials for a UKG data connector, your request body might look like the following sample.  ```json  {    model={      \"dataProviderAuthParams\": {         \"provider\": \"UKG\",         \"ultimateAuthParams\": {            \"hostDomainName\": \"exampleHostDomain\",            \"apiKey\": \"apiKey1234\",            \"username\": \"username1234\",            \"password\": \"password1234\",            \"userAccessKey\": \"accessKey1234\"         }      },      \"dataProviderBasicInformation\": {         \"displayName\": \"exampleDisplayName\",         \"description\": \"exampleDescription\"      }  }  ```

        :param data_provider_auth_information_dto: (required)
        :type data_provider_auth_information_dto: DataProviderAuthInformationDTO
        :param tenant_code: The tenant code of a specific analytic tenant that you want to create the credential for.
        :type tenant_code: str
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

        _param = self._create_connector_credential_serialize(
            data_provider_auth_information_dto=data_provider_auth_information_dto,
            tenant_code=tenant_code,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "CredentialCreationAPIResponseDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        return response_data.response


    def _create_connector_credential_serialize(
        self,
        data_provider_auth_information_dto,
        tenant_code,
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
        if tenant_code is not None:
            
            _query_params.append(('tenantCode', tenant_code))
            
        # process the header parameters
        if target_tenant_id is not None:
            _header_params['TargetTenantID'] = target_tenant_id
        # process the form parameters
        # process the body parameter
        if data_provider_auth_information_dto is not None:
            _body_params = data_provider_auth_information_dto


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
            resource_path='/v1/op/data-connector-credentials',
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
    def data_connector_credentials(
        self,
        tenant_code: Annotated[Optional[StrictStr], Field(description="The tenant code of a specific analytic tenant that you want to retrieve for.")] = None,
        limit: Annotated[Optional[StrictInt], Field(description="The limit to retrieve.")] = None,
        start: Annotated[Optional[StrictInt], Field(description="The index to start retrieving results from, also known as offset. The index begins at 0.")] = None,
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
    ) -> ExtractorCredentialsAPIDTO:
        """Retrieve a list of all data connector credentials

        Retrieve a list of the connector credentials in a specified tenant. Connector credentials allow  Visier to retrieve data from your source systems through an integration user in the source system.

        :param tenant_code: The tenant code of a specific analytic tenant that you want to retrieve for.
        :type tenant_code: str
        :param limit: The limit to retrieve.
        :type limit: int
        :param start: The index to start retrieving results from, also known as offset. The index begins at 0.
        :type start: int
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

        _param = self._data_connector_credentials_serialize(
            tenant_code=tenant_code,
            limit=limit,
            start=start,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "ExtractorCredentialsAPIDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        ).data


    @validate_call
    def data_connector_credentials_with_http_info(
        self,
        tenant_code: Annotated[Optional[StrictStr], Field(description="The tenant code of a specific analytic tenant that you want to retrieve for.")] = None,
        limit: Annotated[Optional[StrictInt], Field(description="The limit to retrieve.")] = None,
        start: Annotated[Optional[StrictInt], Field(description="The index to start retrieving results from, also known as offset. The index begins at 0.")] = None,
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
    ) -> ApiResponse[ExtractorCredentialsAPIDTO]:
        """Retrieve a list of all data connector credentials

        Retrieve a list of the connector credentials in a specified tenant. Connector credentials allow  Visier to retrieve data from your source systems through an integration user in the source system.

        :param tenant_code: The tenant code of a specific analytic tenant that you want to retrieve for.
        :type tenant_code: str
        :param limit: The limit to retrieve.
        :type limit: int
        :param start: The index to start retrieving results from, also known as offset. The index begins at 0.
        :type start: int
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

        _param = self._data_connector_credentials_serialize(
            tenant_code=tenant_code,
            limit=limit,
            start=start,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "ExtractorCredentialsAPIDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        )


    @validate_call
    def data_connector_credentials_without_preload_content(
        self,
        tenant_code: Annotated[Optional[StrictStr], Field(description="The tenant code of a specific analytic tenant that you want to retrieve for.")] = None,
        limit: Annotated[Optional[StrictInt], Field(description="The limit to retrieve.")] = None,
        start: Annotated[Optional[StrictInt], Field(description="The index to start retrieving results from, also known as offset. The index begins at 0.")] = None,
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
        """Retrieve a list of all data connector credentials

        Retrieve a list of the connector credentials in a specified tenant. Connector credentials allow  Visier to retrieve data from your source systems through an integration user in the source system.

        :param tenant_code: The tenant code of a specific analytic tenant that you want to retrieve for.
        :type tenant_code: str
        :param limit: The limit to retrieve.
        :type limit: int
        :param start: The index to start retrieving results from, also known as offset. The index begins at 0.
        :type start: int
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

        _param = self._data_connector_credentials_serialize(
            tenant_code=tenant_code,
            limit=limit,
            start=start,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "ExtractorCredentialsAPIDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        return response_data.response


    def _data_connector_credentials_serialize(
        self,
        tenant_code,
        limit,
        start,
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
        if tenant_code is not None:
            
            _query_params.append(('tenantCode', tenant_code))
            
        if limit is not None:
            
            _query_params.append(('limit', limit))
            
        if start is not None:
            
            _query_params.append(('start', start))
            
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
            resource_path='/v1/op/data-connector-credentials',
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
    def data_connectors(
        self,
        tenant_code: Annotated[Optional[StrictStr], Field(description="The tenant code of a specific analytic tenant that you want to retrieve for.")] = None,
        limit: Annotated[Optional[StrictInt], Field(description="The limit to retrieve.")] = None,
        start: Annotated[Optional[StrictInt], Field(description="The index to start retrieving results from, also known as offset. The index begins at 0.")] = None,
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
    ) -> ImportDefinitionsAPIDTO:
        """Retrieve a list of all data connectors

        Retrieve a list of the data connectors in a specified tenant. Data connectors are an alternative  to generating flat files and transferring them to Visier via SFTP.

        :param tenant_code: The tenant code of a specific analytic tenant that you want to retrieve for.
        :type tenant_code: str
        :param limit: The limit to retrieve.
        :type limit: int
        :param start: The index to start retrieving results from, also known as offset. The index begins at 0.
        :type start: int
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

        _param = self._data_connectors_serialize(
            tenant_code=tenant_code,
            limit=limit,
            start=start,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "ImportDefinitionsAPIDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        ).data


    @validate_call
    def data_connectors_with_http_info(
        self,
        tenant_code: Annotated[Optional[StrictStr], Field(description="The tenant code of a specific analytic tenant that you want to retrieve for.")] = None,
        limit: Annotated[Optional[StrictInt], Field(description="The limit to retrieve.")] = None,
        start: Annotated[Optional[StrictInt], Field(description="The index to start retrieving results from, also known as offset. The index begins at 0.")] = None,
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
    ) -> ApiResponse[ImportDefinitionsAPIDTO]:
        """Retrieve a list of all data connectors

        Retrieve a list of the data connectors in a specified tenant. Data connectors are an alternative  to generating flat files and transferring them to Visier via SFTP.

        :param tenant_code: The tenant code of a specific analytic tenant that you want to retrieve for.
        :type tenant_code: str
        :param limit: The limit to retrieve.
        :type limit: int
        :param start: The index to start retrieving results from, also known as offset. The index begins at 0.
        :type start: int
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

        _param = self._data_connectors_serialize(
            tenant_code=tenant_code,
            limit=limit,
            start=start,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "ImportDefinitionsAPIDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        )


    @validate_call
    def data_connectors_without_preload_content(
        self,
        tenant_code: Annotated[Optional[StrictStr], Field(description="The tenant code of a specific analytic tenant that you want to retrieve for.")] = None,
        limit: Annotated[Optional[StrictInt], Field(description="The limit to retrieve.")] = None,
        start: Annotated[Optional[StrictInt], Field(description="The index to start retrieving results from, also known as offset. The index begins at 0.")] = None,
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
        """Retrieve a list of all data connectors

        Retrieve a list of the data connectors in a specified tenant. Data connectors are an alternative  to generating flat files and transferring them to Visier via SFTP.

        :param tenant_code: The tenant code of a specific analytic tenant that you want to retrieve for.
        :type tenant_code: str
        :param limit: The limit to retrieve.
        :type limit: int
        :param start: The index to start retrieving results from, also known as offset. The index begins at 0.
        :type start: int
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

        _param = self._data_connectors_serialize(
            tenant_code=tenant_code,
            limit=limit,
            start=start,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "ImportDefinitionsAPIDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        return response_data.response


    def _data_connectors_serialize(
        self,
        tenant_code,
        limit,
        start,
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
        if tenant_code is not None:
            
            _query_params.append(('tenantCode', tenant_code))
            
        if limit is not None:
            
            _query_params.append(('limit', limit))
            
        if start is not None:
            
            _query_params.append(('start', start))
            
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
            resource_path='/v1/op/data-connectors',
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
    def delete_connector_credential(
        self,
        id: Annotated[StrictStr, Field(description="The credentialId of the credential you want to delete.")],
        tenant_code: Annotated[Optional[StrictStr], Field(description="The tenant code of the analytic tenant in which the credential you're deleting.")] = None,
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
    ) -> str:
        """Delete a connector credential

        Use this API to delete connector credentials from your tenants. Credentials that are no longer valid  should be deleted.

        :param id: The credentialId of the credential you want to delete. (required)
        :type id: str
        :param tenant_code: The tenant code of the analytic tenant in which the credential you're deleting.
        :type tenant_code: str
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

        _param = self._delete_connector_credential_serialize(
            id=id,
            tenant_code=tenant_code,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "str",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        ).data


    @validate_call
    def delete_connector_credential_with_http_info(
        self,
        id: Annotated[StrictStr, Field(description="The credentialId of the credential you want to delete.")],
        tenant_code: Annotated[Optional[StrictStr], Field(description="The tenant code of the analytic tenant in which the credential you're deleting.")] = None,
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
    ) -> ApiResponse[str]:
        """Delete a connector credential

        Use this API to delete connector credentials from your tenants. Credentials that are no longer valid  should be deleted.

        :param id: The credentialId of the credential you want to delete. (required)
        :type id: str
        :param tenant_code: The tenant code of the analytic tenant in which the credential you're deleting.
        :type tenant_code: str
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

        _param = self._delete_connector_credential_serialize(
            id=id,
            tenant_code=tenant_code,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "str",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        )


    @validate_call
    def delete_connector_credential_without_preload_content(
        self,
        id: Annotated[StrictStr, Field(description="The credentialId of the credential you want to delete.")],
        tenant_code: Annotated[Optional[StrictStr], Field(description="The tenant code of the analytic tenant in which the credential you're deleting.")] = None,
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
        """Delete a connector credential

        Use this API to delete connector credentials from your tenants. Credentials that are no longer valid  should be deleted.

        :param id: The credentialId of the credential you want to delete. (required)
        :type id: str
        :param tenant_code: The tenant code of the analytic tenant in which the credential you're deleting.
        :type tenant_code: str
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

        _param = self._delete_connector_credential_serialize(
            id=id,
            tenant_code=tenant_code,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "str",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        return response_data.response


    def _delete_connector_credential_serialize(
        self,
        id,
        tenant_code,
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
        if id is not None:
            _path_params['id'] = id
        # process the query parameters
        if tenant_code is not None:
            
            _query_params.append(('tenantCode', tenant_code))
            
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
            method='DELETE',
            resource_path='/v1/op/data-connector-credentials/{id}',
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
    def disable_dv(
        self,
        disable_dv_request: DisableDVRequest,
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
    ) -> DisableDVResponse:
        """Disable data versions for a list of analytic tenants

        If you discover that a data version is not what is expected after running metric value validation on a data load,  you may want to disable the data version for that processing job.   Disable the latest enabled data versions for affected analytic tenants or to disable a particular  data version for each analytic tenant.   **Note:** Disabling an older data version may not have an effect on the state of the solution.

        :param disable_dv_request: (required)
        :type disable_dv_request: DisableDVRequest
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

        _param = self._disable_dv_serialize(
            disable_dv_request=disable_dv_request,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "DisableDVResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        ).data


    @validate_call
    def disable_dv_with_http_info(
        self,
        disable_dv_request: DisableDVRequest,
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
    ) -> ApiResponse[DisableDVResponse]:
        """Disable data versions for a list of analytic tenants

        If you discover that a data version is not what is expected after running metric value validation on a data load,  you may want to disable the data version for that processing job.   Disable the latest enabled data versions for affected analytic tenants or to disable a particular  data version for each analytic tenant.   **Note:** Disabling an older data version may not have an effect on the state of the solution.

        :param disable_dv_request: (required)
        :type disable_dv_request: DisableDVRequest
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

        _param = self._disable_dv_serialize(
            disable_dv_request=disable_dv_request,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "DisableDVResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        )


    @validate_call
    def disable_dv_without_preload_content(
        self,
        disable_dv_request: DisableDVRequest,
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
        """Disable data versions for a list of analytic tenants

        If you discover that a data version is not what is expected after running metric value validation on a data load,  you may want to disable the data version for that processing job.   Disable the latest enabled data versions for affected analytic tenants or to disable a particular  data version for each analytic tenant.   **Note:** Disabling an older data version may not have an effect on the state of the solution.

        :param disable_dv_request: (required)
        :type disable_dv_request: DisableDVRequest
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

        _param = self._disable_dv_serialize(
            disable_dv_request=disable_dv_request,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "DisableDVResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        return response_data.response


    def _disable_dv_serialize(
        self,
        disable_dv_request,
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
        if disable_dv_request is not None:
            _body_params = disable_dv_request


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
            method='PUT',
            resource_path='/v1/op/data-versions/disable',
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
    def dispatching_job_status(
        self,
        job_id: Annotated[StrictStr, Field(description="The ID of the job you want to retrieve.")],
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
    ) -> DispatchingJobStatusResponse:
        """Retrieve a dispatching job's status

        Retrieve the status of a dispatching job, including its job ID and the number of jobs it generated.

        :param job_id: The ID of the job you want to retrieve. (required)
        :type job_id: str
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

        _param = self._dispatching_job_status_serialize(
            job_id=job_id,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "DispatchingJobStatusResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        ).data


    @validate_call
    def dispatching_job_status_with_http_info(
        self,
        job_id: Annotated[StrictStr, Field(description="The ID of the job you want to retrieve.")],
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
    ) -> ApiResponse[DispatchingJobStatusResponse]:
        """Retrieve a dispatching job's status

        Retrieve the status of a dispatching job, including its job ID and the number of jobs it generated.

        :param job_id: The ID of the job you want to retrieve. (required)
        :type job_id: str
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

        _param = self._dispatching_job_status_serialize(
            job_id=job_id,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "DispatchingJobStatusResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        )


    @validate_call
    def dispatching_job_status_without_preload_content(
        self,
        job_id: Annotated[StrictStr, Field(description="The ID of the job you want to retrieve.")],
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
        """Retrieve a dispatching job's status

        Retrieve the status of a dispatching job, including its job ID and the number of jobs it generated.

        :param job_id: The ID of the job you want to retrieve. (required)
        :type job_id: str
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

        _param = self._dispatching_job_status_serialize(
            job_id=job_id,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "DispatchingJobStatusResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        return response_data.response


    def _dispatching_job_status_serialize(
        self,
        job_id,
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
        if job_id is not None:
            _path_params['jobId'] = job_id
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
            resource_path='/v1/op/jobs/dispatching-jobs/{jobId}',
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
    def exclude_data_uplaods(
        self,
        exclude_data_uploads_request: ExcludeDataUploadsRequest,
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
    ) -> TenantDataUploadsUpdateResponseDTO:
        """Exclude data uploads

        Exclude either a specified list of data uploads or all data uploads for each analytic tenant.

        :param exclude_data_uploads_request: (required)
        :type exclude_data_uploads_request: ExcludeDataUploadsRequest
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

        _param = self._exclude_data_uplaods_serialize(
            exclude_data_uploads_request=exclude_data_uploads_request,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "TenantDataUploadsUpdateResponseDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        ).data


    @validate_call
    def exclude_data_uplaods_with_http_info(
        self,
        exclude_data_uploads_request: ExcludeDataUploadsRequest,
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
    ) -> ApiResponse[TenantDataUploadsUpdateResponseDTO]:
        """Exclude data uploads

        Exclude either a specified list of data uploads or all data uploads for each analytic tenant.

        :param exclude_data_uploads_request: (required)
        :type exclude_data_uploads_request: ExcludeDataUploadsRequest
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

        _param = self._exclude_data_uplaods_serialize(
            exclude_data_uploads_request=exclude_data_uploads_request,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "TenantDataUploadsUpdateResponseDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        )


    @validate_call
    def exclude_data_uplaods_without_preload_content(
        self,
        exclude_data_uploads_request: ExcludeDataUploadsRequest,
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
        """Exclude data uploads

        Exclude either a specified list of data uploads or all data uploads for each analytic tenant.

        :param exclude_data_uploads_request: (required)
        :type exclude_data_uploads_request: ExcludeDataUploadsRequest
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

        _param = self._exclude_data_uplaods_serialize(
            exclude_data_uploads_request=exclude_data_uploads_request,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "TenantDataUploadsUpdateResponseDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        return response_data.response


    def _exclude_data_uplaods_serialize(
        self,
        exclude_data_uploads_request,
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
        if exclude_data_uploads_request is not None:
            _body_params = exclude_data_uploads_request


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
            method='PUT',
            resource_path='/v1/op/data/uploads/exclude',
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
    def extraction_job_and_status(
        self,
        job_id: Annotated[StrictStr, Field(description="The ID of the dispatching job you want to retrieve.")],
        dispatching_job_id: Annotated[Optional[StrictStr], Field(description="The ID of the dispatching job that generated the extraction jobs.")] = None,
        tenant_code: Annotated[Optional[StrictStr], Field(description="The tenant code of a specific analytic tenant that you want to retrieve the extraction job status for.  Use this if you are only interested in the results for one analytic tenant.")] = None,
        limit: Annotated[Optional[StrictInt], Field(description="The limit of extraction job statuses to retrieve.")] = None,
        start: Annotated[Optional[StrictInt], Field(description="The index to start retrieving results from, also known as offset. The index begins at 0.")] = None,
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
    ) -> ExtractionJobAndStatusResponse:
        """Retrieve a dispatching job's extraction jobs with their statuses

        Retrieve the statuses of extraction jobs associated with a dispatching job. The dispatching job  is a \"parent\" to extraction jobs, which retrieve data from your source systems through data connectors.

        :param job_id: The ID of the dispatching job you want to retrieve. (required)
        :type job_id: str
        :param dispatching_job_id: The ID of the dispatching job that generated the extraction jobs.
        :type dispatching_job_id: str
        :param tenant_code: The tenant code of a specific analytic tenant that you want to retrieve the extraction job status for.  Use this if you are only interested in the results for one analytic tenant.
        :type tenant_code: str
        :param limit: The limit of extraction job statuses to retrieve.
        :type limit: int
        :param start: The index to start retrieving results from, also known as offset. The index begins at 0.
        :type start: int
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

        _param = self._extraction_job_and_status_serialize(
            job_id=job_id,
            dispatching_job_id=dispatching_job_id,
            tenant_code=tenant_code,
            limit=limit,
            start=start,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "ExtractionJobAndStatusResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        ).data


    @validate_call
    def extraction_job_and_status_with_http_info(
        self,
        job_id: Annotated[StrictStr, Field(description="The ID of the dispatching job you want to retrieve.")],
        dispatching_job_id: Annotated[Optional[StrictStr], Field(description="The ID of the dispatching job that generated the extraction jobs.")] = None,
        tenant_code: Annotated[Optional[StrictStr], Field(description="The tenant code of a specific analytic tenant that you want to retrieve the extraction job status for.  Use this if you are only interested in the results for one analytic tenant.")] = None,
        limit: Annotated[Optional[StrictInt], Field(description="The limit of extraction job statuses to retrieve.")] = None,
        start: Annotated[Optional[StrictInt], Field(description="The index to start retrieving results from, also known as offset. The index begins at 0.")] = None,
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
    ) -> ApiResponse[ExtractionJobAndStatusResponse]:
        """Retrieve a dispatching job's extraction jobs with their statuses

        Retrieve the statuses of extraction jobs associated with a dispatching job. The dispatching job  is a \"parent\" to extraction jobs, which retrieve data from your source systems through data connectors.

        :param job_id: The ID of the dispatching job you want to retrieve. (required)
        :type job_id: str
        :param dispatching_job_id: The ID of the dispatching job that generated the extraction jobs.
        :type dispatching_job_id: str
        :param tenant_code: The tenant code of a specific analytic tenant that you want to retrieve the extraction job status for.  Use this if you are only interested in the results for one analytic tenant.
        :type tenant_code: str
        :param limit: The limit of extraction job statuses to retrieve.
        :type limit: int
        :param start: The index to start retrieving results from, also known as offset. The index begins at 0.
        :type start: int
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

        _param = self._extraction_job_and_status_serialize(
            job_id=job_id,
            dispatching_job_id=dispatching_job_id,
            tenant_code=tenant_code,
            limit=limit,
            start=start,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "ExtractionJobAndStatusResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        )


    @validate_call
    def extraction_job_and_status_without_preload_content(
        self,
        job_id: Annotated[StrictStr, Field(description="The ID of the dispatching job you want to retrieve.")],
        dispatching_job_id: Annotated[Optional[StrictStr], Field(description="The ID of the dispatching job that generated the extraction jobs.")] = None,
        tenant_code: Annotated[Optional[StrictStr], Field(description="The tenant code of a specific analytic tenant that you want to retrieve the extraction job status for.  Use this if you are only interested in the results for one analytic tenant.")] = None,
        limit: Annotated[Optional[StrictInt], Field(description="The limit of extraction job statuses to retrieve.")] = None,
        start: Annotated[Optional[StrictInt], Field(description="The index to start retrieving results from, also known as offset. The index begins at 0.")] = None,
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
        """Retrieve a dispatching job's extraction jobs with their statuses

        Retrieve the statuses of extraction jobs associated with a dispatching job. The dispatching job  is a \"parent\" to extraction jobs, which retrieve data from your source systems through data connectors.

        :param job_id: The ID of the dispatching job you want to retrieve. (required)
        :type job_id: str
        :param dispatching_job_id: The ID of the dispatching job that generated the extraction jobs.
        :type dispatching_job_id: str
        :param tenant_code: The tenant code of a specific analytic tenant that you want to retrieve the extraction job status for.  Use this if you are only interested in the results for one analytic tenant.
        :type tenant_code: str
        :param limit: The limit of extraction job statuses to retrieve.
        :type limit: int
        :param start: The index to start retrieving results from, also known as offset. The index begins at 0.
        :type start: int
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

        _param = self._extraction_job_and_status_serialize(
            job_id=job_id,
            dispatching_job_id=dispatching_job_id,
            tenant_code=tenant_code,
            limit=limit,
            start=start,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "ExtractionJobAndStatusResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        return response_data.response


    def _extraction_job_and_status_serialize(
        self,
        job_id,
        dispatching_job_id,
        tenant_code,
        limit,
        start,
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
        if job_id is not None:
            _path_params['jobId'] = job_id
        # process the query parameters
        if dispatching_job_id is not None:
            
            _query_params.append(('dispatchingJobId', dispatching_job_id))
            
        if tenant_code is not None:
            
            _query_params.append(('tenantCode', tenant_code))
            
        if limit is not None:
            
            _query_params.append(('limit', limit))
            
        if start is not None:
            
            _query_params.append(('start', start))
            
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
            resource_path='/v1/op/jobs/dispatching-jobs/{jobId}/extraction-jobs',
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
    def include_data_uploads(
        self,
        include_data_uploads_request: IncludeDataUploadsRequest,
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
    ) -> TenantDataUploadsUpdateResponseDTO:
        """Include data uploads

        Include either the specified list of data uploads or all data uploads for each analytic tenant.

        :param include_data_uploads_request: (required)
        :type include_data_uploads_request: IncludeDataUploadsRequest
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

        _param = self._include_data_uploads_serialize(
            include_data_uploads_request=include_data_uploads_request,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "TenantDataUploadsUpdateResponseDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        ).data


    @validate_call
    def include_data_uploads_with_http_info(
        self,
        include_data_uploads_request: IncludeDataUploadsRequest,
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
    ) -> ApiResponse[TenantDataUploadsUpdateResponseDTO]:
        """Include data uploads

        Include either the specified list of data uploads or all data uploads for each analytic tenant.

        :param include_data_uploads_request: (required)
        :type include_data_uploads_request: IncludeDataUploadsRequest
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

        _param = self._include_data_uploads_serialize(
            include_data_uploads_request=include_data_uploads_request,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "TenantDataUploadsUpdateResponseDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        )


    @validate_call
    def include_data_uploads_without_preload_content(
        self,
        include_data_uploads_request: IncludeDataUploadsRequest,
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
        """Include data uploads

        Include either the specified list of data uploads or all data uploads for each analytic tenant.

        :param include_data_uploads_request: (required)
        :type include_data_uploads_request: IncludeDataUploadsRequest
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

        _param = self._include_data_uploads_serialize(
            include_data_uploads_request=include_data_uploads_request,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "TenantDataUploadsUpdateResponseDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        return response_data.response


    def _include_data_uploads_serialize(
        self,
        include_data_uploads_request,
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
        if include_data_uploads_request is not None:
            _body_params = include_data_uploads_request


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
            method='PUT',
            resource_path='/v1/op/data/uploads/include',
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
    def job_id_status(
        self,
        job_id: Annotated[StrictStr, Field(description="The unique ID of the job to retrieve the status for.")],
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
    ) -> ReceivingJobStatusResponse:
        """Retrieve a specific job's status

        Use this API to retrieve the list of statuses for a specific job with id `jobId`. You can retrieve all job statuses or specify a time period to retrieve statuses from.

        :param job_id: The unique ID of the job to retrieve the status for. (required)
        :type job_id: str
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

        _param = self._job_id_status_serialize(
            job_id=job_id,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "ReceivingJobStatusResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        ).data


    @validate_call
    def job_id_status_with_http_info(
        self,
        job_id: Annotated[StrictStr, Field(description="The unique ID of the job to retrieve the status for.")],
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
    ) -> ApiResponse[ReceivingJobStatusResponse]:
        """Retrieve a specific job's status

        Use this API to retrieve the list of statuses for a specific job with id `jobId`. You can retrieve all job statuses or specify a time period to retrieve statuses from.

        :param job_id: The unique ID of the job to retrieve the status for. (required)
        :type job_id: str
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

        _param = self._job_id_status_serialize(
            job_id=job_id,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "ReceivingJobStatusResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        )


    @validate_call
    def job_id_status_without_preload_content(
        self,
        job_id: Annotated[StrictStr, Field(description="The unique ID of the job to retrieve the status for.")],
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
        """Retrieve a specific job's status

        Use this API to retrieve the list of statuses for a specific job with id `jobId`. You can retrieve all job statuses or specify a time period to retrieve statuses from.

        :param job_id: The unique ID of the job to retrieve the status for. (required)
        :type job_id: str
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

        _param = self._job_id_status_serialize(
            job_id=job_id,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "ReceivingJobStatusResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        return response_data.response


    def _job_id_status_serialize(
        self,
        job_id,
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
        if job_id is not None:
            _path_params['jobId'] = job_id
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
            resource_path='/v1/op/job-status/jobs/{jobId}',
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
    def job_status(
        self,
        start_time: Annotated[Optional[StrictStr], Field(description="The start time from which to retrieve job statuses.")] = None,
        end_time: Annotated[Optional[StrictStr], Field(description="The end time from which to retrieve job statuses.")] = None,
        status: Annotated[Optional[StrictStr], Field(description="The specific status to restrict the list of jobs to.")] = None,
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
    ) -> JobStatusListResponse:
        """Retrieve the statuses of all jobs

        Retrieve the list of statuses for all jobs.

        :param start_time: The start time from which to retrieve job statuses.
        :type start_time: str
        :param end_time: The end time from which to retrieve job statuses.
        :type end_time: str
        :param status: The specific status to restrict the list of jobs to.
        :type status: str
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

        _param = self._job_status_serialize(
            start_time=start_time,
            end_time=end_time,
            status=status,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "JobStatusListResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        ).data


    @validate_call
    def job_status_with_http_info(
        self,
        start_time: Annotated[Optional[StrictStr], Field(description="The start time from which to retrieve job statuses.")] = None,
        end_time: Annotated[Optional[StrictStr], Field(description="The end time from which to retrieve job statuses.")] = None,
        status: Annotated[Optional[StrictStr], Field(description="The specific status to restrict the list of jobs to.")] = None,
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
    ) -> ApiResponse[JobStatusListResponse]:
        """Retrieve the statuses of all jobs

        Retrieve the list of statuses for all jobs.

        :param start_time: The start time from which to retrieve job statuses.
        :type start_time: str
        :param end_time: The end time from which to retrieve job statuses.
        :type end_time: str
        :param status: The specific status to restrict the list of jobs to.
        :type status: str
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

        _param = self._job_status_serialize(
            start_time=start_time,
            end_time=end_time,
            status=status,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "JobStatusListResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        )


    @validate_call
    def job_status_without_preload_content(
        self,
        start_time: Annotated[Optional[StrictStr], Field(description="The start time from which to retrieve job statuses.")] = None,
        end_time: Annotated[Optional[StrictStr], Field(description="The end time from which to retrieve job statuses.")] = None,
        status: Annotated[Optional[StrictStr], Field(description="The specific status to restrict the list of jobs to.")] = None,
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
        """Retrieve the statuses of all jobs

        Retrieve the list of statuses for all jobs.

        :param start_time: The start time from which to retrieve job statuses.
        :type start_time: str
        :param end_time: The end time from which to retrieve job statuses.
        :type end_time: str
        :param status: The specific status to restrict the list of jobs to.
        :type status: str
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

        _param = self._job_status_serialize(
            start_time=start_time,
            end_time=end_time,
            status=status,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "JobStatusListResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        return response_data.response


    def _job_status_serialize(
        self,
        start_time,
        end_time,
        status,
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
        if start_time is not None:
            
            _query_params.append(('startTime', start_time))
            
        if end_time is not None:
            
            _query_params.append(('endTime', end_time))
            
        if status is not None:
            
            _query_params.append(('status', status))
            
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
            resource_path='/v1/op/job-status/jobs',
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
    def latest_enabled_dv(
        self,
        tenant_code: Annotated[Optional[StrictStr], Field(description="The tenant code of a specific analytic tenant that you want to retrieve data versions for.  Use this if you are only interested in the results for one analytic tenant.")] = None,
        limit: Annotated[Optional[StrictInt], Field(description="The limit of analytic tenants to retrieve data versions for.  This parameter is not used if the tenantCode parameter is specified.")] = None,
        start: Annotated[Optional[StrictInt], Field(description="The index to start retrieving results from, also known as offset. The index begins at 0.")] = None,
        number_of_versions: Annotated[Optional[StrictInt], Field(description="The number of latest enabled data versions to retrieve. The maximum value is 5.")] = None,
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
    ) -> MultipleTenantDataVersionsListDTO:
        """Retrieve the latest enabled data versions for all analytic tenants

        If you discover any inconsistencies after running metric value validation, you may want to find the data versions  causing inconsistencies so you can later disable them.   Retrieve up to five (5) of the latest enabled data versions for all your analytic tenants or a  single specified analytic tenant.

        :param tenant_code: The tenant code of a specific analytic tenant that you want to retrieve data versions for.  Use this if you are only interested in the results for one analytic tenant.
        :type tenant_code: str
        :param limit: The limit of analytic tenants to retrieve data versions for.  This parameter is not used if the tenantCode parameter is specified.
        :type limit: int
        :param start: The index to start retrieving results from, also known as offset. The index begins at 0.
        :type start: int
        :param number_of_versions: The number of latest enabled data versions to retrieve. The maximum value is 5.
        :type number_of_versions: int
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

        _param = self._latest_enabled_dv_serialize(
            tenant_code=tenant_code,
            limit=limit,
            start=start,
            number_of_versions=number_of_versions,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "MultipleTenantDataVersionsListDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        ).data


    @validate_call
    def latest_enabled_dv_with_http_info(
        self,
        tenant_code: Annotated[Optional[StrictStr], Field(description="The tenant code of a specific analytic tenant that you want to retrieve data versions for.  Use this if you are only interested in the results for one analytic tenant.")] = None,
        limit: Annotated[Optional[StrictInt], Field(description="The limit of analytic tenants to retrieve data versions for.  This parameter is not used if the tenantCode parameter is specified.")] = None,
        start: Annotated[Optional[StrictInt], Field(description="The index to start retrieving results from, also known as offset. The index begins at 0.")] = None,
        number_of_versions: Annotated[Optional[StrictInt], Field(description="The number of latest enabled data versions to retrieve. The maximum value is 5.")] = None,
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
    ) -> ApiResponse[MultipleTenantDataVersionsListDTO]:
        """Retrieve the latest enabled data versions for all analytic tenants

        If you discover any inconsistencies after running metric value validation, you may want to find the data versions  causing inconsistencies so you can later disable them.   Retrieve up to five (5) of the latest enabled data versions for all your analytic tenants or a  single specified analytic tenant.

        :param tenant_code: The tenant code of a specific analytic tenant that you want to retrieve data versions for.  Use this if you are only interested in the results for one analytic tenant.
        :type tenant_code: str
        :param limit: The limit of analytic tenants to retrieve data versions for.  This parameter is not used if the tenantCode parameter is specified.
        :type limit: int
        :param start: The index to start retrieving results from, also known as offset. The index begins at 0.
        :type start: int
        :param number_of_versions: The number of latest enabled data versions to retrieve. The maximum value is 5.
        :type number_of_versions: int
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

        _param = self._latest_enabled_dv_serialize(
            tenant_code=tenant_code,
            limit=limit,
            start=start,
            number_of_versions=number_of_versions,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "MultipleTenantDataVersionsListDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        )


    @validate_call
    def latest_enabled_dv_without_preload_content(
        self,
        tenant_code: Annotated[Optional[StrictStr], Field(description="The tenant code of a specific analytic tenant that you want to retrieve data versions for.  Use this if you are only interested in the results for one analytic tenant.")] = None,
        limit: Annotated[Optional[StrictInt], Field(description="The limit of analytic tenants to retrieve data versions for.  This parameter is not used if the tenantCode parameter is specified.")] = None,
        start: Annotated[Optional[StrictInt], Field(description="The index to start retrieving results from, also known as offset. The index begins at 0.")] = None,
        number_of_versions: Annotated[Optional[StrictInt], Field(description="The number of latest enabled data versions to retrieve. The maximum value is 5.")] = None,
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
        """Retrieve the latest enabled data versions for all analytic tenants

        If you discover any inconsistencies after running metric value validation, you may want to find the data versions  causing inconsistencies so you can later disable them.   Retrieve up to five (5) of the latest enabled data versions for all your analytic tenants or a  single specified analytic tenant.

        :param tenant_code: The tenant code of a specific analytic tenant that you want to retrieve data versions for.  Use this if you are only interested in the results for one analytic tenant.
        :type tenant_code: str
        :param limit: The limit of analytic tenants to retrieve data versions for.  This parameter is not used if the tenantCode parameter is specified.
        :type limit: int
        :param start: The index to start retrieving results from, also known as offset. The index begins at 0.
        :type start: int
        :param number_of_versions: The number of latest enabled data versions to retrieve. The maximum value is 5.
        :type number_of_versions: int
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

        _param = self._latest_enabled_dv_serialize(
            tenant_code=tenant_code,
            limit=limit,
            start=start,
            number_of_versions=number_of_versions,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "MultipleTenantDataVersionsListDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        return response_data.response


    def _latest_enabled_dv_serialize(
        self,
        tenant_code,
        limit,
        start,
        number_of_versions,
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
        if tenant_code is not None:
            
            _query_params.append(('tenantCode', tenant_code))
            
        if limit is not None:
            
            _query_params.append(('limit', limit))
            
        if start is not None:
            
            _query_params.append(('start', start))
            
        if number_of_versions is not None:
            
            _query_params.append(('numberOfVersions', number_of_versions))
            
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
            resource_path='/v1/op/data-versions',
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
    def list_connector_settings(
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
    ) -> ExtractorSettingsAPIDTO:
        """Retrieve data connector settings

        Get a list of settings for all data connectors. This request retrieves data connectors from the production environment. The response returns a list of settings, if available, for each data connector in the tenant.

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

        _param = self._list_connector_settings_serialize(
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "ExtractorSettingsAPIDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        ).data


    @validate_call
    def list_connector_settings_with_http_info(
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
    ) -> ApiResponse[ExtractorSettingsAPIDTO]:
        """Retrieve data connector settings

        Get a list of settings for all data connectors. This request retrieves data connectors from the production environment. The response returns a list of settings, if available, for each data connector in the tenant.

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

        _param = self._list_connector_settings_serialize(
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "ExtractorSettingsAPIDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        )


    @validate_call
    def list_connector_settings_without_preload_content(
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
        """Retrieve data connector settings

        Get a list of settings for all data connectors. This request retrieves data connectors from the production environment. The response returns a list of settings, if available, for each data connector in the tenant.

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

        _param = self._list_connector_settings_serialize(
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "ExtractorSettingsAPIDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        return response_data.response


    def _list_connector_settings_serialize(
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
            resource_path='/v1/op/data-connectors/connector-settings',
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
    def processing_job_and_status(
        self,
        job_id: Annotated[StrictStr, Field(description="The ID of the dispatching job you want to retrieve.")],
        dispatching_job_id: Annotated[Optional[StrictStr], Field(description="The ID of the dispatching job that generated the extraction jobs.")] = None,
        tenant_code: Annotated[Optional[StrictStr], Field(description="The tenant code of a specific analytic tenant that you want to retrieve the extraction job status for.  Use this if you are only interested in the results for one analytic tenant.")] = None,
        limit: Annotated[Optional[StrictInt], Field(description="The limit of extraction job statuses to retrieve.")] = None,
        start: Annotated[Optional[StrictInt], Field(description="The index to start retrieving results from, also known as offset. The index begins at 0.")] = None,
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
    ) -> ProcessingJobAndStatusResponse:
        """Retrieve a dispatching job's processing jobs with their statuses

        Retrieve the statuses of processing jobs associated with a dispatching job. The dispatching job  is a \"parent\" to extraction jobs, which in turn generate processing jobs and receiving jobs.

        :param job_id: The ID of the dispatching job you want to retrieve. (required)
        :type job_id: str
        :param dispatching_job_id: The ID of the dispatching job that generated the extraction jobs.
        :type dispatching_job_id: str
        :param tenant_code: The tenant code of a specific analytic tenant that you want to retrieve the extraction job status for.  Use this if you are only interested in the results for one analytic tenant.
        :type tenant_code: str
        :param limit: The limit of extraction job statuses to retrieve.
        :type limit: int
        :param start: The index to start retrieving results from, also known as offset. The index begins at 0.
        :type start: int
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

        _param = self._processing_job_and_status_serialize(
            job_id=job_id,
            dispatching_job_id=dispatching_job_id,
            tenant_code=tenant_code,
            limit=limit,
            start=start,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "ProcessingJobAndStatusResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        ).data


    @validate_call
    def processing_job_and_status_with_http_info(
        self,
        job_id: Annotated[StrictStr, Field(description="The ID of the dispatching job you want to retrieve.")],
        dispatching_job_id: Annotated[Optional[StrictStr], Field(description="The ID of the dispatching job that generated the extraction jobs.")] = None,
        tenant_code: Annotated[Optional[StrictStr], Field(description="The tenant code of a specific analytic tenant that you want to retrieve the extraction job status for.  Use this if you are only interested in the results for one analytic tenant.")] = None,
        limit: Annotated[Optional[StrictInt], Field(description="The limit of extraction job statuses to retrieve.")] = None,
        start: Annotated[Optional[StrictInt], Field(description="The index to start retrieving results from, also known as offset. The index begins at 0.")] = None,
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
    ) -> ApiResponse[ProcessingJobAndStatusResponse]:
        """Retrieve a dispatching job's processing jobs with their statuses

        Retrieve the statuses of processing jobs associated with a dispatching job. The dispatching job  is a \"parent\" to extraction jobs, which in turn generate processing jobs and receiving jobs.

        :param job_id: The ID of the dispatching job you want to retrieve. (required)
        :type job_id: str
        :param dispatching_job_id: The ID of the dispatching job that generated the extraction jobs.
        :type dispatching_job_id: str
        :param tenant_code: The tenant code of a specific analytic tenant that you want to retrieve the extraction job status for.  Use this if you are only interested in the results for one analytic tenant.
        :type tenant_code: str
        :param limit: The limit of extraction job statuses to retrieve.
        :type limit: int
        :param start: The index to start retrieving results from, also known as offset. The index begins at 0.
        :type start: int
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

        _param = self._processing_job_and_status_serialize(
            job_id=job_id,
            dispatching_job_id=dispatching_job_id,
            tenant_code=tenant_code,
            limit=limit,
            start=start,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "ProcessingJobAndStatusResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        )


    @validate_call
    def processing_job_and_status_without_preload_content(
        self,
        job_id: Annotated[StrictStr, Field(description="The ID of the dispatching job you want to retrieve.")],
        dispatching_job_id: Annotated[Optional[StrictStr], Field(description="The ID of the dispatching job that generated the extraction jobs.")] = None,
        tenant_code: Annotated[Optional[StrictStr], Field(description="The tenant code of a specific analytic tenant that you want to retrieve the extraction job status for.  Use this if you are only interested in the results for one analytic tenant.")] = None,
        limit: Annotated[Optional[StrictInt], Field(description="The limit of extraction job statuses to retrieve.")] = None,
        start: Annotated[Optional[StrictInt], Field(description="The index to start retrieving results from, also known as offset. The index begins at 0.")] = None,
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
        """Retrieve a dispatching job's processing jobs with their statuses

        Retrieve the statuses of processing jobs associated with a dispatching job. The dispatching job  is a \"parent\" to extraction jobs, which in turn generate processing jobs and receiving jobs.

        :param job_id: The ID of the dispatching job you want to retrieve. (required)
        :type job_id: str
        :param dispatching_job_id: The ID of the dispatching job that generated the extraction jobs.
        :type dispatching_job_id: str
        :param tenant_code: The tenant code of a specific analytic tenant that you want to retrieve the extraction job status for.  Use this if you are only interested in the results for one analytic tenant.
        :type tenant_code: str
        :param limit: The limit of extraction job statuses to retrieve.
        :type limit: int
        :param start: The index to start retrieving results from, also known as offset. The index begins at 0.
        :type start: int
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

        _param = self._processing_job_and_status_serialize(
            job_id=job_id,
            dispatching_job_id=dispatching_job_id,
            tenant_code=tenant_code,
            limit=limit,
            start=start,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "ProcessingJobAndStatusResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        return response_data.response


    def _processing_job_and_status_serialize(
        self,
        job_id,
        dispatching_job_id,
        tenant_code,
        limit,
        start,
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
        if job_id is not None:
            _path_params['jobId'] = job_id
        # process the query parameters
        if dispatching_job_id is not None:
            
            _query_params.append(('dispatchingJobId', dispatching_job_id))
            
        if tenant_code is not None:
            
            _query_params.append(('tenantCode', tenant_code))
            
        if limit is not None:
            
            _query_params.append(('limit', limit))
            
        if start is not None:
            
            _query_params.append(('start', start))
            
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
            resource_path='/v1/op/jobs/dispatching-jobs/{jobId}/processing-jobs',
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
    def processing_job_status(
        self,
        receiving_job_id: Annotated[StrictStr, Field(description="The receiving job ID")],
        tenant_code: Annotated[Optional[StrictStr], Field(description="The tenant code of the tenant you want to retrieve the processing jobs for.  Use this if you are only interested in the results for one analytic tenant.")] = None,
        limit: Annotated[Optional[StrictInt], Field(description="The limit of processing jobs to retrieve per page.")] = None,
        start: Annotated[Optional[StrictInt], Field(description="The index to start retrieving results from, also known as offset. The index begins at 0.")] = None,
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
    ) -> ProcessingJobStatusResponse:
        """Retrieve processing job statuses by receiving job ID

        Retrieve a list of statuses for all processing jobs associated with the given receiving job ID.  Processing jobs deal with an individual analytic tenant's data load. A processing job is either triggered through  the UI or is one of many processing jobs spawned from a receiving job. When a processing job is triggered as part  of a set from an receiving job, it is associated to the receiving job through a Parent ID.

        :param receiving_job_id: The receiving job ID (required)
        :type receiving_job_id: str
        :param tenant_code: The tenant code of the tenant you want to retrieve the processing jobs for.  Use this if you are only interested in the results for one analytic tenant.
        :type tenant_code: str
        :param limit: The limit of processing jobs to retrieve per page.
        :type limit: int
        :param start: The index to start retrieving results from, also known as offset. The index begins at 0.
        :type start: int
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

        _param = self._processing_job_status_serialize(
            receiving_job_id=receiving_job_id,
            tenant_code=tenant_code,
            limit=limit,
            start=start,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "ProcessingJobStatusResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        ).data


    @validate_call
    def processing_job_status_with_http_info(
        self,
        receiving_job_id: Annotated[StrictStr, Field(description="The receiving job ID")],
        tenant_code: Annotated[Optional[StrictStr], Field(description="The tenant code of the tenant you want to retrieve the processing jobs for.  Use this if you are only interested in the results for one analytic tenant.")] = None,
        limit: Annotated[Optional[StrictInt], Field(description="The limit of processing jobs to retrieve per page.")] = None,
        start: Annotated[Optional[StrictInt], Field(description="The index to start retrieving results from, also known as offset. The index begins at 0.")] = None,
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
    ) -> ApiResponse[ProcessingJobStatusResponse]:
        """Retrieve processing job statuses by receiving job ID

        Retrieve a list of statuses for all processing jobs associated with the given receiving job ID.  Processing jobs deal with an individual analytic tenant's data load. A processing job is either triggered through  the UI or is one of many processing jobs spawned from a receiving job. When a processing job is triggered as part  of a set from an receiving job, it is associated to the receiving job through a Parent ID.

        :param receiving_job_id: The receiving job ID (required)
        :type receiving_job_id: str
        :param tenant_code: The tenant code of the tenant you want to retrieve the processing jobs for.  Use this if you are only interested in the results for one analytic tenant.
        :type tenant_code: str
        :param limit: The limit of processing jobs to retrieve per page.
        :type limit: int
        :param start: The index to start retrieving results from, also known as offset. The index begins at 0.
        :type start: int
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

        _param = self._processing_job_status_serialize(
            receiving_job_id=receiving_job_id,
            tenant_code=tenant_code,
            limit=limit,
            start=start,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "ProcessingJobStatusResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        )


    @validate_call
    def processing_job_status_without_preload_content(
        self,
        receiving_job_id: Annotated[StrictStr, Field(description="The receiving job ID")],
        tenant_code: Annotated[Optional[StrictStr], Field(description="The tenant code of the tenant you want to retrieve the processing jobs for.  Use this if you are only interested in the results for one analytic tenant.")] = None,
        limit: Annotated[Optional[StrictInt], Field(description="The limit of processing jobs to retrieve per page.")] = None,
        start: Annotated[Optional[StrictInt], Field(description="The index to start retrieving results from, also known as offset. The index begins at 0.")] = None,
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
        """Retrieve processing job statuses by receiving job ID

        Retrieve a list of statuses for all processing jobs associated with the given receiving job ID.  Processing jobs deal with an individual analytic tenant's data load. A processing job is either triggered through  the UI or is one of many processing jobs spawned from a receiving job. When a processing job is triggered as part  of a set from an receiving job, it is associated to the receiving job through a Parent ID.

        :param receiving_job_id: The receiving job ID (required)
        :type receiving_job_id: str
        :param tenant_code: The tenant code of the tenant you want to retrieve the processing jobs for.  Use this if you are only interested in the results for one analytic tenant.
        :type tenant_code: str
        :param limit: The limit of processing jobs to retrieve per page.
        :type limit: int
        :param start: The index to start retrieving results from, also known as offset. The index begins at 0.
        :type start: int
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

        _param = self._processing_job_status_serialize(
            receiving_job_id=receiving_job_id,
            tenant_code=tenant_code,
            limit=limit,
            start=start,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "ProcessingJobStatusResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        return response_data.response


    def _processing_job_status_serialize(
        self,
        receiving_job_id,
        tenant_code,
        limit,
        start,
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
        if receiving_job_id is not None:
            _path_params['receivingJobId'] = receiving_job_id
        # process the query parameters
        if tenant_code is not None:
            
            _query_params.append(('tenantCode', tenant_code))
            
        if limit is not None:
            
            _query_params.append(('limit', limit))
            
        if start is not None:
            
            _query_params.append(('start', start))
            
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
            resource_path='/v1/op/jobs/processing-jobs/{receivingJobId}',
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
    def receiving_job_and_status(
        self,
        job_id: Annotated[StrictStr, Field(description="The ID of the dispatching job you want to retrieve.")],
        dispatching_job_id: Annotated[Optional[StrictStr], Field(description="The ID of the dispatching job that generated the extraction jobs.")] = None,
        tenant_code: Annotated[Optional[StrictStr], Field(description="The tenant code of a specific analytic tenant that you want to retrieve the extraction job status for.  Use this if you are only interested in the results for one analytic tenant.")] = None,
        limit: Annotated[Optional[StrictInt], Field(description="The limit of extraction job statuses to retrieve.")] = None,
        start: Annotated[Optional[StrictInt], Field(description="The index to start retrieving results from, also known as offset. The index begins at 0.")] = None,
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
    ) -> ReceivingJobAndStatusResponse:
        """Retrieve a dispatching job's receiving jobs with their statuses

        Retrieve the statuses of receiving jobs associated with a dispatching job. The dispatching job  is a \"parent\" to extraction jobs, which in turn generate processing jobs and receiving jobs.

        :param job_id: The ID of the dispatching job you want to retrieve. (required)
        :type job_id: str
        :param dispatching_job_id: The ID of the dispatching job that generated the extraction jobs.
        :type dispatching_job_id: str
        :param tenant_code: The tenant code of a specific analytic tenant that you want to retrieve the extraction job status for.  Use this if you are only interested in the results for one analytic tenant.
        :type tenant_code: str
        :param limit: The limit of extraction job statuses to retrieve.
        :type limit: int
        :param start: The index to start retrieving results from, also known as offset. The index begins at 0.
        :type start: int
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

        _param = self._receiving_job_and_status_serialize(
            job_id=job_id,
            dispatching_job_id=dispatching_job_id,
            tenant_code=tenant_code,
            limit=limit,
            start=start,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "ReceivingJobAndStatusResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        ).data


    @validate_call
    def receiving_job_and_status_with_http_info(
        self,
        job_id: Annotated[StrictStr, Field(description="The ID of the dispatching job you want to retrieve.")],
        dispatching_job_id: Annotated[Optional[StrictStr], Field(description="The ID of the dispatching job that generated the extraction jobs.")] = None,
        tenant_code: Annotated[Optional[StrictStr], Field(description="The tenant code of a specific analytic tenant that you want to retrieve the extraction job status for.  Use this if you are only interested in the results for one analytic tenant.")] = None,
        limit: Annotated[Optional[StrictInt], Field(description="The limit of extraction job statuses to retrieve.")] = None,
        start: Annotated[Optional[StrictInt], Field(description="The index to start retrieving results from, also known as offset. The index begins at 0.")] = None,
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
    ) -> ApiResponse[ReceivingJobAndStatusResponse]:
        """Retrieve a dispatching job's receiving jobs with their statuses

        Retrieve the statuses of receiving jobs associated with a dispatching job. The dispatching job  is a \"parent\" to extraction jobs, which in turn generate processing jobs and receiving jobs.

        :param job_id: The ID of the dispatching job you want to retrieve. (required)
        :type job_id: str
        :param dispatching_job_id: The ID of the dispatching job that generated the extraction jobs.
        :type dispatching_job_id: str
        :param tenant_code: The tenant code of a specific analytic tenant that you want to retrieve the extraction job status for.  Use this if you are only interested in the results for one analytic tenant.
        :type tenant_code: str
        :param limit: The limit of extraction job statuses to retrieve.
        :type limit: int
        :param start: The index to start retrieving results from, also known as offset. The index begins at 0.
        :type start: int
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

        _param = self._receiving_job_and_status_serialize(
            job_id=job_id,
            dispatching_job_id=dispatching_job_id,
            tenant_code=tenant_code,
            limit=limit,
            start=start,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "ReceivingJobAndStatusResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        )


    @validate_call
    def receiving_job_and_status_without_preload_content(
        self,
        job_id: Annotated[StrictStr, Field(description="The ID of the dispatching job you want to retrieve.")],
        dispatching_job_id: Annotated[Optional[StrictStr], Field(description="The ID of the dispatching job that generated the extraction jobs.")] = None,
        tenant_code: Annotated[Optional[StrictStr], Field(description="The tenant code of a specific analytic tenant that you want to retrieve the extraction job status for.  Use this if you are only interested in the results for one analytic tenant.")] = None,
        limit: Annotated[Optional[StrictInt], Field(description="The limit of extraction job statuses to retrieve.")] = None,
        start: Annotated[Optional[StrictInt], Field(description="The index to start retrieving results from, also known as offset. The index begins at 0.")] = None,
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
        """Retrieve a dispatching job's receiving jobs with their statuses

        Retrieve the statuses of receiving jobs associated with a dispatching job. The dispatching job  is a \"parent\" to extraction jobs, which in turn generate processing jobs and receiving jobs.

        :param job_id: The ID of the dispatching job you want to retrieve. (required)
        :type job_id: str
        :param dispatching_job_id: The ID of the dispatching job that generated the extraction jobs.
        :type dispatching_job_id: str
        :param tenant_code: The tenant code of a specific analytic tenant that you want to retrieve the extraction job status for.  Use this if you are only interested in the results for one analytic tenant.
        :type tenant_code: str
        :param limit: The limit of extraction job statuses to retrieve.
        :type limit: int
        :param start: The index to start retrieving results from, also known as offset. The index begins at 0.
        :type start: int
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

        _param = self._receiving_job_and_status_serialize(
            job_id=job_id,
            dispatching_job_id=dispatching_job_id,
            tenant_code=tenant_code,
            limit=limit,
            start=start,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "ReceivingJobAndStatusResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        return response_data.response


    def _receiving_job_and_status_serialize(
        self,
        job_id,
        dispatching_job_id,
        tenant_code,
        limit,
        start,
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
        if job_id is not None:
            _path_params['jobId'] = job_id
        # process the query parameters
        if dispatching_job_id is not None:
            
            _query_params.append(('dispatchingJobId', dispatching_job_id))
            
        if tenant_code is not None:
            
            _query_params.append(('tenantCode', tenant_code))
            
        if limit is not None:
            
            _query_params.append(('limit', limit))
            
        if start is not None:
            
            _query_params.append(('start', start))
            
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
            resource_path='/v1/op/jobs/dispatching-jobs/{jobId}/receiving-jobs',
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
    def receiving_job_status(
        self,
        receiving_job_id: Annotated[StrictStr, Field(description="The jobId provided after sending data to Visier.")],
        jobs: Annotated[Optional[StrictBool], Field(description="If `true`, returns the status of receiving jobs spawned by the receiving job specified by `jobId`.")] = None,
        tenant_code: Annotated[Optional[StrictStr], Field(description="The tenant code of the tenant you want to retrieve the receiving jobs for. Use this if you are only interested  in the results for one analytic tenant.")] = None,
        start: Annotated[Optional[StrictInt], Field(description="The index to start retrieving results from, also known as offset. The index begins at 0.")] = None,
        limit: Annotated[Optional[StrictInt], Field(description="The number of job statuses to return per page.")] = None,
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
    ) -> ReceivingJobStatusResponse:
        """Retrieve a receiving job's status

        After sending data to Visier, you may want to know the status of the receiving job and the associated tenant  receiving jobs. A receiving job validates the transferred data and adds the transferred data to Visier's data  store.    A successful response indicates that the receiving job was successful. To get the status of the jobs spawned by the receiving job, set the `jobs` parameter to `true`.

        :param receiving_job_id: The jobId provided after sending data to Visier. (required)
        :type receiving_job_id: str
        :param jobs: If `true`, returns the status of receiving jobs spawned by the receiving job specified by `jobId`.
        :type jobs: bool
        :param tenant_code: The tenant code of the tenant you want to retrieve the receiving jobs for. Use this if you are only interested  in the results for one analytic tenant.
        :type tenant_code: str
        :param start: The index to start retrieving results from, also known as offset. The index begins at 0.
        :type start: int
        :param limit: The number of job statuses to return per page.
        :type limit: int
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

        _param = self._receiving_job_status_serialize(
            receiving_job_id=receiving_job_id,
            jobs=jobs,
            tenant_code=tenant_code,
            start=start,
            limit=limit,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "ReceivingJobStatusResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        ).data


    @validate_call
    def receiving_job_status_with_http_info(
        self,
        receiving_job_id: Annotated[StrictStr, Field(description="The jobId provided after sending data to Visier.")],
        jobs: Annotated[Optional[StrictBool], Field(description="If `true`, returns the status of receiving jobs spawned by the receiving job specified by `jobId`.")] = None,
        tenant_code: Annotated[Optional[StrictStr], Field(description="The tenant code of the tenant you want to retrieve the receiving jobs for. Use this if you are only interested  in the results for one analytic tenant.")] = None,
        start: Annotated[Optional[StrictInt], Field(description="The index to start retrieving results from, also known as offset. The index begins at 0.")] = None,
        limit: Annotated[Optional[StrictInt], Field(description="The number of job statuses to return per page.")] = None,
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
    ) -> ApiResponse[ReceivingJobStatusResponse]:
        """Retrieve a receiving job's status

        After sending data to Visier, you may want to know the status of the receiving job and the associated tenant  receiving jobs. A receiving job validates the transferred data and adds the transferred data to Visier's data  store.    A successful response indicates that the receiving job was successful. To get the status of the jobs spawned by the receiving job, set the `jobs` parameter to `true`.

        :param receiving_job_id: The jobId provided after sending data to Visier. (required)
        :type receiving_job_id: str
        :param jobs: If `true`, returns the status of receiving jobs spawned by the receiving job specified by `jobId`.
        :type jobs: bool
        :param tenant_code: The tenant code of the tenant you want to retrieve the receiving jobs for. Use this if you are only interested  in the results for one analytic tenant.
        :type tenant_code: str
        :param start: The index to start retrieving results from, also known as offset. The index begins at 0.
        :type start: int
        :param limit: The number of job statuses to return per page.
        :type limit: int
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

        _param = self._receiving_job_status_serialize(
            receiving_job_id=receiving_job_id,
            jobs=jobs,
            tenant_code=tenant_code,
            start=start,
            limit=limit,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "ReceivingJobStatusResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        )


    @validate_call
    def receiving_job_status_without_preload_content(
        self,
        receiving_job_id: Annotated[StrictStr, Field(description="The jobId provided after sending data to Visier.")],
        jobs: Annotated[Optional[StrictBool], Field(description="If `true`, returns the status of receiving jobs spawned by the receiving job specified by `jobId`.")] = None,
        tenant_code: Annotated[Optional[StrictStr], Field(description="The tenant code of the tenant you want to retrieve the receiving jobs for. Use this if you are only interested  in the results for one analytic tenant.")] = None,
        start: Annotated[Optional[StrictInt], Field(description="The index to start retrieving results from, also known as offset. The index begins at 0.")] = None,
        limit: Annotated[Optional[StrictInt], Field(description="The number of job statuses to return per page.")] = None,
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
        """Retrieve a receiving job's status

        After sending data to Visier, you may want to know the status of the receiving job and the associated tenant  receiving jobs. A receiving job validates the transferred data and adds the transferred data to Visier's data  store.    A successful response indicates that the receiving job was successful. To get the status of the jobs spawned by the receiving job, set the `jobs` parameter to `true`.

        :param receiving_job_id: The jobId provided after sending data to Visier. (required)
        :type receiving_job_id: str
        :param jobs: If `true`, returns the status of receiving jobs spawned by the receiving job specified by `jobId`.
        :type jobs: bool
        :param tenant_code: The tenant code of the tenant you want to retrieve the receiving jobs for. Use this if you are only interested  in the results for one analytic tenant.
        :type tenant_code: str
        :param start: The index to start retrieving results from, also known as offset. The index begins at 0.
        :type start: int
        :param limit: The number of job statuses to return per page.
        :type limit: int
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

        _param = self._receiving_job_status_serialize(
            receiving_job_id=receiving_job_id,
            jobs=jobs,
            tenant_code=tenant_code,
            start=start,
            limit=limit,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "ReceivingJobStatusResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        return response_data.response


    def _receiving_job_status_serialize(
        self,
        receiving_job_id,
        jobs,
        tenant_code,
        start,
        limit,
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
        if receiving_job_id is not None:
            _path_params['receivingJobId'] = receiving_job_id
        # process the query parameters
        if jobs is not None:
            
            _query_params.append(('jobs', jobs))
            
        if tenant_code is not None:
            
            _query_params.append(('tenantCode', tenant_code))
            
        if start is not None:
            
            _query_params.append(('start', start))
            
        if limit is not None:
            
            _query_params.append(('limit', limit))
            
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
            resource_path='/v1/op/jobs/receiving-jobs/{receivingJobId}',
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
    def retrieve_data_categories(
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
    ) -> DataCategoriesResponseDTO:
        """Retrieve a list of all data categories

        Retrieve a list of all available data categories.

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

        _param = self._retrieve_data_categories_serialize(
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "DataCategoriesResponseDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        ).data


    @validate_call
    def retrieve_data_categories_with_http_info(
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
    ) -> ApiResponse[DataCategoriesResponseDTO]:
        """Retrieve a list of all data categories

        Retrieve a list of all available data categories.

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

        _param = self._retrieve_data_categories_serialize(
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "DataCategoriesResponseDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        )


    @validate_call
    def retrieve_data_categories_without_preload_content(
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
        """Retrieve a list of all data categories

        Retrieve a list of all available data categories.

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

        _param = self._retrieve_data_categories_serialize(
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "DataCategoriesResponseDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        return response_data.response


    def _retrieve_data_categories_serialize(
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
            resource_path='/v1/op/data/categories',
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
    def retrieve_data_uploads(
        self,
        upload_job_id: Annotated[Optional[StrictStr], Field(description="The job ID of an upload job. Use this if you are interested in the data uploads for a specific upload job.")] = None,
        tenant_code: Annotated[Optional[StrictInt], Field(description="The tenant code of a specific analytic tenant that you want to retrieve the data uploads for.")] = None,
        limit: Annotated[Optional[StrictInt], Field(description="The limit of analytic tenants to retrieve data uploads for. This parameter is not used if the tenantCode parameter is specified. Default is 1000.")] = None,
        start: Annotated[Optional[StrictInt], Field(description="The index to start retrieving results from, also known as offset. The index begins at 0.")] = None,
        number_of_data_uploads: Annotated[Optional[StrictInt], Field(description="The maximum number of latest enabled data uploads to retrieve for each analytic tenant. The maximum value is 5. Default is 1.")] = None,
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
    ) -> TenantDataUploadsListResponseDTO:
        """Retrieve data uploads

        Retrieve the data uploads and whether they're included in one of:  - A list of analytic tenants managed by you.  - A single specified analytic tenant.  - An upload job.

        :param upload_job_id: The job ID of an upload job. Use this if you are interested in the data uploads for a specific upload job.
        :type upload_job_id: str
        :param tenant_code: The tenant code of a specific analytic tenant that you want to retrieve the data uploads for.
        :type tenant_code: int
        :param limit: The limit of analytic tenants to retrieve data uploads for. This parameter is not used if the tenantCode parameter is specified. Default is 1000.
        :type limit: int
        :param start: The index to start retrieving results from, also known as offset. The index begins at 0.
        :type start: int
        :param number_of_data_uploads: The maximum number of latest enabled data uploads to retrieve for each analytic tenant. The maximum value is 5. Default is 1.
        :type number_of_data_uploads: int
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

        _param = self._retrieve_data_uploads_serialize(
            upload_job_id=upload_job_id,
            tenant_code=tenant_code,
            limit=limit,
            start=start,
            number_of_data_uploads=number_of_data_uploads,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "TenantDataUploadsListResponseDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        ).data


    @validate_call
    def retrieve_data_uploads_with_http_info(
        self,
        upload_job_id: Annotated[Optional[StrictStr], Field(description="The job ID of an upload job. Use this if you are interested in the data uploads for a specific upload job.")] = None,
        tenant_code: Annotated[Optional[StrictInt], Field(description="The tenant code of a specific analytic tenant that you want to retrieve the data uploads for.")] = None,
        limit: Annotated[Optional[StrictInt], Field(description="The limit of analytic tenants to retrieve data uploads for. This parameter is not used if the tenantCode parameter is specified. Default is 1000.")] = None,
        start: Annotated[Optional[StrictInt], Field(description="The index to start retrieving results from, also known as offset. The index begins at 0.")] = None,
        number_of_data_uploads: Annotated[Optional[StrictInt], Field(description="The maximum number of latest enabled data uploads to retrieve for each analytic tenant. The maximum value is 5. Default is 1.")] = None,
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
    ) -> ApiResponse[TenantDataUploadsListResponseDTO]:
        """Retrieve data uploads

        Retrieve the data uploads and whether they're included in one of:  - A list of analytic tenants managed by you.  - A single specified analytic tenant.  - An upload job.

        :param upload_job_id: The job ID of an upload job. Use this if you are interested in the data uploads for a specific upload job.
        :type upload_job_id: str
        :param tenant_code: The tenant code of a specific analytic tenant that you want to retrieve the data uploads for.
        :type tenant_code: int
        :param limit: The limit of analytic tenants to retrieve data uploads for. This parameter is not used if the tenantCode parameter is specified. Default is 1000.
        :type limit: int
        :param start: The index to start retrieving results from, also known as offset. The index begins at 0.
        :type start: int
        :param number_of_data_uploads: The maximum number of latest enabled data uploads to retrieve for each analytic tenant. The maximum value is 5. Default is 1.
        :type number_of_data_uploads: int
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

        _param = self._retrieve_data_uploads_serialize(
            upload_job_id=upload_job_id,
            tenant_code=tenant_code,
            limit=limit,
            start=start,
            number_of_data_uploads=number_of_data_uploads,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "TenantDataUploadsListResponseDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        )


    @validate_call
    def retrieve_data_uploads_without_preload_content(
        self,
        upload_job_id: Annotated[Optional[StrictStr], Field(description="The job ID of an upload job. Use this if you are interested in the data uploads for a specific upload job.")] = None,
        tenant_code: Annotated[Optional[StrictInt], Field(description="The tenant code of a specific analytic tenant that you want to retrieve the data uploads for.")] = None,
        limit: Annotated[Optional[StrictInt], Field(description="The limit of analytic tenants to retrieve data uploads for. This parameter is not used if the tenantCode parameter is specified. Default is 1000.")] = None,
        start: Annotated[Optional[StrictInt], Field(description="The index to start retrieving results from, also known as offset. The index begins at 0.")] = None,
        number_of_data_uploads: Annotated[Optional[StrictInt], Field(description="The maximum number of latest enabled data uploads to retrieve for each analytic tenant. The maximum value is 5. Default is 1.")] = None,
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
        """Retrieve data uploads

        Retrieve the data uploads and whether they're included in one of:  - A list of analytic tenants managed by you.  - A single specified analytic tenant.  - An upload job.

        :param upload_job_id: The job ID of an upload job. Use this if you are interested in the data uploads for a specific upload job.
        :type upload_job_id: str
        :param tenant_code: The tenant code of a specific analytic tenant that you want to retrieve the data uploads for.
        :type tenant_code: int
        :param limit: The limit of analytic tenants to retrieve data uploads for. This parameter is not used if the tenantCode parameter is specified. Default is 1000.
        :type limit: int
        :param start: The index to start retrieving results from, also known as offset. The index begins at 0.
        :type start: int
        :param number_of_data_uploads: The maximum number of latest enabled data uploads to retrieve for each analytic tenant. The maximum value is 5. Default is 1.
        :type number_of_data_uploads: int
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

        _param = self._retrieve_data_uploads_serialize(
            upload_job_id=upload_job_id,
            tenant_code=tenant_code,
            limit=limit,
            start=start,
            number_of_data_uploads=number_of_data_uploads,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "TenantDataUploadsListResponseDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        return response_data.response


    def _retrieve_data_uploads_serialize(
        self,
        upload_job_id,
        tenant_code,
        limit,
        start,
        number_of_data_uploads,
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
        if upload_job_id is not None:
            
            _query_params.append(('uploadJobId', upload_job_id))
            
        if tenant_code is not None:
            
            _query_params.append(('tenantCode', tenant_code))
            
        if limit is not None:
            
            _query_params.append(('limit', limit))
            
        if start is not None:
            
            _query_params.append(('start', start))
            
        if number_of_data_uploads is not None:
            
            _query_params.append(('numberOfDataUploads', number_of_data_uploads))
            
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
            resource_path='/v1/op/data/uploads',
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
    def set_connector_setting(
        self,
        set_connector_settings_request_dto: SetConnectorSettingsRequestDTO,
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
    ) -> SetConnectorSettingsResponseDTO:
        """Update data connector settings

        Define the settings for one or more data connectors. To find the available settings, see `Retrieve data connector settings`.

        :param set_connector_settings_request_dto: (required)
        :type set_connector_settings_request_dto: SetConnectorSettingsRequestDTO
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

        _param = self._set_connector_setting_serialize(
            set_connector_settings_request_dto=set_connector_settings_request_dto,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "SetConnectorSettingsResponseDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        ).data


    @validate_call
    def set_connector_setting_with_http_info(
        self,
        set_connector_settings_request_dto: SetConnectorSettingsRequestDTO,
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
    ) -> ApiResponse[SetConnectorSettingsResponseDTO]:
        """Update data connector settings

        Define the settings for one or more data connectors. To find the available settings, see `Retrieve data connector settings`.

        :param set_connector_settings_request_dto: (required)
        :type set_connector_settings_request_dto: SetConnectorSettingsRequestDTO
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

        _param = self._set_connector_setting_serialize(
            set_connector_settings_request_dto=set_connector_settings_request_dto,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "SetConnectorSettingsResponseDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        )


    @validate_call
    def set_connector_setting_without_preload_content(
        self,
        set_connector_settings_request_dto: SetConnectorSettingsRequestDTO,
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
        """Update data connector settings

        Define the settings for one or more data connectors. To find the available settings, see `Retrieve data connector settings`.

        :param set_connector_settings_request_dto: (required)
        :type set_connector_settings_request_dto: SetConnectorSettingsRequestDTO
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

        _param = self._set_connector_setting_serialize(
            set_connector_settings_request_dto=set_connector_settings_request_dto,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "SetConnectorSettingsResponseDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        return response_data.response


    def _set_connector_setting_serialize(
        self,
        set_connector_settings_request_dto,
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
        if set_connector_settings_request_dto is not None:
            _body_params = set_connector_settings_request_dto


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
            method='PUT',
            resource_path='/v1/op/data-connectors/connector-settings',
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
    def start_extraction(
        self,
        extract_data_and_load_dto: ExtractDataAndLoadDTO,
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
    ) -> StartExtractionResponse:
        """Trigger data connector extraction jobs

        Run data connector extraction jobs for the administrating tenant or a list of analytic tenants.    This API creates a dispatching job that generates one extraction job per tenant. The dispatching job is the \"parent\" of the extraction jobs and the dispatching job ID is returned in the response. Use that ID to monitor the extraction job statuses by calling `GET /v1/op/jobs/dispatching-jobs/{jobId}/extraction-jobs`.   The extraction job generates receiving jobs to validate the data and processing jobs to populate data in the analytic tenants. Use the dispatching job ID to monitor the receiving and processing job statuses by calling `GET /v1/op/jobs/dispatching-jobs/{jobId}/receiving-jobs` or `GET /v1/op/jobs/dispatching-jobs/{jobId}/processing-jobs`.

        :param extract_data_and_load_dto: (required)
        :type extract_data_and_load_dto: ExtractDataAndLoadDTO
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

        _param = self._start_extraction_serialize(
            extract_data_and_load_dto=extract_data_and_load_dto,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "StartExtractionResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        ).data


    @validate_call
    def start_extraction_with_http_info(
        self,
        extract_data_and_load_dto: ExtractDataAndLoadDTO,
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
    ) -> ApiResponse[StartExtractionResponse]:
        """Trigger data connector extraction jobs

        Run data connector extraction jobs for the administrating tenant or a list of analytic tenants.    This API creates a dispatching job that generates one extraction job per tenant. The dispatching job is the \"parent\" of the extraction jobs and the dispatching job ID is returned in the response. Use that ID to monitor the extraction job statuses by calling `GET /v1/op/jobs/dispatching-jobs/{jobId}/extraction-jobs`.   The extraction job generates receiving jobs to validate the data and processing jobs to populate data in the analytic tenants. Use the dispatching job ID to monitor the receiving and processing job statuses by calling `GET /v1/op/jobs/dispatching-jobs/{jobId}/receiving-jobs` or `GET /v1/op/jobs/dispatching-jobs/{jobId}/processing-jobs`.

        :param extract_data_and_load_dto: (required)
        :type extract_data_and_load_dto: ExtractDataAndLoadDTO
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

        _param = self._start_extraction_serialize(
            extract_data_and_load_dto=extract_data_and_load_dto,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "StartExtractionResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        )


    @validate_call
    def start_extraction_without_preload_content(
        self,
        extract_data_and_load_dto: ExtractDataAndLoadDTO,
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
        """Trigger data connector extraction jobs

        Run data connector extraction jobs for the administrating tenant or a list of analytic tenants.    This API creates a dispatching job that generates one extraction job per tenant. The dispatching job is the \"parent\" of the extraction jobs and the dispatching job ID is returned in the response. Use that ID to monitor the extraction job statuses by calling `GET /v1/op/jobs/dispatching-jobs/{jobId}/extraction-jobs`.   The extraction job generates receiving jobs to validate the data and processing jobs to populate data in the analytic tenants. Use the dispatching job ID to monitor the receiving and processing job statuses by calling `GET /v1/op/jobs/dispatching-jobs/{jobId}/receiving-jobs` or `GET /v1/op/jobs/dispatching-jobs/{jobId}/processing-jobs`.

        :param extract_data_and_load_dto: (required)
        :type extract_data_and_load_dto: ExtractDataAndLoadDTO
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

        _param = self._start_extraction_serialize(
            extract_data_and_load_dto=extract_data_and_load_dto,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "StartExtractionResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        return response_data.response


    def _start_extraction_serialize(
        self,
        extract_data_and_load_dto,
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
        if extract_data_and_load_dto is not None:
            _body_params = extract_data_and_load_dto


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
            resource_path='/v1/op/data/startExtractAndLoad',
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
    def start_load(
        self,
        data_load_request: DataLoadRequest,
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
    ) -> DataLoadResponse:
        """Start the data load for analytic tenants

        This API starts the data load process for all analytic tenants included in the specified data files uploaded  to the Visier SFTP server. On success, you receive a job ID that can be filtered and searched for within the  Jobs room in Visier. This job ID is associated with the receiving job, and related to all processing jobs that  spawn for each analytic tenant.   With the job ID, you can also call the next two APIs to retrieve the status of the receiving job and the status  list of all related processing jobs.   **Prerequisite:** You must first obtain Visier's public encryption key and upload the source data files to Visier's  SFTP server. Files must have a .zip.gpg extension, meaning the files are encrypted using the PGP protocol and compressed.   Visier provides SFTP server credentials and instructions. You can find the encryption key at https://www.visier.com/pgp/visier.public.pgp.asc.  After downloading the file, open the file in a text editor or by dragging it into your browser.   **Note:**   - To see the full status of all analytic tenant data loads, navigate to the Jobs room in a project.   - For performance and efficiency, Visier requires that the uncompressed batch file size is below 5 GB and that no     more than 5000 tenants are included in a batch.

        :param data_load_request: (required)
        :type data_load_request: DataLoadRequest
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

        _param = self._start_load_serialize(
            data_load_request=data_load_request,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "DataLoadResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        ).data


    @validate_call
    def start_load_with_http_info(
        self,
        data_load_request: DataLoadRequest,
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
    ) -> ApiResponse[DataLoadResponse]:
        """Start the data load for analytic tenants

        This API starts the data load process for all analytic tenants included in the specified data files uploaded  to the Visier SFTP server. On success, you receive a job ID that can be filtered and searched for within the  Jobs room in Visier. This job ID is associated with the receiving job, and related to all processing jobs that  spawn for each analytic tenant.   With the job ID, you can also call the next two APIs to retrieve the status of the receiving job and the status  list of all related processing jobs.   **Prerequisite:** You must first obtain Visier's public encryption key and upload the source data files to Visier's  SFTP server. Files must have a .zip.gpg extension, meaning the files are encrypted using the PGP protocol and compressed.   Visier provides SFTP server credentials and instructions. You can find the encryption key at https://www.visier.com/pgp/visier.public.pgp.asc.  After downloading the file, open the file in a text editor or by dragging it into your browser.   **Note:**   - To see the full status of all analytic tenant data loads, navigate to the Jobs room in a project.   - For performance and efficiency, Visier requires that the uncompressed batch file size is below 5 GB and that no     more than 5000 tenants are included in a batch.

        :param data_load_request: (required)
        :type data_load_request: DataLoadRequest
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

        _param = self._start_load_serialize(
            data_load_request=data_load_request,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "DataLoadResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_data_in.models,
            response_data=response_data,
            response_types_map=_response_types_map
        )


    @validate_call
    def start_load_without_preload_content(
        self,
        data_load_request: DataLoadRequest,
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
        """Start the data load for analytic tenants

        This API starts the data load process for all analytic tenants included in the specified data files uploaded  to the Visier SFTP server. On success, you receive a job ID that can be filtered and searched for within the  Jobs room in Visier. This job ID is associated with the receiving job, and related to all processing jobs that  spawn for each analytic tenant.   With the job ID, you can also call the next two APIs to retrieve the status of the receiving job and the status  list of all related processing jobs.   **Prerequisite:** You must first obtain Visier's public encryption key and upload the source data files to Visier's  SFTP server. Files must have a .zip.gpg extension, meaning the files are encrypted using the PGP protocol and compressed.   Visier provides SFTP server credentials and instructions. You can find the encryption key at https://www.visier.com/pgp/visier.public.pgp.asc.  After downloading the file, open the file in a text editor or by dragging it into your browser.   **Note:**   - To see the full status of all analytic tenant data loads, navigate to the Jobs room in a project.   - For performance and efficiency, Visier requires that the uncompressed batch file size is below 5 GB and that no     more than 5000 tenants are included in a batch.

        :param data_load_request: (required)
        :type data_load_request: DataLoadRequest
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

        _param = self._start_load_serialize(
            data_load_request=data_load_request,
            target_tenant_id=target_tenant_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "DataLoadResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        return response_data.response


    def _start_load_serialize(
        self,
        data_load_request,
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
        if data_load_request is not None:
            _body_params = data_load_request


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
            resource_path='/v1/op/data/startload',
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


