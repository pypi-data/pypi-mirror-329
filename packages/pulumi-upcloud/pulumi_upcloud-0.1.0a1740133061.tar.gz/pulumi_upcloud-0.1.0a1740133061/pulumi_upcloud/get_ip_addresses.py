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
    'GetIpAddressesResult',
    'AwaitableGetIpAddressesResult',
    'get_ip_addresses',
    'get_ip_addresses_output',
]

@pulumi.output_type
class GetIpAddressesResult:
    """
    A collection of values returned by getIpAddresses.
    """
    def __init__(__self__, addresses=None, id=None):
        if addresses and not isinstance(addresses, list):
            raise TypeError("Expected argument 'addresses' to be a list")
        pulumi.set(__self__, "addresses", addresses)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def addresses(self) -> Optional[Sequence['outputs.GetIpAddressesAddressResult']]:
        return pulumi.get(self, "addresses")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        ID of the resource.
        """
        return pulumi.get(self, "id")


class AwaitableGetIpAddressesResult(GetIpAddressesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetIpAddressesResult(
            addresses=self.addresses,
            id=self.id)


def get_ip_addresses(addresses: Optional[Sequence[Union['GetIpAddressesAddressArgs', 'GetIpAddressesAddressArgsDict']]] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetIpAddressesResult:
    """
    Returns a set of IP Addresses that are associated with the UpCloud account.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_upcloud as upcloud

    all_ip_addresses = upcloud.get_ip_addresses()
    ```
    """
    __args__ = dict()
    __args__['addresses'] = addresses
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('upcloud:index/getIpAddresses:getIpAddresses', __args__, opts=opts, typ=GetIpAddressesResult).value

    return AwaitableGetIpAddressesResult(
        addresses=pulumi.get(__ret__, 'addresses'),
        id=pulumi.get(__ret__, 'id'))
def get_ip_addresses_output(addresses: Optional[pulumi.Input[Optional[Sequence[Union['GetIpAddressesAddressArgs', 'GetIpAddressesAddressArgsDict']]]]] = None,
                            opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetIpAddressesResult]:
    """
    Returns a set of IP Addresses that are associated with the UpCloud account.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_upcloud as upcloud

    all_ip_addresses = upcloud.get_ip_addresses()
    ```
    """
    __args__ = dict()
    __args__['addresses'] = addresses
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('upcloud:index/getIpAddresses:getIpAddresses', __args__, opts=opts, typ=GetIpAddressesResult)
    return __ret__.apply(lambda __response__: GetIpAddressesResult(
        addresses=pulumi.get(__response__, 'addresses'),
        id=pulumi.get(__response__, 'id')))
