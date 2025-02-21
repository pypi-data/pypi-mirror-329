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


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from visier_api_data_in.models.adp_auth_params_dto import AdpAuthParamsDTO
from visier_api_data_in.models.bamboo_auth_params_dto import BambooAuthParamsDTO
from visier_api_data_in.models.basic_s3_auth_params_dto import BasicS3AuthParamsDTO
from visier_api_data_in.models.big_query_auth_params_dto import BigQueryAuthParamsDTO
from visier_api_data_in.models.copy_s3_auth_params_dto import CopyS3AuthParamsDTO
from visier_api_data_in.models.dayforce_v2_auth_params_dto import DayforceV2AuthParamsDTO
from visier_api_data_in.models.dimensions_auth_params_dto import DimensionsAuthParamsDTO
from visier_api_data_in.models.fusion_auth_params_dto import FusionAuthParamsDTO
from visier_api_data_in.models.gong_auth_params_dto import GongAuthParamsDTO
from visier_api_data_in.models.google_sheets_auth_params_dto import GoogleSheetsAuthParamsDTO
from visier_api_data_in.models.google_workspace_auth_params_dto import GoogleWorkspaceAuthParamsDTO
from visier_api_data_in.models.greenhouse_auth_params_dto import GreenhouseAuthParamsDTO
from visier_api_data_in.models.icims_auth_params_dto import IcimsAuthParamsDTO
from visier_api_data_in.models.internal_s3_auth_params_dto import InternalS3AuthParamsDTO
from visier_api_data_in.models.jdbc_auth_params_dto import JdbcAuthParamsDTO
from visier_api_data_in.models.jira_auth_params_dto import JiraAuthParamsDTO
from visier_api_data_in.models.lever_auth_params_dto import LeverAuthParamsDTO
from visier_api_data_in.models.medallia_auth_params_dto import MedalliaAuthParamsDTO
from visier_api_data_in.models.microsoft365_auth_params_dto import Microsoft365AuthParamsDTO
from visier_api_data_in.models.my_sql_auth_params_dto import MySqlAuthParamsDTO
from visier_api_data_in.models.namely_auth_params_dto import NamelyAuthParamsDTO
from visier_api_data_in.models.oracle_db_auth_params_dto import OracleDbAuthParamsDTO
from visier_api_data_in.models.qualtrics_auth_params_dto import QualtricsAuthParamsDTO
from visier_api_data_in.models.redshift_auth_params_dto import RedshiftAuthParamsDTO
from visier_api_data_in.models.salesforce_auth_params_dto import SalesforceAuthParamsDTO
from visier_api_data_in.models.salesforce_v2_auth_params_dto import SalesforceV2AuthParamsDTO
from visier_api_data_in.models.service_now_auth_params_dto import ServiceNowAuthParamsDTO
from visier_api_data_in.models.service_now_v2_auth_params_dto import ServiceNowV2AuthParamsDTO
from visier_api_data_in.models.slack_auth_params_dto import SlackAuthParamsDTO
from visier_api_data_in.models.snowflake_auth_params_dto import SnowflakeAuthParamsDTO
from visier_api_data_in.models.sql_server_auth_params_dto import SqlServerAuthParamsDTO
from visier_api_data_in.models.success_factors_auth_params_dto import SuccessFactorsAuthParamsDTO
from visier_api_data_in.models.ultimate_auth_params_dto import UltimateAuthParamsDTO
from visier_api_data_in.models.willow_auth_params_dto import WillowAuthParamsDTO
from visier_api_data_in.models.workday_auth_params_dto import WorkdayAuthParamsDTO
from visier_api_data_in.models.workday_raas_auth_params_dto import WorkdayRaasAuthParamsDTO
from visier_api_data_in.models.zoom_auth_params_dto import ZoomAuthParamsDTO
from typing import Optional, Set
from typing_extensions import Self

class DataProviderAuthParamsDTO(BaseModel):
    """
    DataProviderAuthParamsDTO
    """ # noqa: E501
    adp_auth_params: Optional[AdpAuthParamsDTO] = Field(default=None, alias="adpAuthParams")
    auth_context: Optional[StrictStr] = Field(default=None, alias="authContext")
    bamboo_auth_params: Optional[BambooAuthParamsDTO] = Field(default=None, alias="bambooAuthParams")
    big_query_auth_params: Optional[BigQueryAuthParamsDTO] = Field(default=None, alias="bigQueryAuthParams")
    copy_s3_auth_params: Optional[CopyS3AuthParamsDTO] = Field(default=None, alias="copyS3AuthParams")
    dayforce_v2_auth_params: Optional[DayforceV2AuthParamsDTO] = Field(default=None, alias="dayforceV2AuthParams")
    dimensions_auth_params: Optional[DimensionsAuthParamsDTO] = Field(default=None, alias="dimensionsAuthParams")
    empty_auth_params: Optional[Dict[str, Any]] = Field(default=None, alias="emptyAuthParams")
    fusion_auth_params: Optional[FusionAuthParamsDTO] = Field(default=None, alias="fusionAuthParams")
    gong_auth_params: Optional[GongAuthParamsDTO] = Field(default=None, alias="gongAuthParams")
    google_sheets_auth_params: Optional[GoogleSheetsAuthParamsDTO] = Field(default=None, alias="googleSheetsAuthParams")
    google_workspace_auth_params: Optional[GoogleWorkspaceAuthParamsDTO] = Field(default=None, alias="googleWorkspaceAuthParams")
    greenhouse_auth_params: Optional[GreenhouseAuthParamsDTO] = Field(default=None, alias="greenhouseAuthParams")
    has_updates: Optional[StrictBool] = Field(default=None, alias="hasUpdates")
    icims_auth_params: Optional[IcimsAuthParamsDTO] = Field(default=None, alias="icimsAuthParams")
    internal_s3_auth_params: Optional[InternalS3AuthParamsDTO] = Field(default=None, alias="internalS3AuthParams")
    jdbc_auth_params: Optional[JdbcAuthParamsDTO] = Field(default=None, alias="jdbcAuthParams")
    jira_auth_params: Optional[JiraAuthParamsDTO] = Field(default=None, alias="jiraAuthParams")
    lever_auth_params: Optional[LeverAuthParamsDTO] = Field(default=None, alias="leverAuthParams")
    medallia_auth_params: Optional[MedalliaAuthParamsDTO] = Field(default=None, alias="medalliaAuthParams")
    ms365_auth_params: Optional[Microsoft365AuthParamsDTO] = Field(default=None, alias="ms365AuthParams")
    my_sql_auth_params: Optional[MySqlAuthParamsDTO] = Field(default=None, alias="mySqlAuthParams")
    namely_auth_params: Optional[NamelyAuthParamsDTO] = Field(default=None, alias="namelyAuthParams")
    oracle_db_auth_params: Optional[OracleDbAuthParamsDTO] = Field(default=None, alias="oracleDbAuthParams")
    provider: Optional[StrictStr] = Field(default=None, description="The data provider associated with the credential.")
    qualtrics_auth_params: Optional[QualtricsAuthParamsDTO] = Field(default=None, alias="qualtricsAuthParams")
    redshift_auth_params: Optional[RedshiftAuthParamsDTO] = Field(default=None, alias="redshiftAuthParams")
    s3_auth_params: Optional[BasicS3AuthParamsDTO] = Field(default=None, alias="s3AuthParams")
    salesforce_auth_params: Optional[SalesforceAuthParamsDTO] = Field(default=None, alias="salesforceAuthParams")
    salesforce_v2_auth_params: Optional[SalesforceV2AuthParamsDTO] = Field(default=None, alias="salesforceV2AuthParams")
    service_now_auth_params: Optional[ServiceNowAuthParamsDTO] = Field(default=None, alias="serviceNowAuthParams")
    service_now_v2_auth_params: Optional[ServiceNowV2AuthParamsDTO] = Field(default=None, alias="serviceNowV2AuthParams")
    slack_auth_params: Optional[SlackAuthParamsDTO] = Field(default=None, alias="slackAuthParams")
    snowflake_auth_params: Optional[SnowflakeAuthParamsDTO] = Field(default=None, alias="snowflakeAuthParams")
    sql_server_auth_params: Optional[SqlServerAuthParamsDTO] = Field(default=None, alias="sqlServerAuthParams")
    success_factors_auth_params: Optional[SuccessFactorsAuthParamsDTO] = Field(default=None, alias="successFactorsAuthParams")
    tenant_domain_name: Optional[StrictStr] = Field(default=None, alias="tenantDomainName")
    ultimate_auth_params: Optional[UltimateAuthParamsDTO] = Field(default=None, alias="ultimateAuthParams")
    willow_auth_params: Optional[WillowAuthParamsDTO] = Field(default=None, alias="willowAuthParams")
    workday_auth_params: Optional[WorkdayAuthParamsDTO] = Field(default=None, alias="workdayAuthParams")
    workday_raas_auth_params: Optional[WorkdayRaasAuthParamsDTO] = Field(default=None, alias="workdayRaasAuthParams")
    zoom_auth_params: Optional[ZoomAuthParamsDTO] = Field(default=None, alias="zoomAuthParams")
    __properties: ClassVar[List[str]] = ["adpAuthParams", "authContext", "bambooAuthParams", "bigQueryAuthParams", "copyS3AuthParams", "dayforceV2AuthParams", "dimensionsAuthParams", "emptyAuthParams", "fusionAuthParams", "gongAuthParams", "googleSheetsAuthParams", "googleWorkspaceAuthParams", "greenhouseAuthParams", "hasUpdates", "icimsAuthParams", "internalS3AuthParams", "jdbcAuthParams", "jiraAuthParams", "leverAuthParams", "medalliaAuthParams", "ms365AuthParams", "mySqlAuthParams", "namelyAuthParams", "oracleDbAuthParams", "provider", "qualtricsAuthParams", "redshiftAuthParams", "s3AuthParams", "salesforceAuthParams", "salesforceV2AuthParams", "serviceNowAuthParams", "serviceNowV2AuthParams", "slackAuthParams", "snowflakeAuthParams", "sqlServerAuthParams", "successFactorsAuthParams", "tenantDomainName", "ultimateAuthParams", "willowAuthParams", "workdayAuthParams", "workdayRaasAuthParams", "zoomAuthParams"]

    @field_validator('auth_context')
    def auth_context_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['DefaultDataExtraction', 'WorkplaceDynamicsDataExtraction', 'Notification']):
            raise ValueError("must be one of enum values ('DefaultDataExtraction', 'WorkplaceDynamicsDataExtraction', 'Notification')")
        return value

    @field_validator('provider')
    def provider_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['Bamboo', 'GoogleSheets', 'Greenhouse', 'Jira', 'Lever', 'Namely', 'Qualtrics', 'Salesforce', 'UKG', 'Workday', 'Icims', 'ServiceNow', 'Jdbc', 'BasicS3', 'InternalS3', 'CopyS3', 'Redshift', 'Snowflake', 'BigQuery', 'SqlServer', 'Dimensions', 'IcimsPartnerProviderRedshift', 'Willow', 'SuccessFactors', 'IcimsV2', 'ADP', 'WorkdayV2', 'ServiceNowV2', 'Medallia', 'Fusion', 'SalesforceV2', 'Gong', 'Zoom', 'GoogleCalendar', 'UKGV2', 'DayforceV2', 'GoogleActivityReport', 'Slack', 'MySql', 'WorkdayRaas', 'Microsoft365', 'GoogleWorkspace', 'OracleDb', 'SmartRecruiters', 'WorkdayWQL', 'OEMCornerstone']):
            raise ValueError("must be one of enum values ('Bamboo', 'GoogleSheets', 'Greenhouse', 'Jira', 'Lever', 'Namely', 'Qualtrics', 'Salesforce', 'UKG', 'Workday', 'Icims', 'ServiceNow', 'Jdbc', 'BasicS3', 'InternalS3', 'CopyS3', 'Redshift', 'Snowflake', 'BigQuery', 'SqlServer', 'Dimensions', 'IcimsPartnerProviderRedshift', 'Willow', 'SuccessFactors', 'IcimsV2', 'ADP', 'WorkdayV2', 'ServiceNowV2', 'Medallia', 'Fusion', 'SalesforceV2', 'Gong', 'Zoom', 'GoogleCalendar', 'UKGV2', 'DayforceV2', 'GoogleActivityReport', 'Slack', 'MySql', 'WorkdayRaas', 'Microsoft365', 'GoogleWorkspace', 'OracleDb', 'SmartRecruiters', 'WorkdayWQL', 'OEMCornerstone')")
        return value

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of DataProviderAuthParamsDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of adp_auth_params
        if self.adp_auth_params:
            _dict['adpAuthParams'] = self.adp_auth_params.to_dict()
        # override the default output from pydantic by calling `to_dict()` of bamboo_auth_params
        if self.bamboo_auth_params:
            _dict['bambooAuthParams'] = self.bamboo_auth_params.to_dict()
        # override the default output from pydantic by calling `to_dict()` of big_query_auth_params
        if self.big_query_auth_params:
            _dict['bigQueryAuthParams'] = self.big_query_auth_params.to_dict()
        # override the default output from pydantic by calling `to_dict()` of copy_s3_auth_params
        if self.copy_s3_auth_params:
            _dict['copyS3AuthParams'] = self.copy_s3_auth_params.to_dict()
        # override the default output from pydantic by calling `to_dict()` of dayforce_v2_auth_params
        if self.dayforce_v2_auth_params:
            _dict['dayforceV2AuthParams'] = self.dayforce_v2_auth_params.to_dict()
        # override the default output from pydantic by calling `to_dict()` of dimensions_auth_params
        if self.dimensions_auth_params:
            _dict['dimensionsAuthParams'] = self.dimensions_auth_params.to_dict()
        # override the default output from pydantic by calling `to_dict()` of fusion_auth_params
        if self.fusion_auth_params:
            _dict['fusionAuthParams'] = self.fusion_auth_params.to_dict()
        # override the default output from pydantic by calling `to_dict()` of gong_auth_params
        if self.gong_auth_params:
            _dict['gongAuthParams'] = self.gong_auth_params.to_dict()
        # override the default output from pydantic by calling `to_dict()` of google_sheets_auth_params
        if self.google_sheets_auth_params:
            _dict['googleSheetsAuthParams'] = self.google_sheets_auth_params.to_dict()
        # override the default output from pydantic by calling `to_dict()` of google_workspace_auth_params
        if self.google_workspace_auth_params:
            _dict['googleWorkspaceAuthParams'] = self.google_workspace_auth_params.to_dict()
        # override the default output from pydantic by calling `to_dict()` of greenhouse_auth_params
        if self.greenhouse_auth_params:
            _dict['greenhouseAuthParams'] = self.greenhouse_auth_params.to_dict()
        # override the default output from pydantic by calling `to_dict()` of icims_auth_params
        if self.icims_auth_params:
            _dict['icimsAuthParams'] = self.icims_auth_params.to_dict()
        # override the default output from pydantic by calling `to_dict()` of internal_s3_auth_params
        if self.internal_s3_auth_params:
            _dict['internalS3AuthParams'] = self.internal_s3_auth_params.to_dict()
        # override the default output from pydantic by calling `to_dict()` of jdbc_auth_params
        if self.jdbc_auth_params:
            _dict['jdbcAuthParams'] = self.jdbc_auth_params.to_dict()
        # override the default output from pydantic by calling `to_dict()` of jira_auth_params
        if self.jira_auth_params:
            _dict['jiraAuthParams'] = self.jira_auth_params.to_dict()
        # override the default output from pydantic by calling `to_dict()` of lever_auth_params
        if self.lever_auth_params:
            _dict['leverAuthParams'] = self.lever_auth_params.to_dict()
        # override the default output from pydantic by calling `to_dict()` of medallia_auth_params
        if self.medallia_auth_params:
            _dict['medalliaAuthParams'] = self.medallia_auth_params.to_dict()
        # override the default output from pydantic by calling `to_dict()` of ms365_auth_params
        if self.ms365_auth_params:
            _dict['ms365AuthParams'] = self.ms365_auth_params.to_dict()
        # override the default output from pydantic by calling `to_dict()` of my_sql_auth_params
        if self.my_sql_auth_params:
            _dict['mySqlAuthParams'] = self.my_sql_auth_params.to_dict()
        # override the default output from pydantic by calling `to_dict()` of namely_auth_params
        if self.namely_auth_params:
            _dict['namelyAuthParams'] = self.namely_auth_params.to_dict()
        # override the default output from pydantic by calling `to_dict()` of oracle_db_auth_params
        if self.oracle_db_auth_params:
            _dict['oracleDbAuthParams'] = self.oracle_db_auth_params.to_dict()
        # override the default output from pydantic by calling `to_dict()` of qualtrics_auth_params
        if self.qualtrics_auth_params:
            _dict['qualtricsAuthParams'] = self.qualtrics_auth_params.to_dict()
        # override the default output from pydantic by calling `to_dict()` of redshift_auth_params
        if self.redshift_auth_params:
            _dict['redshiftAuthParams'] = self.redshift_auth_params.to_dict()
        # override the default output from pydantic by calling `to_dict()` of s3_auth_params
        if self.s3_auth_params:
            _dict['s3AuthParams'] = self.s3_auth_params.to_dict()
        # override the default output from pydantic by calling `to_dict()` of salesforce_auth_params
        if self.salesforce_auth_params:
            _dict['salesforceAuthParams'] = self.salesforce_auth_params.to_dict()
        # override the default output from pydantic by calling `to_dict()` of salesforce_v2_auth_params
        if self.salesforce_v2_auth_params:
            _dict['salesforceV2AuthParams'] = self.salesforce_v2_auth_params.to_dict()
        # override the default output from pydantic by calling `to_dict()` of service_now_auth_params
        if self.service_now_auth_params:
            _dict['serviceNowAuthParams'] = self.service_now_auth_params.to_dict()
        # override the default output from pydantic by calling `to_dict()` of service_now_v2_auth_params
        if self.service_now_v2_auth_params:
            _dict['serviceNowV2AuthParams'] = self.service_now_v2_auth_params.to_dict()
        # override the default output from pydantic by calling `to_dict()` of slack_auth_params
        if self.slack_auth_params:
            _dict['slackAuthParams'] = self.slack_auth_params.to_dict()
        # override the default output from pydantic by calling `to_dict()` of snowflake_auth_params
        if self.snowflake_auth_params:
            _dict['snowflakeAuthParams'] = self.snowflake_auth_params.to_dict()
        # override the default output from pydantic by calling `to_dict()` of sql_server_auth_params
        if self.sql_server_auth_params:
            _dict['sqlServerAuthParams'] = self.sql_server_auth_params.to_dict()
        # override the default output from pydantic by calling `to_dict()` of success_factors_auth_params
        if self.success_factors_auth_params:
            _dict['successFactorsAuthParams'] = self.success_factors_auth_params.to_dict()
        # override the default output from pydantic by calling `to_dict()` of ultimate_auth_params
        if self.ultimate_auth_params:
            _dict['ultimateAuthParams'] = self.ultimate_auth_params.to_dict()
        # override the default output from pydantic by calling `to_dict()` of willow_auth_params
        if self.willow_auth_params:
            _dict['willowAuthParams'] = self.willow_auth_params.to_dict()
        # override the default output from pydantic by calling `to_dict()` of workday_auth_params
        if self.workday_auth_params:
            _dict['workdayAuthParams'] = self.workday_auth_params.to_dict()
        # override the default output from pydantic by calling `to_dict()` of workday_raas_auth_params
        if self.workday_raas_auth_params:
            _dict['workdayRaasAuthParams'] = self.workday_raas_auth_params.to_dict()
        # override the default output from pydantic by calling `to_dict()` of zoom_auth_params
        if self.zoom_auth_params:
            _dict['zoomAuthParams'] = self.zoom_auth_params.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of DataProviderAuthParamsDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "adpAuthParams": AdpAuthParamsDTO.from_dict(obj["adpAuthParams"]) if obj.get("adpAuthParams") is not None else None,
            "authContext": obj.get("authContext"),
            "bambooAuthParams": BambooAuthParamsDTO.from_dict(obj["bambooAuthParams"]) if obj.get("bambooAuthParams") is not None else None,
            "bigQueryAuthParams": BigQueryAuthParamsDTO.from_dict(obj["bigQueryAuthParams"]) if obj.get("bigQueryAuthParams") is not None else None,
            "copyS3AuthParams": CopyS3AuthParamsDTO.from_dict(obj["copyS3AuthParams"]) if obj.get("copyS3AuthParams") is not None else None,
            "dayforceV2AuthParams": DayforceV2AuthParamsDTO.from_dict(obj["dayforceV2AuthParams"]) if obj.get("dayforceV2AuthParams") is not None else None,
            "dimensionsAuthParams": DimensionsAuthParamsDTO.from_dict(obj["dimensionsAuthParams"]) if obj.get("dimensionsAuthParams") is not None else None,
            "emptyAuthParams": obj.get("emptyAuthParams"),
            "fusionAuthParams": FusionAuthParamsDTO.from_dict(obj["fusionAuthParams"]) if obj.get("fusionAuthParams") is not None else None,
            "gongAuthParams": GongAuthParamsDTO.from_dict(obj["gongAuthParams"]) if obj.get("gongAuthParams") is not None else None,
            "googleSheetsAuthParams": GoogleSheetsAuthParamsDTO.from_dict(obj["googleSheetsAuthParams"]) if obj.get("googleSheetsAuthParams") is not None else None,
            "googleWorkspaceAuthParams": GoogleWorkspaceAuthParamsDTO.from_dict(obj["googleWorkspaceAuthParams"]) if obj.get("googleWorkspaceAuthParams") is not None else None,
            "greenhouseAuthParams": GreenhouseAuthParamsDTO.from_dict(obj["greenhouseAuthParams"]) if obj.get("greenhouseAuthParams") is not None else None,
            "hasUpdates": obj.get("hasUpdates"),
            "icimsAuthParams": IcimsAuthParamsDTO.from_dict(obj["icimsAuthParams"]) if obj.get("icimsAuthParams") is not None else None,
            "internalS3AuthParams": InternalS3AuthParamsDTO.from_dict(obj["internalS3AuthParams"]) if obj.get("internalS3AuthParams") is not None else None,
            "jdbcAuthParams": JdbcAuthParamsDTO.from_dict(obj["jdbcAuthParams"]) if obj.get("jdbcAuthParams") is not None else None,
            "jiraAuthParams": JiraAuthParamsDTO.from_dict(obj["jiraAuthParams"]) if obj.get("jiraAuthParams") is not None else None,
            "leverAuthParams": LeverAuthParamsDTO.from_dict(obj["leverAuthParams"]) if obj.get("leverAuthParams") is not None else None,
            "medalliaAuthParams": MedalliaAuthParamsDTO.from_dict(obj["medalliaAuthParams"]) if obj.get("medalliaAuthParams") is not None else None,
            "ms365AuthParams": Microsoft365AuthParamsDTO.from_dict(obj["ms365AuthParams"]) if obj.get("ms365AuthParams") is not None else None,
            "mySqlAuthParams": MySqlAuthParamsDTO.from_dict(obj["mySqlAuthParams"]) if obj.get("mySqlAuthParams") is not None else None,
            "namelyAuthParams": NamelyAuthParamsDTO.from_dict(obj["namelyAuthParams"]) if obj.get("namelyAuthParams") is not None else None,
            "oracleDbAuthParams": OracleDbAuthParamsDTO.from_dict(obj["oracleDbAuthParams"]) if obj.get("oracleDbAuthParams") is not None else None,
            "provider": obj.get("provider"),
            "qualtricsAuthParams": QualtricsAuthParamsDTO.from_dict(obj["qualtricsAuthParams"]) if obj.get("qualtricsAuthParams") is not None else None,
            "redshiftAuthParams": RedshiftAuthParamsDTO.from_dict(obj["redshiftAuthParams"]) if obj.get("redshiftAuthParams") is not None else None,
            "s3AuthParams": BasicS3AuthParamsDTO.from_dict(obj["s3AuthParams"]) if obj.get("s3AuthParams") is not None else None,
            "salesforceAuthParams": SalesforceAuthParamsDTO.from_dict(obj["salesforceAuthParams"]) if obj.get("salesforceAuthParams") is not None else None,
            "salesforceV2AuthParams": SalesforceV2AuthParamsDTO.from_dict(obj["salesforceV2AuthParams"]) if obj.get("salesforceV2AuthParams") is not None else None,
            "serviceNowAuthParams": ServiceNowAuthParamsDTO.from_dict(obj["serviceNowAuthParams"]) if obj.get("serviceNowAuthParams") is not None else None,
            "serviceNowV2AuthParams": ServiceNowV2AuthParamsDTO.from_dict(obj["serviceNowV2AuthParams"]) if obj.get("serviceNowV2AuthParams") is not None else None,
            "slackAuthParams": SlackAuthParamsDTO.from_dict(obj["slackAuthParams"]) if obj.get("slackAuthParams") is not None else None,
            "snowflakeAuthParams": SnowflakeAuthParamsDTO.from_dict(obj["snowflakeAuthParams"]) if obj.get("snowflakeAuthParams") is not None else None,
            "sqlServerAuthParams": SqlServerAuthParamsDTO.from_dict(obj["sqlServerAuthParams"]) if obj.get("sqlServerAuthParams") is not None else None,
            "successFactorsAuthParams": SuccessFactorsAuthParamsDTO.from_dict(obj["successFactorsAuthParams"]) if obj.get("successFactorsAuthParams") is not None else None,
            "tenantDomainName": obj.get("tenantDomainName"),
            "ultimateAuthParams": UltimateAuthParamsDTO.from_dict(obj["ultimateAuthParams"]) if obj.get("ultimateAuthParams") is not None else None,
            "willowAuthParams": WillowAuthParamsDTO.from_dict(obj["willowAuthParams"]) if obj.get("willowAuthParams") is not None else None,
            "workdayAuthParams": WorkdayAuthParamsDTO.from_dict(obj["workdayAuthParams"]) if obj.get("workdayAuthParams") is not None else None,
            "workdayRaasAuthParams": WorkdayRaasAuthParamsDTO.from_dict(obj["workdayRaasAuthParams"]) if obj.get("workdayRaasAuthParams") is not None else None,
            "zoomAuthParams": ZoomAuthParamsDTO.from_dict(obj["zoomAuthParams"]) if obj.get("zoomAuthParams") is not None else None
        })
        return _obj


