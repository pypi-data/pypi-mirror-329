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

__all__ = [
    'GetZonesResult',
    'AwaitableGetZonesResult',
    'get_zones',
    'get_zones_output',
]

@pulumi.output_type
class GetZonesResult:
    """
    A collection of values returned by getZones.
    """
    def __init__(__self__, filter_type=None, id=None, zone_ids=None):
        if filter_type and not isinstance(filter_type, str):
            raise TypeError("Expected argument 'filter_type' to be a str")
        pulumi.set(__self__, "filter_type", filter_type)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if zone_ids and not isinstance(zone_ids, list):
            raise TypeError("Expected argument 'zone_ids' to be a list")
        pulumi.set(__self__, "zone_ids", zone_ids)

    @property
    @pulumi.getter(name="filterType")
    def filter_type(self) -> Optional[str]:
        return pulumi.get(self, "filter_type")

    @property
    @pulumi.getter
    def id(self) -> str:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="zoneIds")
    def zone_ids(self) -> Sequence[str]:
        return pulumi.get(self, "zone_ids")


class AwaitableGetZonesResult(GetZonesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetZonesResult(
            filter_type=self.filter_type,
            id=self.id,
            zone_ids=self.zone_ids)


def get_zones(filter_type: Optional[str] = None,
              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetZonesResult:
    """
    Returns a list of available UpCloud zones.
    """
    __args__ = dict()
    __args__['filterType'] = filter_type
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('upcloud:index/getZones:getZones', __args__, opts=opts, typ=GetZonesResult).value

    return AwaitableGetZonesResult(
        filter_type=pulumi.get(__ret__, 'filter_type'),
        id=pulumi.get(__ret__, 'id'),
        zone_ids=pulumi.get(__ret__, 'zone_ids'))
def get_zones_output(filter_type: Optional[pulumi.Input[Optional[str]]] = None,
                     opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetZonesResult]:
    """
    Returns a list of available UpCloud zones.
    """
    __args__ = dict()
    __args__['filterType'] = filter_type
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('upcloud:index/getZones:getZones', __args__, opts=opts, typ=GetZonesResult)
    return __ret__.apply(lambda __response__: GetZonesResult(
        filter_type=pulumi.get(__response__, 'filter_type'),
        id=pulumi.get(__response__, 'id'),
        zone_ids=pulumi.get(__response__, 'zone_ids')))
