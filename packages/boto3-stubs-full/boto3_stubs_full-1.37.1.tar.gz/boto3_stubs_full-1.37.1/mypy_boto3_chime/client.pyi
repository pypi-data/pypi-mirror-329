"""
Type annotations for chime service Client.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_chime.client import ChimeClient

    session = Session()
    client: ChimeClient = session.client("chime")
    ```
"""

from __future__ import annotations

import sys
from typing import Any, overload

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import ListAccountsPaginator, ListUsersPaginator
from .type_defs import (
    AssociatePhoneNumbersWithVoiceConnectorGroupRequestTypeDef,
    AssociatePhoneNumbersWithVoiceConnectorGroupResponseTypeDef,
    AssociatePhoneNumbersWithVoiceConnectorRequestTypeDef,
    AssociatePhoneNumbersWithVoiceConnectorResponseTypeDef,
    AssociatePhoneNumberWithUserRequestTypeDef,
    AssociateSigninDelegateGroupsWithAccountRequestTypeDef,
    BatchCreateAttendeeRequestTypeDef,
    BatchCreateAttendeeResponseTypeDef,
    BatchCreateChannelMembershipRequestTypeDef,
    BatchCreateChannelMembershipResponseTypeDef,
    BatchCreateRoomMembershipRequestTypeDef,
    BatchCreateRoomMembershipResponseTypeDef,
    BatchDeletePhoneNumberRequestTypeDef,
    BatchDeletePhoneNumberResponseTypeDef,
    BatchSuspendUserRequestTypeDef,
    BatchSuspendUserResponseTypeDef,
    BatchUnsuspendUserRequestTypeDef,
    BatchUnsuspendUserResponseTypeDef,
    BatchUpdatePhoneNumberRequestTypeDef,
    BatchUpdatePhoneNumberResponseTypeDef,
    BatchUpdateUserRequestTypeDef,
    BatchUpdateUserResponseTypeDef,
    CreateAccountRequestTypeDef,
    CreateAccountResponseTypeDef,
    CreateAppInstanceAdminRequestTypeDef,
    CreateAppInstanceAdminResponseTypeDef,
    CreateAppInstanceRequestTypeDef,
    CreateAppInstanceResponseTypeDef,
    CreateAppInstanceUserRequestTypeDef,
    CreateAppInstanceUserResponseTypeDef,
    CreateAttendeeRequestTypeDef,
    CreateAttendeeResponseTypeDef,
    CreateBotRequestTypeDef,
    CreateBotResponseTypeDef,
    CreateChannelBanRequestTypeDef,
    CreateChannelBanResponseTypeDef,
    CreateChannelMembershipRequestTypeDef,
    CreateChannelMembershipResponseTypeDef,
    CreateChannelModeratorRequestTypeDef,
    CreateChannelModeratorResponseTypeDef,
    CreateChannelRequestTypeDef,
    CreateChannelResponseTypeDef,
    CreateMediaCapturePipelineRequestTypeDef,
    CreateMediaCapturePipelineResponseTypeDef,
    CreateMeetingDialOutRequestTypeDef,
    CreateMeetingDialOutResponseTypeDef,
    CreateMeetingRequestTypeDef,
    CreateMeetingResponseTypeDef,
    CreateMeetingWithAttendeesRequestTypeDef,
    CreateMeetingWithAttendeesResponseTypeDef,
    CreatePhoneNumberOrderRequestTypeDef,
    CreatePhoneNumberOrderResponseTypeDef,
    CreateProxySessionRequestTypeDef,
    CreateProxySessionResponseTypeDef,
    CreateRoomMembershipRequestTypeDef,
    CreateRoomMembershipResponseTypeDef,
    CreateRoomRequestTypeDef,
    CreateRoomResponseTypeDef,
    CreateSipMediaApplicationCallRequestTypeDef,
    CreateSipMediaApplicationCallResponseTypeDef,
    CreateSipMediaApplicationRequestTypeDef,
    CreateSipMediaApplicationResponseTypeDef,
    CreateSipRuleRequestTypeDef,
    CreateSipRuleResponseTypeDef,
    CreateUserRequestTypeDef,
    CreateUserResponseTypeDef,
    CreateVoiceConnectorGroupRequestTypeDef,
    CreateVoiceConnectorGroupResponseTypeDef,
    CreateVoiceConnectorRequestTypeDef,
    CreateVoiceConnectorResponseTypeDef,
    DeleteAccountRequestTypeDef,
    DeleteAppInstanceAdminRequestTypeDef,
    DeleteAppInstanceRequestTypeDef,
    DeleteAppInstanceStreamingConfigurationsRequestTypeDef,
    DeleteAppInstanceUserRequestTypeDef,
    DeleteAttendeeRequestTypeDef,
    DeleteChannelBanRequestTypeDef,
    DeleteChannelMembershipRequestTypeDef,
    DeleteChannelMessageRequestTypeDef,
    DeleteChannelModeratorRequestTypeDef,
    DeleteChannelRequestTypeDef,
    DeleteEventsConfigurationRequestTypeDef,
    DeleteMediaCapturePipelineRequestTypeDef,
    DeleteMeetingRequestTypeDef,
    DeletePhoneNumberRequestTypeDef,
    DeleteProxySessionRequestTypeDef,
    DeleteRoomMembershipRequestTypeDef,
    DeleteRoomRequestTypeDef,
    DeleteSipMediaApplicationRequestTypeDef,
    DeleteSipRuleRequestTypeDef,
    DeleteVoiceConnectorEmergencyCallingConfigurationRequestTypeDef,
    DeleteVoiceConnectorGroupRequestTypeDef,
    DeleteVoiceConnectorOriginationRequestTypeDef,
    DeleteVoiceConnectorProxyRequestTypeDef,
    DeleteVoiceConnectorRequestTypeDef,
    DeleteVoiceConnectorStreamingConfigurationRequestTypeDef,
    DeleteVoiceConnectorTerminationCredentialsRequestTypeDef,
    DeleteVoiceConnectorTerminationRequestTypeDef,
    DescribeAppInstanceAdminRequestTypeDef,
    DescribeAppInstanceAdminResponseTypeDef,
    DescribeAppInstanceRequestTypeDef,
    DescribeAppInstanceResponseTypeDef,
    DescribeAppInstanceUserRequestTypeDef,
    DescribeAppInstanceUserResponseTypeDef,
    DescribeChannelBanRequestTypeDef,
    DescribeChannelBanResponseTypeDef,
    DescribeChannelMembershipForAppInstanceUserRequestTypeDef,
    DescribeChannelMembershipForAppInstanceUserResponseTypeDef,
    DescribeChannelMembershipRequestTypeDef,
    DescribeChannelMembershipResponseTypeDef,
    DescribeChannelModeratedByAppInstanceUserRequestTypeDef,
    DescribeChannelModeratedByAppInstanceUserResponseTypeDef,
    DescribeChannelModeratorRequestTypeDef,
    DescribeChannelModeratorResponseTypeDef,
    DescribeChannelRequestTypeDef,
    DescribeChannelResponseTypeDef,
    DisassociatePhoneNumberFromUserRequestTypeDef,
    DisassociatePhoneNumbersFromVoiceConnectorGroupRequestTypeDef,
    DisassociatePhoneNumbersFromVoiceConnectorGroupResponseTypeDef,
    DisassociatePhoneNumbersFromVoiceConnectorRequestTypeDef,
    DisassociatePhoneNumbersFromVoiceConnectorResponseTypeDef,
    DisassociateSigninDelegateGroupsFromAccountRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    GetAccountRequestTypeDef,
    GetAccountResponseTypeDef,
    GetAccountSettingsRequestTypeDef,
    GetAccountSettingsResponseTypeDef,
    GetAppInstanceRetentionSettingsRequestTypeDef,
    GetAppInstanceRetentionSettingsResponseTypeDef,
    GetAppInstanceStreamingConfigurationsRequestTypeDef,
    GetAppInstanceStreamingConfigurationsResponseTypeDef,
    GetAttendeeRequestTypeDef,
    GetAttendeeResponseTypeDef,
    GetBotRequestTypeDef,
    GetBotResponseTypeDef,
    GetChannelMessageRequestTypeDef,
    GetChannelMessageResponseTypeDef,
    GetEventsConfigurationRequestTypeDef,
    GetEventsConfigurationResponseTypeDef,
    GetGlobalSettingsResponseTypeDef,
    GetMediaCapturePipelineRequestTypeDef,
    GetMediaCapturePipelineResponseTypeDef,
    GetMeetingRequestTypeDef,
    GetMeetingResponseTypeDef,
    GetMessagingSessionEndpointResponseTypeDef,
    GetPhoneNumberOrderRequestTypeDef,
    GetPhoneNumberOrderResponseTypeDef,
    GetPhoneNumberRequestTypeDef,
    GetPhoneNumberResponseTypeDef,
    GetPhoneNumberSettingsResponseTypeDef,
    GetProxySessionRequestTypeDef,
    GetProxySessionResponseTypeDef,
    GetRetentionSettingsRequestTypeDef,
    GetRetentionSettingsResponseTypeDef,
    GetRoomRequestTypeDef,
    GetRoomResponseTypeDef,
    GetSipMediaApplicationLoggingConfigurationRequestTypeDef,
    GetSipMediaApplicationLoggingConfigurationResponseTypeDef,
    GetSipMediaApplicationRequestTypeDef,
    GetSipMediaApplicationResponseTypeDef,
    GetSipRuleRequestTypeDef,
    GetSipRuleResponseTypeDef,
    GetUserRequestTypeDef,
    GetUserResponseTypeDef,
    GetUserSettingsRequestTypeDef,
    GetUserSettingsResponseTypeDef,
    GetVoiceConnectorEmergencyCallingConfigurationRequestTypeDef,
    GetVoiceConnectorEmergencyCallingConfigurationResponseTypeDef,
    GetVoiceConnectorGroupRequestTypeDef,
    GetVoiceConnectorGroupResponseTypeDef,
    GetVoiceConnectorLoggingConfigurationRequestTypeDef,
    GetVoiceConnectorLoggingConfigurationResponseTypeDef,
    GetVoiceConnectorOriginationRequestTypeDef,
    GetVoiceConnectorOriginationResponseTypeDef,
    GetVoiceConnectorProxyRequestTypeDef,
    GetVoiceConnectorProxyResponseTypeDef,
    GetVoiceConnectorRequestTypeDef,
    GetVoiceConnectorResponseTypeDef,
    GetVoiceConnectorStreamingConfigurationRequestTypeDef,
    GetVoiceConnectorStreamingConfigurationResponseTypeDef,
    GetVoiceConnectorTerminationHealthRequestTypeDef,
    GetVoiceConnectorTerminationHealthResponseTypeDef,
    GetVoiceConnectorTerminationRequestTypeDef,
    GetVoiceConnectorTerminationResponseTypeDef,
    InviteUsersRequestTypeDef,
    InviteUsersResponseTypeDef,
    ListAccountsRequestTypeDef,
    ListAccountsResponseTypeDef,
    ListAppInstanceAdminsRequestTypeDef,
    ListAppInstanceAdminsResponseTypeDef,
    ListAppInstancesRequestTypeDef,
    ListAppInstancesResponseTypeDef,
    ListAppInstanceUsersRequestTypeDef,
    ListAppInstanceUsersResponseTypeDef,
    ListAttendeesRequestTypeDef,
    ListAttendeesResponseTypeDef,
    ListAttendeeTagsRequestTypeDef,
    ListAttendeeTagsResponseTypeDef,
    ListBotsRequestTypeDef,
    ListBotsResponseTypeDef,
    ListChannelBansRequestTypeDef,
    ListChannelBansResponseTypeDef,
    ListChannelMembershipsForAppInstanceUserRequestTypeDef,
    ListChannelMembershipsForAppInstanceUserResponseTypeDef,
    ListChannelMembershipsRequestTypeDef,
    ListChannelMembershipsResponseTypeDef,
    ListChannelMessagesRequestTypeDef,
    ListChannelMessagesResponseTypeDef,
    ListChannelModeratorsRequestTypeDef,
    ListChannelModeratorsResponseTypeDef,
    ListChannelsModeratedByAppInstanceUserRequestTypeDef,
    ListChannelsModeratedByAppInstanceUserResponseTypeDef,
    ListChannelsRequestTypeDef,
    ListChannelsResponseTypeDef,
    ListMediaCapturePipelinesRequestTypeDef,
    ListMediaCapturePipelinesResponseTypeDef,
    ListMeetingsRequestTypeDef,
    ListMeetingsResponseTypeDef,
    ListMeetingTagsRequestTypeDef,
    ListMeetingTagsResponseTypeDef,
    ListPhoneNumberOrdersRequestTypeDef,
    ListPhoneNumberOrdersResponseTypeDef,
    ListPhoneNumbersRequestTypeDef,
    ListPhoneNumbersResponseTypeDef,
    ListProxySessionsRequestTypeDef,
    ListProxySessionsResponseTypeDef,
    ListRoomMembershipsRequestTypeDef,
    ListRoomMembershipsResponseTypeDef,
    ListRoomsRequestTypeDef,
    ListRoomsResponseTypeDef,
    ListSipMediaApplicationsRequestTypeDef,
    ListSipMediaApplicationsResponseTypeDef,
    ListSipRulesRequestTypeDef,
    ListSipRulesResponseTypeDef,
    ListSupportedPhoneNumberCountriesRequestTypeDef,
    ListSupportedPhoneNumberCountriesResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListUsersRequestTypeDef,
    ListUsersResponseTypeDef,
    ListVoiceConnectorGroupsRequestTypeDef,
    ListVoiceConnectorGroupsResponseTypeDef,
    ListVoiceConnectorsRequestTypeDef,
    ListVoiceConnectorsResponseTypeDef,
    ListVoiceConnectorTerminationCredentialsRequestTypeDef,
    ListVoiceConnectorTerminationCredentialsResponseTypeDef,
    LogoutUserRequestTypeDef,
    PutAppInstanceRetentionSettingsRequestTypeDef,
    PutAppInstanceRetentionSettingsResponseTypeDef,
    PutAppInstanceStreamingConfigurationsRequestTypeDef,
    PutAppInstanceStreamingConfigurationsResponseTypeDef,
    PutEventsConfigurationRequestTypeDef,
    PutEventsConfigurationResponseTypeDef,
    PutRetentionSettingsRequestTypeDef,
    PutRetentionSettingsResponseTypeDef,
    PutSipMediaApplicationLoggingConfigurationRequestTypeDef,
    PutSipMediaApplicationLoggingConfigurationResponseTypeDef,
    PutVoiceConnectorEmergencyCallingConfigurationRequestTypeDef,
    PutVoiceConnectorEmergencyCallingConfigurationResponseTypeDef,
    PutVoiceConnectorLoggingConfigurationRequestTypeDef,
    PutVoiceConnectorLoggingConfigurationResponseTypeDef,
    PutVoiceConnectorOriginationRequestTypeDef,
    PutVoiceConnectorOriginationResponseTypeDef,
    PutVoiceConnectorProxyRequestTypeDef,
    PutVoiceConnectorProxyResponseTypeDef,
    PutVoiceConnectorStreamingConfigurationRequestTypeDef,
    PutVoiceConnectorStreamingConfigurationResponseTypeDef,
    PutVoiceConnectorTerminationCredentialsRequestTypeDef,
    PutVoiceConnectorTerminationRequestTypeDef,
    PutVoiceConnectorTerminationResponseTypeDef,
    RedactChannelMessageRequestTypeDef,
    RedactChannelMessageResponseTypeDef,
    RedactConversationMessageRequestTypeDef,
    RedactRoomMessageRequestTypeDef,
    RegenerateSecurityTokenRequestTypeDef,
    RegenerateSecurityTokenResponseTypeDef,
    ResetPersonalPINRequestTypeDef,
    ResetPersonalPINResponseTypeDef,
    RestorePhoneNumberRequestTypeDef,
    RestorePhoneNumberResponseTypeDef,
    SearchAvailablePhoneNumbersRequestTypeDef,
    SearchAvailablePhoneNumbersResponseTypeDef,
    SendChannelMessageRequestTypeDef,
    SendChannelMessageResponseTypeDef,
    StartMeetingTranscriptionRequestTypeDef,
    StopMeetingTranscriptionRequestTypeDef,
    TagAttendeeRequestTypeDef,
    TagMeetingRequestTypeDef,
    TagResourceRequestTypeDef,
    UntagAttendeeRequestTypeDef,
    UntagMeetingRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateAccountRequestTypeDef,
    UpdateAccountResponseTypeDef,
    UpdateAccountSettingsRequestTypeDef,
    UpdateAppInstanceRequestTypeDef,
    UpdateAppInstanceResponseTypeDef,
    UpdateAppInstanceUserRequestTypeDef,
    UpdateAppInstanceUserResponseTypeDef,
    UpdateBotRequestTypeDef,
    UpdateBotResponseTypeDef,
    UpdateChannelMessageRequestTypeDef,
    UpdateChannelMessageResponseTypeDef,
    UpdateChannelReadMarkerRequestTypeDef,
    UpdateChannelReadMarkerResponseTypeDef,
    UpdateChannelRequestTypeDef,
    UpdateChannelResponseTypeDef,
    UpdateGlobalSettingsRequestTypeDef,
    UpdatePhoneNumberRequestTypeDef,
    UpdatePhoneNumberResponseTypeDef,
    UpdatePhoneNumberSettingsRequestTypeDef,
    UpdateProxySessionRequestTypeDef,
    UpdateProxySessionResponseTypeDef,
    UpdateRoomMembershipRequestTypeDef,
    UpdateRoomMembershipResponseTypeDef,
    UpdateRoomRequestTypeDef,
    UpdateRoomResponseTypeDef,
    UpdateSipMediaApplicationCallRequestTypeDef,
    UpdateSipMediaApplicationCallResponseTypeDef,
    UpdateSipMediaApplicationRequestTypeDef,
    UpdateSipMediaApplicationResponseTypeDef,
    UpdateSipRuleRequestTypeDef,
    UpdateSipRuleResponseTypeDef,
    UpdateUserRequestTypeDef,
    UpdateUserResponseTypeDef,
    UpdateUserSettingsRequestTypeDef,
    UpdateVoiceConnectorGroupRequestTypeDef,
    UpdateVoiceConnectorGroupResponseTypeDef,
    UpdateVoiceConnectorRequestTypeDef,
    UpdateVoiceConnectorResponseTypeDef,
    ValidateE911AddressRequestTypeDef,
    ValidateE911AddressResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Dict, Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("ChimeClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ForbiddenException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    ResourceLimitExceededException: Type[BotocoreClientError]
    ServiceFailureException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    ThrottledClientException: Type[BotocoreClientError]
    UnauthorizedClientException: Type[BotocoreClientError]
    UnprocessableEntityException: Type[BotocoreClientError]

class ChimeClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ChimeClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#generate_presigned_url)
        """

    def associate_phone_number_with_user(
        self, **kwargs: Unpack[AssociatePhoneNumberWithUserRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Associates a phone number with the specified Amazon Chime user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/associate_phone_number_with_user.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#associate_phone_number_with_user)
        """

    def associate_phone_numbers_with_voice_connector(
        self, **kwargs: Unpack[AssociatePhoneNumbersWithVoiceConnectorRequestTypeDef]
    ) -> AssociatePhoneNumbersWithVoiceConnectorResponseTypeDef:
        """
        Associates phone numbers with the specified Amazon Chime Voice Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/associate_phone_numbers_with_voice_connector.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#associate_phone_numbers_with_voice_connector)
        """

    def associate_phone_numbers_with_voice_connector_group(
        self, **kwargs: Unpack[AssociatePhoneNumbersWithVoiceConnectorGroupRequestTypeDef]
    ) -> AssociatePhoneNumbersWithVoiceConnectorGroupResponseTypeDef:
        """
        Associates phone numbers with the specified Amazon Chime Voice Connector group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/associate_phone_numbers_with_voice_connector_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#associate_phone_numbers_with_voice_connector_group)
        """

    def associate_signin_delegate_groups_with_account(
        self, **kwargs: Unpack[AssociateSigninDelegateGroupsWithAccountRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Associates the specified sign-in delegate groups with the specified Amazon
        Chime account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/associate_signin_delegate_groups_with_account.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#associate_signin_delegate_groups_with_account)
        """

    def batch_create_attendee(
        self, **kwargs: Unpack[BatchCreateAttendeeRequestTypeDef]
    ) -> BatchCreateAttendeeResponseTypeDef:
        """
        Creates up to 100 new attendees for an active Amazon Chime SDK meeting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/batch_create_attendee.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#batch_create_attendee)
        """

    def batch_create_channel_membership(
        self, **kwargs: Unpack[BatchCreateChannelMembershipRequestTypeDef]
    ) -> BatchCreateChannelMembershipResponseTypeDef:
        """
        Adds a specified number of users to a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/batch_create_channel_membership.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#batch_create_channel_membership)
        """

    def batch_create_room_membership(
        self, **kwargs: Unpack[BatchCreateRoomMembershipRequestTypeDef]
    ) -> BatchCreateRoomMembershipResponseTypeDef:
        """
        Adds up to 50 members to a chat room in an Amazon Chime Enterprise account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/batch_create_room_membership.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#batch_create_room_membership)
        """

    def batch_delete_phone_number(
        self, **kwargs: Unpack[BatchDeletePhoneNumberRequestTypeDef]
    ) -> BatchDeletePhoneNumberResponseTypeDef:
        """
        Moves phone numbers into the <b>Deletion queue</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/batch_delete_phone_number.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#batch_delete_phone_number)
        """

    def batch_suspend_user(
        self, **kwargs: Unpack[BatchSuspendUserRequestTypeDef]
    ) -> BatchSuspendUserResponseTypeDef:
        """
        Suspends up to 50 users from a <code>Team</code> or <code>EnterpriseLWA</code>
        Amazon Chime account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/batch_suspend_user.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#batch_suspend_user)
        """

    def batch_unsuspend_user(
        self, **kwargs: Unpack[BatchUnsuspendUserRequestTypeDef]
    ) -> BatchUnsuspendUserResponseTypeDef:
        """
        Removes the suspension from up to 50 previously suspended users for the
        specified Amazon Chime <code>EnterpriseLWA</code> account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/batch_unsuspend_user.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#batch_unsuspend_user)
        """

    def batch_update_phone_number(
        self, **kwargs: Unpack[BatchUpdatePhoneNumberRequestTypeDef]
    ) -> BatchUpdatePhoneNumberResponseTypeDef:
        """
        Updates phone number product types or calling names.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/batch_update_phone_number.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#batch_update_phone_number)
        """

    def batch_update_user(
        self, **kwargs: Unpack[BatchUpdateUserRequestTypeDef]
    ) -> BatchUpdateUserResponseTypeDef:
        """
        Updates user details within the <a>UpdateUserRequestItem</a> object for up to
        20 users for the specified Amazon Chime account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/batch_update_user.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#batch_update_user)
        """

    def create_account(
        self, **kwargs: Unpack[CreateAccountRequestTypeDef]
    ) -> CreateAccountResponseTypeDef:
        """
        Creates an Amazon Chime account under the administrator's AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/create_account.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#create_account)
        """

    def create_app_instance(
        self, **kwargs: Unpack[CreateAppInstanceRequestTypeDef]
    ) -> CreateAppInstanceResponseTypeDef:
        """
        Creates an Amazon Chime SDK messaging <code>AppInstance</code> under an AWS
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/create_app_instance.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#create_app_instance)
        """

    def create_app_instance_admin(
        self, **kwargs: Unpack[CreateAppInstanceAdminRequestTypeDef]
    ) -> CreateAppInstanceAdminResponseTypeDef:
        """
        Promotes an <code>AppInstanceUser</code> to an <code>AppInstanceAdmin</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/create_app_instance_admin.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#create_app_instance_admin)
        """

    def create_app_instance_user(
        self, **kwargs: Unpack[CreateAppInstanceUserRequestTypeDef]
    ) -> CreateAppInstanceUserResponseTypeDef:
        """
        Creates a user under an Amazon Chime <code>AppInstance</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/create_app_instance_user.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#create_app_instance_user)
        """

    def create_attendee(
        self, **kwargs: Unpack[CreateAttendeeRequestTypeDef]
    ) -> CreateAttendeeResponseTypeDef:
        """
        Creates a new attendee for an active Amazon Chime SDK meeting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/create_attendee.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#create_attendee)
        """

    def create_bot(self, **kwargs: Unpack[CreateBotRequestTypeDef]) -> CreateBotResponseTypeDef:
        """
        Creates a bot for an Amazon Chime Enterprise account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/create_bot.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#create_bot)
        """

    def create_channel(
        self, **kwargs: Unpack[CreateChannelRequestTypeDef]
    ) -> CreateChannelResponseTypeDef:
        """
        Creates a channel to which you can add users and send messages.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/create_channel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#create_channel)
        """

    def create_channel_ban(
        self, **kwargs: Unpack[CreateChannelBanRequestTypeDef]
    ) -> CreateChannelBanResponseTypeDef:
        """
        Permanently bans a member from a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/create_channel_ban.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#create_channel_ban)
        """

    def create_channel_membership(
        self, **kwargs: Unpack[CreateChannelMembershipRequestTypeDef]
    ) -> CreateChannelMembershipResponseTypeDef:
        """
        Adds a user to a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/create_channel_membership.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#create_channel_membership)
        """

    def create_channel_moderator(
        self, **kwargs: Unpack[CreateChannelModeratorRequestTypeDef]
    ) -> CreateChannelModeratorResponseTypeDef:
        """
        Creates a new <code>ChannelModerator</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/create_channel_moderator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#create_channel_moderator)
        """

    def create_media_capture_pipeline(
        self, **kwargs: Unpack[CreateMediaCapturePipelineRequestTypeDef]
    ) -> CreateMediaCapturePipelineResponseTypeDef:
        """
        Creates a media capture pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/create_media_capture_pipeline.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#create_media_capture_pipeline)
        """

    def create_meeting(
        self, **kwargs: Unpack[CreateMeetingRequestTypeDef]
    ) -> CreateMeetingResponseTypeDef:
        """
        Creates a new Amazon Chime SDK meeting in the specified media Region with no
        initial attendees.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/create_meeting.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#create_meeting)
        """

    def create_meeting_dial_out(
        self, **kwargs: Unpack[CreateMeetingDialOutRequestTypeDef]
    ) -> CreateMeetingDialOutResponseTypeDef:
        """
        Uses the join token and call metadata in a meeting request (From number, To
        number, and so forth) to initiate an outbound call to a public switched
        telephone network (PSTN) and join them into a Chime meeting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/create_meeting_dial_out.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#create_meeting_dial_out)
        """

    def create_meeting_with_attendees(
        self, **kwargs: Unpack[CreateMeetingWithAttendeesRequestTypeDef]
    ) -> CreateMeetingWithAttendeesResponseTypeDef:
        """
        Creates a new Amazon Chime SDK meeting in the specified media Region, with
        attendees.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/create_meeting_with_attendees.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#create_meeting_with_attendees)
        """

    def create_phone_number_order(
        self, **kwargs: Unpack[CreatePhoneNumberOrderRequestTypeDef]
    ) -> CreatePhoneNumberOrderResponseTypeDef:
        """
        Creates an order for phone numbers to be provisioned.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/create_phone_number_order.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#create_phone_number_order)
        """

    def create_proxy_session(
        self, **kwargs: Unpack[CreateProxySessionRequestTypeDef]
    ) -> CreateProxySessionResponseTypeDef:
        """
        Creates a proxy session on the specified Amazon Chime Voice Connector for the
        specified participant phone numbers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/create_proxy_session.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#create_proxy_session)
        """

    def create_room(self, **kwargs: Unpack[CreateRoomRequestTypeDef]) -> CreateRoomResponseTypeDef:
        """
        Creates a chat room for the specified Amazon Chime Enterprise account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/create_room.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#create_room)
        """

    def create_room_membership(
        self, **kwargs: Unpack[CreateRoomMembershipRequestTypeDef]
    ) -> CreateRoomMembershipResponseTypeDef:
        """
        Adds a member to a chat room in an Amazon Chime Enterprise account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/create_room_membership.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#create_room_membership)
        """

    def create_sip_media_application(
        self, **kwargs: Unpack[CreateSipMediaApplicationRequestTypeDef]
    ) -> CreateSipMediaApplicationResponseTypeDef:
        """
        Creates a SIP media application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/create_sip_media_application.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#create_sip_media_application)
        """

    def create_sip_media_application_call(
        self, **kwargs: Unpack[CreateSipMediaApplicationCallRequestTypeDef]
    ) -> CreateSipMediaApplicationCallResponseTypeDef:
        """
        Creates an outbound call to a phone number from the phone number specified in
        the request, and it invokes the endpoint of the specified
        <code>sipMediaApplicationId</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/create_sip_media_application_call.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#create_sip_media_application_call)
        """

    def create_sip_rule(
        self, **kwargs: Unpack[CreateSipRuleRequestTypeDef]
    ) -> CreateSipRuleResponseTypeDef:
        """
        Creates a SIP rule which can be used to run a SIP media application as a target
        for a specific trigger type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/create_sip_rule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#create_sip_rule)
        """

    def create_user(self, **kwargs: Unpack[CreateUserRequestTypeDef]) -> CreateUserResponseTypeDef:
        """
        Creates a user under the specified Amazon Chime account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/create_user.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#create_user)
        """

    def create_voice_connector(
        self, **kwargs: Unpack[CreateVoiceConnectorRequestTypeDef]
    ) -> CreateVoiceConnectorResponseTypeDef:
        """
        Creates an Amazon Chime Voice Connector under the administrator's AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/create_voice_connector.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#create_voice_connector)
        """

    def create_voice_connector_group(
        self, **kwargs: Unpack[CreateVoiceConnectorGroupRequestTypeDef]
    ) -> CreateVoiceConnectorGroupResponseTypeDef:
        """
        Creates an Amazon Chime Voice Connector group under the administrator's AWS
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/create_voice_connector_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#create_voice_connector_group)
        """

    def delete_account(self, **kwargs: Unpack[DeleteAccountRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes the specified Amazon Chime account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_account.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#delete_account)
        """

    def delete_app_instance(
        self, **kwargs: Unpack[DeleteAppInstanceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an <code>AppInstance</code> and all associated data asynchronously.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_app_instance.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#delete_app_instance)
        """

    def delete_app_instance_admin(
        self, **kwargs: Unpack[DeleteAppInstanceAdminRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Demotes an <code>AppInstanceAdmin</code> to an <code>AppInstanceUser</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_app_instance_admin.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#delete_app_instance_admin)
        """

    def delete_app_instance_streaming_configurations(
        self, **kwargs: Unpack[DeleteAppInstanceStreamingConfigurationsRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the streaming configurations of an <code>AppInstance</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_app_instance_streaming_configurations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#delete_app_instance_streaming_configurations)
        """

    def delete_app_instance_user(
        self, **kwargs: Unpack[DeleteAppInstanceUserRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an <code>AppInstanceUser</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_app_instance_user.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#delete_app_instance_user)
        """

    def delete_attendee(
        self, **kwargs: Unpack[DeleteAttendeeRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an attendee from the specified Amazon Chime SDK meeting and deletes
        their <code>JoinToken</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_attendee.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#delete_attendee)
        """

    def delete_channel(
        self, **kwargs: Unpack[DeleteChannelRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Immediately makes a channel and its memberships inaccessible and marks them for
        deletion.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_channel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#delete_channel)
        """

    def delete_channel_ban(
        self, **kwargs: Unpack[DeleteChannelBanRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes a user from a channel's ban list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_channel_ban.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#delete_channel_ban)
        """

    def delete_channel_membership(
        self, **kwargs: Unpack[DeleteChannelMembershipRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes a member from a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_channel_membership.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#delete_channel_membership)
        """

    def delete_channel_message(
        self, **kwargs: Unpack[DeleteChannelMessageRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a channel message.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_channel_message.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#delete_channel_message)
        """

    def delete_channel_moderator(
        self, **kwargs: Unpack[DeleteChannelModeratorRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a channel moderator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_channel_moderator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#delete_channel_moderator)
        """

    def delete_events_configuration(
        self, **kwargs: Unpack[DeleteEventsConfigurationRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the events configuration that allows a bot to receive outgoing events.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_events_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#delete_events_configuration)
        """

    def delete_media_capture_pipeline(
        self, **kwargs: Unpack[DeleteMediaCapturePipelineRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the media capture pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_media_capture_pipeline.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#delete_media_capture_pipeline)
        """

    def delete_meeting(
        self, **kwargs: Unpack[DeleteMeetingRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified Amazon Chime SDK meeting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_meeting.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#delete_meeting)
        """

    def delete_phone_number(
        self, **kwargs: Unpack[DeletePhoneNumberRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Moves the specified phone number into the <b>Deletion queue</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_phone_number.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#delete_phone_number)
        """

    def delete_proxy_session(
        self, **kwargs: Unpack[DeleteProxySessionRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified proxy session from the specified Amazon Chime Voice
        Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_proxy_session.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#delete_proxy_session)
        """

    def delete_room(
        self, **kwargs: Unpack[DeleteRoomRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a chat room in an Amazon Chime Enterprise account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_room.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#delete_room)
        """

    def delete_room_membership(
        self, **kwargs: Unpack[DeleteRoomMembershipRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes a member from a chat room in an Amazon Chime Enterprise account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_room_membership.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#delete_room_membership)
        """

    def delete_sip_media_application(
        self, **kwargs: Unpack[DeleteSipMediaApplicationRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a SIP media application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_sip_media_application.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#delete_sip_media_application)
        """

    def delete_sip_rule(
        self, **kwargs: Unpack[DeleteSipRuleRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a SIP rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_sip_rule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#delete_sip_rule)
        """

    def delete_voice_connector(
        self, **kwargs: Unpack[DeleteVoiceConnectorRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified Amazon Chime Voice Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_voice_connector.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#delete_voice_connector)
        """

    def delete_voice_connector_emergency_calling_configuration(
        self, **kwargs: Unpack[DeleteVoiceConnectorEmergencyCallingConfigurationRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the emergency calling configuration details from the specified Amazon
        Chime Voice Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_voice_connector_emergency_calling_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#delete_voice_connector_emergency_calling_configuration)
        """

    def delete_voice_connector_group(
        self, **kwargs: Unpack[DeleteVoiceConnectorGroupRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified Amazon Chime Voice Connector group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_voice_connector_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#delete_voice_connector_group)
        """

    def delete_voice_connector_origination(
        self, **kwargs: Unpack[DeleteVoiceConnectorOriginationRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the origination settings for the specified Amazon Chime Voice Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_voice_connector_origination.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#delete_voice_connector_origination)
        """

    def delete_voice_connector_proxy(
        self, **kwargs: Unpack[DeleteVoiceConnectorProxyRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the proxy configuration from the specified Amazon Chime Voice Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_voice_connector_proxy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#delete_voice_connector_proxy)
        """

    def delete_voice_connector_streaming_configuration(
        self, **kwargs: Unpack[DeleteVoiceConnectorStreamingConfigurationRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the streaming configuration for the specified Amazon Chime Voice
        Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_voice_connector_streaming_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#delete_voice_connector_streaming_configuration)
        """

    def delete_voice_connector_termination(
        self, **kwargs: Unpack[DeleteVoiceConnectorTerminationRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the termination settings for the specified Amazon Chime Voice Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_voice_connector_termination.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#delete_voice_connector_termination)
        """

    def delete_voice_connector_termination_credentials(
        self, **kwargs: Unpack[DeleteVoiceConnectorTerminationCredentialsRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified SIP credentials used by your equipment to authenticate
        during call termination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_voice_connector_termination_credentials.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#delete_voice_connector_termination_credentials)
        """

    def describe_app_instance(
        self, **kwargs: Unpack[DescribeAppInstanceRequestTypeDef]
    ) -> DescribeAppInstanceResponseTypeDef:
        """
        Returns the full details of an <code>AppInstance</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/describe_app_instance.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#describe_app_instance)
        """

    def describe_app_instance_admin(
        self, **kwargs: Unpack[DescribeAppInstanceAdminRequestTypeDef]
    ) -> DescribeAppInstanceAdminResponseTypeDef:
        """
        Returns the full details of an <code>AppInstanceAdmin</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/describe_app_instance_admin.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#describe_app_instance_admin)
        """

    def describe_app_instance_user(
        self, **kwargs: Unpack[DescribeAppInstanceUserRequestTypeDef]
    ) -> DescribeAppInstanceUserResponseTypeDef:
        """
        Returns the full details of an <code>AppInstanceUser</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/describe_app_instance_user.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#describe_app_instance_user)
        """

    def describe_channel(
        self, **kwargs: Unpack[DescribeChannelRequestTypeDef]
    ) -> DescribeChannelResponseTypeDef:
        """
        Returns the full details of a channel in an Amazon Chime
        <code>AppInstance</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/describe_channel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#describe_channel)
        """

    def describe_channel_ban(
        self, **kwargs: Unpack[DescribeChannelBanRequestTypeDef]
    ) -> DescribeChannelBanResponseTypeDef:
        """
        Returns the full details of a channel ban.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/describe_channel_ban.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#describe_channel_ban)
        """

    def describe_channel_membership(
        self, **kwargs: Unpack[DescribeChannelMembershipRequestTypeDef]
    ) -> DescribeChannelMembershipResponseTypeDef:
        """
        Returns the full details of a user's channel membership.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/describe_channel_membership.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#describe_channel_membership)
        """

    def describe_channel_membership_for_app_instance_user(
        self, **kwargs: Unpack[DescribeChannelMembershipForAppInstanceUserRequestTypeDef]
    ) -> DescribeChannelMembershipForAppInstanceUserResponseTypeDef:
        """
        Returns the details of a channel based on the membership of the specified
        <code>AppInstanceUser</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/describe_channel_membership_for_app_instance_user.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#describe_channel_membership_for_app_instance_user)
        """

    def describe_channel_moderated_by_app_instance_user(
        self, **kwargs: Unpack[DescribeChannelModeratedByAppInstanceUserRequestTypeDef]
    ) -> DescribeChannelModeratedByAppInstanceUserResponseTypeDef:
        """
        Returns the full details of a channel moderated by the specified
        <code>AppInstanceUser</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/describe_channel_moderated_by_app_instance_user.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#describe_channel_moderated_by_app_instance_user)
        """

    def describe_channel_moderator(
        self, **kwargs: Unpack[DescribeChannelModeratorRequestTypeDef]
    ) -> DescribeChannelModeratorResponseTypeDef:
        """
        Returns the full details of a single ChannelModerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/describe_channel_moderator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#describe_channel_moderator)
        """

    def disassociate_phone_number_from_user(
        self, **kwargs: Unpack[DisassociatePhoneNumberFromUserRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates the primary provisioned phone number from the specified Amazon
        Chime user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/disassociate_phone_number_from_user.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#disassociate_phone_number_from_user)
        """

    def disassociate_phone_numbers_from_voice_connector(
        self, **kwargs: Unpack[DisassociatePhoneNumbersFromVoiceConnectorRequestTypeDef]
    ) -> DisassociatePhoneNumbersFromVoiceConnectorResponseTypeDef:
        """
        Disassociates the specified phone numbers from the specified Amazon Chime Voice
        Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/disassociate_phone_numbers_from_voice_connector.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#disassociate_phone_numbers_from_voice_connector)
        """

    def disassociate_phone_numbers_from_voice_connector_group(
        self, **kwargs: Unpack[DisassociatePhoneNumbersFromVoiceConnectorGroupRequestTypeDef]
    ) -> DisassociatePhoneNumbersFromVoiceConnectorGroupResponseTypeDef:
        """
        Disassociates the specified phone numbers from the specified Amazon Chime Voice
        Connector group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/disassociate_phone_numbers_from_voice_connector_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#disassociate_phone_numbers_from_voice_connector_group)
        """

    def disassociate_signin_delegate_groups_from_account(
        self, **kwargs: Unpack[DisassociateSigninDelegateGroupsFromAccountRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates the specified sign-in delegate groups from the specified Amazon
        Chime account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/disassociate_signin_delegate_groups_from_account.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#disassociate_signin_delegate_groups_from_account)
        """

    def get_account(self, **kwargs: Unpack[GetAccountRequestTypeDef]) -> GetAccountResponseTypeDef:
        """
        Retrieves details for the specified Amazon Chime account, such as account type
        and supported licenses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_account.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#get_account)
        """

    def get_account_settings(
        self, **kwargs: Unpack[GetAccountSettingsRequestTypeDef]
    ) -> GetAccountSettingsResponseTypeDef:
        """
        Retrieves account settings for the specified Amazon Chime account ID, such as
        remote control and dialout settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_account_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#get_account_settings)
        """

    def get_app_instance_retention_settings(
        self, **kwargs: Unpack[GetAppInstanceRetentionSettingsRequestTypeDef]
    ) -> GetAppInstanceRetentionSettingsResponseTypeDef:
        """
        Gets the retention settings for an <code>AppInstance</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_app_instance_retention_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#get_app_instance_retention_settings)
        """

    def get_app_instance_streaming_configurations(
        self, **kwargs: Unpack[GetAppInstanceStreamingConfigurationsRequestTypeDef]
    ) -> GetAppInstanceStreamingConfigurationsResponseTypeDef:
        """
        Gets the streaming settings for an <code>AppInstance</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_app_instance_streaming_configurations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#get_app_instance_streaming_configurations)
        """

    def get_attendee(
        self, **kwargs: Unpack[GetAttendeeRequestTypeDef]
    ) -> GetAttendeeResponseTypeDef:
        """
        Gets the Amazon Chime SDK attendee details for a specified meeting ID and
        attendee ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_attendee.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#get_attendee)
        """

    def get_bot(self, **kwargs: Unpack[GetBotRequestTypeDef]) -> GetBotResponseTypeDef:
        """
        Retrieves details for the specified bot, such as bot email address, bot type,
        status, and display name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_bot.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#get_bot)
        """

    def get_channel_message(
        self, **kwargs: Unpack[GetChannelMessageRequestTypeDef]
    ) -> GetChannelMessageResponseTypeDef:
        """
        Gets the full details of a channel message.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_channel_message.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#get_channel_message)
        """

    def get_events_configuration(
        self, **kwargs: Unpack[GetEventsConfigurationRequestTypeDef]
    ) -> GetEventsConfigurationResponseTypeDef:
        """
        Gets details for an events configuration that allows a bot to receive outgoing
        events, such as an HTTPS endpoint or Lambda function ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_events_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#get_events_configuration)
        """

    def get_global_settings(self) -> GetGlobalSettingsResponseTypeDef:
        """
        Retrieves global settings for the administrator's AWS account, such as Amazon
        Chime Business Calling and Amazon Chime Voice Connector settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_global_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#get_global_settings)
        """

    def get_media_capture_pipeline(
        self, **kwargs: Unpack[GetMediaCapturePipelineRequestTypeDef]
    ) -> GetMediaCapturePipelineResponseTypeDef:
        """
        Gets an existing media capture pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_media_capture_pipeline.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#get_media_capture_pipeline)
        """

    def get_meeting(self, **kwargs: Unpack[GetMeetingRequestTypeDef]) -> GetMeetingResponseTypeDef:
        """
        <b>This API is is no longer supported and will not be updated.</b> We recommend
        using the latest version, <a
        href="https://docs.aws.amazon.com/chime-sdk/latest/APIReference/API_meeting-chime_GetMeeting.html">GetMeeting</a>,
        in the Amazon Chime SDK.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_meeting.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#get_meeting)
        """

    def get_messaging_session_endpoint(self) -> GetMessagingSessionEndpointResponseTypeDef:
        """
        The details of the endpoint for the messaging session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_messaging_session_endpoint.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#get_messaging_session_endpoint)
        """

    def get_phone_number(
        self, **kwargs: Unpack[GetPhoneNumberRequestTypeDef]
    ) -> GetPhoneNumberResponseTypeDef:
        """
        Retrieves details for the specified phone number ID, such as associations,
        capabilities, and product type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_phone_number.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#get_phone_number)
        """

    def get_phone_number_order(
        self, **kwargs: Unpack[GetPhoneNumberOrderRequestTypeDef]
    ) -> GetPhoneNumberOrderResponseTypeDef:
        """
        Retrieves details for the specified phone number order, such as the order
        creation timestamp, phone numbers in E.164 format, product type, and order
        status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_phone_number_order.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#get_phone_number_order)
        """

    def get_phone_number_settings(self) -> GetPhoneNumberSettingsResponseTypeDef:
        """
        Retrieves the phone number settings for the administrator's AWS account, such
        as the default outbound calling name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_phone_number_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#get_phone_number_settings)
        """

    def get_proxy_session(
        self, **kwargs: Unpack[GetProxySessionRequestTypeDef]
    ) -> GetProxySessionResponseTypeDef:
        """
        Gets the specified proxy session details for the specified Amazon Chime Voice
        Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_proxy_session.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#get_proxy_session)
        """

    def get_retention_settings(
        self, **kwargs: Unpack[GetRetentionSettingsRequestTypeDef]
    ) -> GetRetentionSettingsResponseTypeDef:
        """
        Gets the retention settings for the specified Amazon Chime Enterprise account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_retention_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#get_retention_settings)
        """

    def get_room(self, **kwargs: Unpack[GetRoomRequestTypeDef]) -> GetRoomResponseTypeDef:
        """
        Retrieves room details, such as the room name, for a room in an Amazon Chime
        Enterprise account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_room.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#get_room)
        """

    def get_sip_media_application(
        self, **kwargs: Unpack[GetSipMediaApplicationRequestTypeDef]
    ) -> GetSipMediaApplicationResponseTypeDef:
        """
        Retrieves the information for a SIP media application, including name, AWS
        Region, and endpoints.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_sip_media_application.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#get_sip_media_application)
        """

    def get_sip_media_application_logging_configuration(
        self, **kwargs: Unpack[GetSipMediaApplicationLoggingConfigurationRequestTypeDef]
    ) -> GetSipMediaApplicationLoggingConfigurationResponseTypeDef:
        """
        Returns the logging configuration for the specified SIP media application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_sip_media_application_logging_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#get_sip_media_application_logging_configuration)
        """

    def get_sip_rule(self, **kwargs: Unpack[GetSipRuleRequestTypeDef]) -> GetSipRuleResponseTypeDef:
        """
        Retrieves the details of a SIP rule, such as the rule ID, name, triggers, and
        target endpoints.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_sip_rule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#get_sip_rule)
        """

    def get_user(self, **kwargs: Unpack[GetUserRequestTypeDef]) -> GetUserResponseTypeDef:
        """
        Retrieves details for the specified user ID, such as primary email address,
        license type,and personal meeting PIN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_user.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#get_user)
        """

    def get_user_settings(
        self, **kwargs: Unpack[GetUserSettingsRequestTypeDef]
    ) -> GetUserSettingsResponseTypeDef:
        """
        Retrieves settings for the specified user ID, such as any associated phone
        number settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_user_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#get_user_settings)
        """

    def get_voice_connector(
        self, **kwargs: Unpack[GetVoiceConnectorRequestTypeDef]
    ) -> GetVoiceConnectorResponseTypeDef:
        """
        Retrieves details for the specified Amazon Chime Voice Connector, such as
        timestamps,name, outbound host, and encryption requirements.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_voice_connector.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#get_voice_connector)
        """

    def get_voice_connector_emergency_calling_configuration(
        self, **kwargs: Unpack[GetVoiceConnectorEmergencyCallingConfigurationRequestTypeDef]
    ) -> GetVoiceConnectorEmergencyCallingConfigurationResponseTypeDef:
        """
        Gets the emergency calling configuration details for the specified Amazon Chime
        Voice Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_voice_connector_emergency_calling_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#get_voice_connector_emergency_calling_configuration)
        """

    def get_voice_connector_group(
        self, **kwargs: Unpack[GetVoiceConnectorGroupRequestTypeDef]
    ) -> GetVoiceConnectorGroupResponseTypeDef:
        """
        Retrieves details for the specified Amazon Chime Voice Connector group, such as
        timestamps,name, and associated <code>VoiceConnectorItems</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_voice_connector_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#get_voice_connector_group)
        """

    def get_voice_connector_logging_configuration(
        self, **kwargs: Unpack[GetVoiceConnectorLoggingConfigurationRequestTypeDef]
    ) -> GetVoiceConnectorLoggingConfigurationResponseTypeDef:
        """
        Retrieves the logging configuration details for the specified Amazon Chime
        Voice Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_voice_connector_logging_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#get_voice_connector_logging_configuration)
        """

    def get_voice_connector_origination(
        self, **kwargs: Unpack[GetVoiceConnectorOriginationRequestTypeDef]
    ) -> GetVoiceConnectorOriginationResponseTypeDef:
        """
        Retrieves origination setting details for the specified Amazon Chime Voice
        Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_voice_connector_origination.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#get_voice_connector_origination)
        """

    def get_voice_connector_proxy(
        self, **kwargs: Unpack[GetVoiceConnectorProxyRequestTypeDef]
    ) -> GetVoiceConnectorProxyResponseTypeDef:
        """
        Gets the proxy configuration details for the specified Amazon Chime Voice
        Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_voice_connector_proxy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#get_voice_connector_proxy)
        """

    def get_voice_connector_streaming_configuration(
        self, **kwargs: Unpack[GetVoiceConnectorStreamingConfigurationRequestTypeDef]
    ) -> GetVoiceConnectorStreamingConfigurationResponseTypeDef:
        """
        Retrieves the streaming configuration details for the specified Amazon Chime
        Voice Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_voice_connector_streaming_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#get_voice_connector_streaming_configuration)
        """

    def get_voice_connector_termination(
        self, **kwargs: Unpack[GetVoiceConnectorTerminationRequestTypeDef]
    ) -> GetVoiceConnectorTerminationResponseTypeDef:
        """
        Retrieves termination setting details for the specified Amazon Chime Voice
        Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_voice_connector_termination.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#get_voice_connector_termination)
        """

    def get_voice_connector_termination_health(
        self, **kwargs: Unpack[GetVoiceConnectorTerminationHealthRequestTypeDef]
    ) -> GetVoiceConnectorTerminationHealthResponseTypeDef:
        """
        <b>This API is is no longer supported and will not be updated.</b> We recommend
        using the latest version, <a
        href="https://docs.aws.amazon.com/chime-sdk/latest/APIReference/API_voice-chime_GetVoiceConnectorTerminationHealth.html">GetVoiceConnectorTerminationHealth</a>,
        in the Amazon Chime SDK.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_voice_connector_termination_health.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#get_voice_connector_termination_health)
        """

    def invite_users(
        self, **kwargs: Unpack[InviteUsersRequestTypeDef]
    ) -> InviteUsersResponseTypeDef:
        """
        Sends email to a maximum of 50 users, inviting them to the specified Amazon
        Chime <code>Team</code> account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/invite_users.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#invite_users)
        """

    def list_accounts(
        self, **kwargs: Unpack[ListAccountsRequestTypeDef]
    ) -> ListAccountsResponseTypeDef:
        """
        Lists the Amazon Chime accounts under the administrator's AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_accounts.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#list_accounts)
        """

    def list_app_instance_admins(
        self, **kwargs: Unpack[ListAppInstanceAdminsRequestTypeDef]
    ) -> ListAppInstanceAdminsResponseTypeDef:
        """
        Returns a list of the administrators in the <code>AppInstance</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_app_instance_admins.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#list_app_instance_admins)
        """

    def list_app_instance_users(
        self, **kwargs: Unpack[ListAppInstanceUsersRequestTypeDef]
    ) -> ListAppInstanceUsersResponseTypeDef:
        """
        List all <code>AppInstanceUsers</code> created under a single
        <code>AppInstance</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_app_instance_users.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#list_app_instance_users)
        """

    def list_app_instances(
        self, **kwargs: Unpack[ListAppInstancesRequestTypeDef]
    ) -> ListAppInstancesResponseTypeDef:
        """
        Lists all Amazon Chime <code>AppInstance</code>s created under a single AWS
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_app_instances.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#list_app_instances)
        """

    def list_attendee_tags(
        self, **kwargs: Unpack[ListAttendeeTagsRequestTypeDef]
    ) -> ListAttendeeTagsResponseTypeDef:
        """
        Lists the tags applied to an Amazon Chime SDK attendee resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_attendee_tags.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#list_attendee_tags)
        """

    def list_attendees(
        self, **kwargs: Unpack[ListAttendeesRequestTypeDef]
    ) -> ListAttendeesResponseTypeDef:
        """
        Lists the attendees for the specified Amazon Chime SDK meeting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_attendees.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#list_attendees)
        """

    def list_bots(self, **kwargs: Unpack[ListBotsRequestTypeDef]) -> ListBotsResponseTypeDef:
        """
        Lists the bots associated with the administrator's Amazon Chime Enterprise
        account ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_bots.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#list_bots)
        """

    def list_channel_bans(
        self, **kwargs: Unpack[ListChannelBansRequestTypeDef]
    ) -> ListChannelBansResponseTypeDef:
        """
        Lists all the users banned from a particular channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_channel_bans.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#list_channel_bans)
        """

    def list_channel_memberships(
        self, **kwargs: Unpack[ListChannelMembershipsRequestTypeDef]
    ) -> ListChannelMembershipsResponseTypeDef:
        """
        Lists all channel memberships in a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_channel_memberships.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#list_channel_memberships)
        """

    def list_channel_memberships_for_app_instance_user(
        self, **kwargs: Unpack[ListChannelMembershipsForAppInstanceUserRequestTypeDef]
    ) -> ListChannelMembershipsForAppInstanceUserResponseTypeDef:
        """
        Lists all channels that a particular <code>AppInstanceUser</code> is a part of.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_channel_memberships_for_app_instance_user.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#list_channel_memberships_for_app_instance_user)
        """

    def list_channel_messages(
        self, **kwargs: Unpack[ListChannelMessagesRequestTypeDef]
    ) -> ListChannelMessagesResponseTypeDef:
        """
        List all the messages in a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_channel_messages.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#list_channel_messages)
        """

    def list_channel_moderators(
        self, **kwargs: Unpack[ListChannelModeratorsRequestTypeDef]
    ) -> ListChannelModeratorsResponseTypeDef:
        """
        Lists all the moderators for a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_channel_moderators.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#list_channel_moderators)
        """

    def list_channels(
        self, **kwargs: Unpack[ListChannelsRequestTypeDef]
    ) -> ListChannelsResponseTypeDef:
        """
        Lists all Channels created under a single Chime App as a paginated list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_channels.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#list_channels)
        """

    def list_channels_moderated_by_app_instance_user(
        self, **kwargs: Unpack[ListChannelsModeratedByAppInstanceUserRequestTypeDef]
    ) -> ListChannelsModeratedByAppInstanceUserResponseTypeDef:
        """
        A list of the channels moderated by an <code>AppInstanceUser</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_channels_moderated_by_app_instance_user.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#list_channels_moderated_by_app_instance_user)
        """

    def list_media_capture_pipelines(
        self, **kwargs: Unpack[ListMediaCapturePipelinesRequestTypeDef]
    ) -> ListMediaCapturePipelinesResponseTypeDef:
        """
        Returns a list of media capture pipelines.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_media_capture_pipelines.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#list_media_capture_pipelines)
        """

    def list_meeting_tags(
        self, **kwargs: Unpack[ListMeetingTagsRequestTypeDef]
    ) -> ListMeetingTagsResponseTypeDef:
        """
        Lists the tags applied to an Amazon Chime SDK meeting resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_meeting_tags.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#list_meeting_tags)
        """

    def list_meetings(
        self, **kwargs: Unpack[ListMeetingsRequestTypeDef]
    ) -> ListMeetingsResponseTypeDef:
        """
        Lists up to 100 active Amazon Chime SDK meetings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_meetings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#list_meetings)
        """

    def list_phone_number_orders(
        self, **kwargs: Unpack[ListPhoneNumberOrdersRequestTypeDef]
    ) -> ListPhoneNumberOrdersResponseTypeDef:
        """
        Lists the phone number orders for the administrator's Amazon Chime account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_phone_number_orders.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#list_phone_number_orders)
        """

    def list_phone_numbers(
        self, **kwargs: Unpack[ListPhoneNumbersRequestTypeDef]
    ) -> ListPhoneNumbersResponseTypeDef:
        """
        Lists the phone numbers for the specified Amazon Chime account, Amazon Chime
        user, Amazon Chime Voice Connector, or Amazon Chime Voice Connector group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_phone_numbers.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#list_phone_numbers)
        """

    def list_proxy_sessions(
        self, **kwargs: Unpack[ListProxySessionsRequestTypeDef]
    ) -> ListProxySessionsResponseTypeDef:
        """
        Lists the proxy sessions for the specified Amazon Chime Voice Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_proxy_sessions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#list_proxy_sessions)
        """

    def list_room_memberships(
        self, **kwargs: Unpack[ListRoomMembershipsRequestTypeDef]
    ) -> ListRoomMembershipsResponseTypeDef:
        """
        Lists the membership details for the specified room in an Amazon Chime
        Enterprise account, such as the members' IDs, email addresses, and names.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_room_memberships.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#list_room_memberships)
        """

    def list_rooms(self, **kwargs: Unpack[ListRoomsRequestTypeDef]) -> ListRoomsResponseTypeDef:
        """
        Lists the room details for the specified Amazon Chime Enterprise account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_rooms.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#list_rooms)
        """

    def list_sip_media_applications(
        self, **kwargs: Unpack[ListSipMediaApplicationsRequestTypeDef]
    ) -> ListSipMediaApplicationsResponseTypeDef:
        """
        Lists the SIP media applications under the administrator's AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_sip_media_applications.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#list_sip_media_applications)
        """

    def list_sip_rules(
        self, **kwargs: Unpack[ListSipRulesRequestTypeDef]
    ) -> ListSipRulesResponseTypeDef:
        """
        Lists the SIP rules under the administrator's AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_sip_rules.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#list_sip_rules)
        """

    def list_supported_phone_number_countries(
        self, **kwargs: Unpack[ListSupportedPhoneNumberCountriesRequestTypeDef]
    ) -> ListSupportedPhoneNumberCountriesResponseTypeDef:
        """
        Lists supported phone number countries.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_supported_phone_number_countries.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#list_supported_phone_number_countries)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags applied to an Amazon Chime SDK meeting and messaging resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#list_tags_for_resource)
        """

    def list_users(self, **kwargs: Unpack[ListUsersRequestTypeDef]) -> ListUsersResponseTypeDef:
        """
        Lists the users that belong to the specified Amazon Chime account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_users.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#list_users)
        """

    def list_voice_connector_groups(
        self, **kwargs: Unpack[ListVoiceConnectorGroupsRequestTypeDef]
    ) -> ListVoiceConnectorGroupsResponseTypeDef:
        """
        Lists the Amazon Chime Voice Connector groups for the administrator's AWS
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_voice_connector_groups.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#list_voice_connector_groups)
        """

    def list_voice_connector_termination_credentials(
        self, **kwargs: Unpack[ListVoiceConnectorTerminationCredentialsRequestTypeDef]
    ) -> ListVoiceConnectorTerminationCredentialsResponseTypeDef:
        """
        Lists the SIP credentials for the specified Amazon Chime Voice Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_voice_connector_termination_credentials.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#list_voice_connector_termination_credentials)
        """

    def list_voice_connectors(
        self, **kwargs: Unpack[ListVoiceConnectorsRequestTypeDef]
    ) -> ListVoiceConnectorsResponseTypeDef:
        """
        Lists the Amazon Chime Voice Connectors for the administrator's AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_voice_connectors.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#list_voice_connectors)
        """

    def logout_user(self, **kwargs: Unpack[LogoutUserRequestTypeDef]) -> Dict[str, Any]:
        """
        Logs out the specified user from all of the devices they are currently logged
        into.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/logout_user.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#logout_user)
        """

    def put_app_instance_retention_settings(
        self, **kwargs: Unpack[PutAppInstanceRetentionSettingsRequestTypeDef]
    ) -> PutAppInstanceRetentionSettingsResponseTypeDef:
        """
        Sets the amount of time in days that a given <code>AppInstance</code> retains
        data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/put_app_instance_retention_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#put_app_instance_retention_settings)
        """

    def put_app_instance_streaming_configurations(
        self, **kwargs: Unpack[PutAppInstanceStreamingConfigurationsRequestTypeDef]
    ) -> PutAppInstanceStreamingConfigurationsResponseTypeDef:
        """
        The data streaming configurations of an <code>AppInstance</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/put_app_instance_streaming_configurations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#put_app_instance_streaming_configurations)
        """

    def put_events_configuration(
        self, **kwargs: Unpack[PutEventsConfigurationRequestTypeDef]
    ) -> PutEventsConfigurationResponseTypeDef:
        """
        Creates an events configuration that allows a bot to receive outgoing events
        sent by Amazon Chime.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/put_events_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#put_events_configuration)
        """

    def put_retention_settings(
        self, **kwargs: Unpack[PutRetentionSettingsRequestTypeDef]
    ) -> PutRetentionSettingsResponseTypeDef:
        """
        Puts retention settings for the specified Amazon Chime Enterprise account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/put_retention_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#put_retention_settings)
        """

    def put_sip_media_application_logging_configuration(
        self, **kwargs: Unpack[PutSipMediaApplicationLoggingConfigurationRequestTypeDef]
    ) -> PutSipMediaApplicationLoggingConfigurationResponseTypeDef:
        """
        Updates the logging configuration for the specified SIP media application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/put_sip_media_application_logging_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#put_sip_media_application_logging_configuration)
        """

    def put_voice_connector_emergency_calling_configuration(
        self, **kwargs: Unpack[PutVoiceConnectorEmergencyCallingConfigurationRequestTypeDef]
    ) -> PutVoiceConnectorEmergencyCallingConfigurationResponseTypeDef:
        """
        Puts emergency calling configuration details to the specified Amazon Chime
        Voice Connector, such as emergency phone numbers and calling countries.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/put_voice_connector_emergency_calling_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#put_voice_connector_emergency_calling_configuration)
        """

    def put_voice_connector_logging_configuration(
        self, **kwargs: Unpack[PutVoiceConnectorLoggingConfigurationRequestTypeDef]
    ) -> PutVoiceConnectorLoggingConfigurationResponseTypeDef:
        """
        Adds a logging configuration for the specified Amazon Chime Voice Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/put_voice_connector_logging_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#put_voice_connector_logging_configuration)
        """

    def put_voice_connector_origination(
        self, **kwargs: Unpack[PutVoiceConnectorOriginationRequestTypeDef]
    ) -> PutVoiceConnectorOriginationResponseTypeDef:
        """
        Adds origination settings for the specified Amazon Chime Voice Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/put_voice_connector_origination.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#put_voice_connector_origination)
        """

    def put_voice_connector_proxy(
        self, **kwargs: Unpack[PutVoiceConnectorProxyRequestTypeDef]
    ) -> PutVoiceConnectorProxyResponseTypeDef:
        """
        Puts the specified proxy configuration to the specified Amazon Chime Voice
        Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/put_voice_connector_proxy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#put_voice_connector_proxy)
        """

    def put_voice_connector_streaming_configuration(
        self, **kwargs: Unpack[PutVoiceConnectorStreamingConfigurationRequestTypeDef]
    ) -> PutVoiceConnectorStreamingConfigurationResponseTypeDef:
        """
        Adds a streaming configuration for the specified Amazon Chime Voice Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/put_voice_connector_streaming_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#put_voice_connector_streaming_configuration)
        """

    def put_voice_connector_termination(
        self, **kwargs: Unpack[PutVoiceConnectorTerminationRequestTypeDef]
    ) -> PutVoiceConnectorTerminationResponseTypeDef:
        """
        Adds termination settings for the specified Amazon Chime Voice Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/put_voice_connector_termination.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#put_voice_connector_termination)
        """

    def put_voice_connector_termination_credentials(
        self, **kwargs: Unpack[PutVoiceConnectorTerminationCredentialsRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds termination SIP credentials for the specified Amazon Chime Voice Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/put_voice_connector_termination_credentials.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#put_voice_connector_termination_credentials)
        """

    def redact_channel_message(
        self, **kwargs: Unpack[RedactChannelMessageRequestTypeDef]
    ) -> RedactChannelMessageResponseTypeDef:
        """
        Redacts message content, but not metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/redact_channel_message.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#redact_channel_message)
        """

    def redact_conversation_message(
        self, **kwargs: Unpack[RedactConversationMessageRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Redacts the specified message from the specified Amazon Chime conversation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/redact_conversation_message.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#redact_conversation_message)
        """

    def redact_room_message(
        self, **kwargs: Unpack[RedactRoomMessageRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Redacts the specified message from the specified Amazon Chime channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/redact_room_message.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#redact_room_message)
        """

    def regenerate_security_token(
        self, **kwargs: Unpack[RegenerateSecurityTokenRequestTypeDef]
    ) -> RegenerateSecurityTokenResponseTypeDef:
        """
        Regenerates the security token for a bot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/regenerate_security_token.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#regenerate_security_token)
        """

    def reset_personal_pin(
        self, **kwargs: Unpack[ResetPersonalPINRequestTypeDef]
    ) -> ResetPersonalPINResponseTypeDef:
        """
        Resets the personal meeting PIN for the specified user on an Amazon Chime
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/reset_personal_pin.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#reset_personal_pin)
        """

    def restore_phone_number(
        self, **kwargs: Unpack[RestorePhoneNumberRequestTypeDef]
    ) -> RestorePhoneNumberResponseTypeDef:
        """
        Moves a phone number from the <b>Deletion queue</b> back into the phone number
        <b>Inventory</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/restore_phone_number.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#restore_phone_number)
        """

    def search_available_phone_numbers(
        self, **kwargs: Unpack[SearchAvailablePhoneNumbersRequestTypeDef]
    ) -> SearchAvailablePhoneNumbersResponseTypeDef:
        """
        Searches for phone numbers that can be ordered.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/search_available_phone_numbers.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#search_available_phone_numbers)
        """

    def send_channel_message(
        self, **kwargs: Unpack[SendChannelMessageRequestTypeDef]
    ) -> SendChannelMessageResponseTypeDef:
        """
        Sends a message to a particular channel that the member is a part of.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/send_channel_message.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#send_channel_message)
        """

    def start_meeting_transcription(
        self, **kwargs: Unpack[StartMeetingTranscriptionRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Starts transcription for the specified <code>meetingId</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/start_meeting_transcription.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#start_meeting_transcription)
        """

    def stop_meeting_transcription(
        self, **kwargs: Unpack[StopMeetingTranscriptionRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Stops transcription for the specified <code>meetingId</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/stop_meeting_transcription.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#stop_meeting_transcription)
        """

    def tag_attendee(
        self, **kwargs: Unpack[TagAttendeeRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Applies the specified tags to the specified Amazon Chime attendee.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/tag_attendee.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#tag_attendee)
        """

    def tag_meeting(
        self, **kwargs: Unpack[TagMeetingRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Applies the specified tags to the specified Amazon Chime SDK meeting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/tag_meeting.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#tag_meeting)
        """

    def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Applies the specified tags to the specified Amazon Chime SDK meeting resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#tag_resource)
        """

    def untag_attendee(
        self, **kwargs: Unpack[UntagAttendeeRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Untags the specified tags from the specified Amazon Chime SDK attendee.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/untag_attendee.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#untag_attendee)
        """

    def untag_meeting(
        self, **kwargs: Unpack[UntagMeetingRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Untags the specified tags from the specified Amazon Chime SDK meeting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/untag_meeting.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#untag_meeting)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Untags the specified tags from the specified Amazon Chime SDK meeting resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#untag_resource)
        """

    def update_account(
        self, **kwargs: Unpack[UpdateAccountRequestTypeDef]
    ) -> UpdateAccountResponseTypeDef:
        """
        Updates account details for the specified Amazon Chime account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/update_account.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#update_account)
        """

    def update_account_settings(
        self, **kwargs: Unpack[UpdateAccountSettingsRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the settings for the specified Amazon Chime account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/update_account_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#update_account_settings)
        """

    def update_app_instance(
        self, **kwargs: Unpack[UpdateAppInstanceRequestTypeDef]
    ) -> UpdateAppInstanceResponseTypeDef:
        """
        Updates <code>AppInstance</code> metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/update_app_instance.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#update_app_instance)
        """

    def update_app_instance_user(
        self, **kwargs: Unpack[UpdateAppInstanceUserRequestTypeDef]
    ) -> UpdateAppInstanceUserResponseTypeDef:
        """
        Updates the details of an <code>AppInstanceUser</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/update_app_instance_user.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#update_app_instance_user)
        """

    def update_bot(self, **kwargs: Unpack[UpdateBotRequestTypeDef]) -> UpdateBotResponseTypeDef:
        """
        Updates the status of the specified bot, such as starting or stopping the bot
        from running in your Amazon Chime Enterprise account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/update_bot.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#update_bot)
        """

    def update_channel(
        self, **kwargs: Unpack[UpdateChannelRequestTypeDef]
    ) -> UpdateChannelResponseTypeDef:
        """
        Update a channel's attributes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/update_channel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#update_channel)
        """

    def update_channel_message(
        self, **kwargs: Unpack[UpdateChannelMessageRequestTypeDef]
    ) -> UpdateChannelMessageResponseTypeDef:
        """
        Updates the content of a message.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/update_channel_message.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#update_channel_message)
        """

    def update_channel_read_marker(
        self, **kwargs: Unpack[UpdateChannelReadMarkerRequestTypeDef]
    ) -> UpdateChannelReadMarkerResponseTypeDef:
        """
        The details of the time when a user last read messages in a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/update_channel_read_marker.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#update_channel_read_marker)
        """

    def update_global_settings(
        self, **kwargs: Unpack[UpdateGlobalSettingsRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates global settings for the administrator's AWS account, such as Amazon
        Chime Business Calling and Amazon Chime Voice Connector settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/update_global_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#update_global_settings)
        """

    def update_phone_number(
        self, **kwargs: Unpack[UpdatePhoneNumberRequestTypeDef]
    ) -> UpdatePhoneNumberResponseTypeDef:
        """
        Updates phone number details, such as product type or calling name, for the
        specified phone number ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/update_phone_number.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#update_phone_number)
        """

    def update_phone_number_settings(
        self, **kwargs: Unpack[UpdatePhoneNumberSettingsRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the phone number settings for the administrator's AWS account, such as
        the default outbound calling name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/update_phone_number_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#update_phone_number_settings)
        """

    def update_proxy_session(
        self, **kwargs: Unpack[UpdateProxySessionRequestTypeDef]
    ) -> UpdateProxySessionResponseTypeDef:
        """
        Updates the specified proxy session details, such as voice or SMS capabilities.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/update_proxy_session.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#update_proxy_session)
        """

    def update_room(self, **kwargs: Unpack[UpdateRoomRequestTypeDef]) -> UpdateRoomResponseTypeDef:
        """
        Updates room details, such as the room name, for a room in an Amazon Chime
        Enterprise account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/update_room.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#update_room)
        """

    def update_room_membership(
        self, **kwargs: Unpack[UpdateRoomMembershipRequestTypeDef]
    ) -> UpdateRoomMembershipResponseTypeDef:
        """
        Updates room membership details, such as the member role, for a room in an
        Amazon Chime Enterprise account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/update_room_membership.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#update_room_membership)
        """

    def update_sip_media_application(
        self, **kwargs: Unpack[UpdateSipMediaApplicationRequestTypeDef]
    ) -> UpdateSipMediaApplicationResponseTypeDef:
        """
        Updates the details of the specified SIP media application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/update_sip_media_application.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#update_sip_media_application)
        """

    def update_sip_media_application_call(
        self, **kwargs: Unpack[UpdateSipMediaApplicationCallRequestTypeDef]
    ) -> UpdateSipMediaApplicationCallResponseTypeDef:
        """
        Invokes the AWS Lambda function associated with the SIP media application and
        transaction ID in an update request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/update_sip_media_application_call.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#update_sip_media_application_call)
        """

    def update_sip_rule(
        self, **kwargs: Unpack[UpdateSipRuleRequestTypeDef]
    ) -> UpdateSipRuleResponseTypeDef:
        """
        Updates the details of the specified SIP rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/update_sip_rule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#update_sip_rule)
        """

    def update_user(self, **kwargs: Unpack[UpdateUserRequestTypeDef]) -> UpdateUserResponseTypeDef:
        """
        Updates user details for a specified user ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/update_user.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#update_user)
        """

    def update_user_settings(
        self, **kwargs: Unpack[UpdateUserSettingsRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the settings for the specified user, such as phone number settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/update_user_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#update_user_settings)
        """

    def update_voice_connector(
        self, **kwargs: Unpack[UpdateVoiceConnectorRequestTypeDef]
    ) -> UpdateVoiceConnectorResponseTypeDef:
        """
        Updates details for the specified Amazon Chime Voice Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/update_voice_connector.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#update_voice_connector)
        """

    def update_voice_connector_group(
        self, **kwargs: Unpack[UpdateVoiceConnectorGroupRequestTypeDef]
    ) -> UpdateVoiceConnectorGroupResponseTypeDef:
        """
        Updates details of the specified Amazon Chime Voice Connector group, such as
        the name and Amazon Chime Voice Connector priority ranking.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/update_voice_connector_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#update_voice_connector_group)
        """

    def validate_e911_address(
        self, **kwargs: Unpack[ValidateE911AddressRequestTypeDef]
    ) -> ValidateE911AddressResponseTypeDef:
        """
        Validates an address to be used for 911 calls made with Amazon Chime Voice
        Connectors.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/validate_e911_address.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#validate_e911_address)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_accounts"]
    ) -> ListAccountsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_users"]
    ) -> ListUsersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime/client/#get_paginator)
        """
