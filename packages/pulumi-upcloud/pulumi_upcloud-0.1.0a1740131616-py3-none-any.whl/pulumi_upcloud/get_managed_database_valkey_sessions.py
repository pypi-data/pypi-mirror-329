# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import sys
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
if sys.version_info >= (3, 11):
    from typing import NotRequired, TypedDict, TypeAlias
else:
    from typing_extensions import NotRequired, TypedDict, TypeAlias
from . import _utilities
from . import outputs
from ._inputs import *

__all__ = [
    'GetManagedDatabaseValkeySessionsResult',
    'AwaitableGetManagedDatabaseValkeySessionsResult',
    'get_managed_database_valkey_sessions',
    'get_managed_database_valkey_sessions_output',
]

@pulumi.output_type
class GetManagedDatabaseValkeySessionsResult:
    """
    A collection of values returned by getManagedDatabaseValkeySessions.
    """
    def __init__(__self__, id=None, limit=None, offset=None, order=None, service=None, sessions=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if limit and not isinstance(limit, int):
            raise TypeError("Expected argument 'limit' to be a int")
        pulumi.set(__self__, "limit", limit)
        if offset and not isinstance(offset, int):
            raise TypeError("Expected argument 'offset' to be a int")
        pulumi.set(__self__, "offset", offset)
        if order and not isinstance(order, str):
            raise TypeError("Expected argument 'order' to be a str")
        pulumi.set(__self__, "order", order)
        if service and not isinstance(service, str):
            raise TypeError("Expected argument 'service' to be a str")
        pulumi.set(__self__, "service", service)
        if sessions and not isinstance(sessions, list):
            raise TypeError("Expected argument 'sessions' to be a list")
        pulumi.set(__self__, "sessions", sessions)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def limit(self) -> Optional[int]:
        return pulumi.get(self, "limit")

    @property
    @pulumi.getter
    def offset(self) -> Optional[int]:
        return pulumi.get(self, "offset")

    @property
    @pulumi.getter
    def order(self) -> Optional[str]:
        return pulumi.get(self, "order")

    @property
    @pulumi.getter
    def service(self) -> str:
        return pulumi.get(self, "service")

    @property
    @pulumi.getter
    def sessions(self) -> Sequence['outputs.GetManagedDatabaseValkeySessionsSessionResult']:
        return pulumi.get(self, "sessions")


class AwaitableGetManagedDatabaseValkeySessionsResult(GetManagedDatabaseValkeySessionsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetManagedDatabaseValkeySessionsResult(
            id=self.id,
            limit=self.limit,
            offset=self.offset,
            order=self.order,
            service=self.service,
            sessions=self.sessions)


def get_managed_database_valkey_sessions(limit: Optional[int] = None,
                                         offset: Optional[int] = None,
                                         order: Optional[str] = None,
                                         service: Optional[str] = None,
                                         sessions: Optional[Sequence[Union['GetManagedDatabaseValkeySessionsSessionArgs', 'GetManagedDatabaseValkeySessionsSessionArgsDict']]] = None,
                                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetManagedDatabaseValkeySessionsResult:
    """
    Current sessions of a Valkey managed database

    ## Example Usage

    ```python
    import pulumi
    import pulumi_upcloud as upcloud

    # Use data source to gather a list of the active sessions for a Managed Valkey Database
    # Create a Managed Valkey resource
    example_managed_database_valkey = upcloud.ManagedDatabaseValkey("exampleManagedDatabaseValkey",
        title="example",
        plan="1x1xCPU-2GB",
        zone="fi-hel2")
    example_managed_database_valkey_sessions = upcloud.get_managed_database_valkey_sessions_output(service=example_managed_database_valkey.id)
    ```
    """
    __args__ = dict()
    __args__['limit'] = limit
    __args__['offset'] = offset
    __args__['order'] = order
    __args__['service'] = service
    __args__['sessions'] = sessions
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('upcloud:index/getManagedDatabaseValkeySessions:getManagedDatabaseValkeySessions', __args__, opts=opts, typ=GetManagedDatabaseValkeySessionsResult).value

    return AwaitableGetManagedDatabaseValkeySessionsResult(
        id=pulumi.get(__ret__, 'id'),
        limit=pulumi.get(__ret__, 'limit'),
        offset=pulumi.get(__ret__, 'offset'),
        order=pulumi.get(__ret__, 'order'),
        service=pulumi.get(__ret__, 'service'),
        sessions=pulumi.get(__ret__, 'sessions'))
def get_managed_database_valkey_sessions_output(limit: Optional[pulumi.Input[Optional[int]]] = None,
                                                offset: Optional[pulumi.Input[Optional[int]]] = None,
                                                order: Optional[pulumi.Input[Optional[str]]] = None,
                                                service: Optional[pulumi.Input[str]] = None,
                                                sessions: Optional[pulumi.Input[Optional[Sequence[Union['GetManagedDatabaseValkeySessionsSessionArgs', 'GetManagedDatabaseValkeySessionsSessionArgsDict']]]]] = None,
                                                opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetManagedDatabaseValkeySessionsResult]:
    """
    Current sessions of a Valkey managed database

    ## Example Usage

    ```python
    import pulumi
    import pulumi_upcloud as upcloud

    # Use data source to gather a list of the active sessions for a Managed Valkey Database
    # Create a Managed Valkey resource
    example_managed_database_valkey = upcloud.ManagedDatabaseValkey("exampleManagedDatabaseValkey",
        title="example",
        plan="1x1xCPU-2GB",
        zone="fi-hel2")
    example_managed_database_valkey_sessions = upcloud.get_managed_database_valkey_sessions_output(service=example_managed_database_valkey.id)
    ```
    """
    __args__ = dict()
    __args__['limit'] = limit
    __args__['offset'] = offset
    __args__['order'] = order
    __args__['service'] = service
    __args__['sessions'] = sessions
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('upcloud:index/getManagedDatabaseValkeySessions:getManagedDatabaseValkeySessions', __args__, opts=opts, typ=GetManagedDatabaseValkeySessionsResult)
    return __ret__.apply(lambda __response__: GetManagedDatabaseValkeySessionsResult(
        id=pulumi.get(__response__, 'id'),
        limit=pulumi.get(__response__, 'limit'),
        offset=pulumi.get(__response__, 'offset'),
        order=pulumi.get(__response__, 'order'),
        service=pulumi.get(__response__, 'service'),
        sessions=pulumi.get(__response__, 'sessions')))
