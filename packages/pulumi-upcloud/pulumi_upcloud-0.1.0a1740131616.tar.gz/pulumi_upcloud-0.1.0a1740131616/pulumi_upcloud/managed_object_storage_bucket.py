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

__all__ = ['ManagedObjectStorageBucketArgs', 'ManagedObjectStorageBucket']

@pulumi.input_type
class ManagedObjectStorageBucketArgs:
    def __init__(__self__, *,
                 service_uuid: pulumi.Input[str],
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ManagedObjectStorageBucket resource.
        :param pulumi.Input[str] service_uuid: Managed Object Storage service UUID.
        :param pulumi.Input[str] name: Name of the bucket.
        """
        pulumi.set(__self__, "service_uuid", service_uuid)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="serviceUuid")
    def service_uuid(self) -> pulumi.Input[str]:
        """
        Managed Object Storage service UUID.
        """
        return pulumi.get(self, "service_uuid")

    @service_uuid.setter
    def service_uuid(self, value: pulumi.Input[str]):
        pulumi.set(self, "service_uuid", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the bucket.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _ManagedObjectStorageBucketState:
    def __init__(__self__, *,
                 name: Optional[pulumi.Input[str]] = None,
                 service_uuid: Optional[pulumi.Input[str]] = None,
                 total_objects: Optional[pulumi.Input[int]] = None,
                 total_size_bytes: Optional[pulumi.Input[int]] = None):
        """
        Input properties used for looking up and filtering ManagedObjectStorageBucket resources.
        :param pulumi.Input[str] name: Name of the bucket.
        :param pulumi.Input[str] service_uuid: Managed Object Storage service UUID.
        :param pulumi.Input[int] total_objects: Number of objects stored in the bucket.
        :param pulumi.Input[int] total_size_bytes: Total size of objects stored in the bucket.
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if service_uuid is not None:
            pulumi.set(__self__, "service_uuid", service_uuid)
        if total_objects is not None:
            pulumi.set(__self__, "total_objects", total_objects)
        if total_size_bytes is not None:
            pulumi.set(__self__, "total_size_bytes", total_size_bytes)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the bucket.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="serviceUuid")
    def service_uuid(self) -> Optional[pulumi.Input[str]]:
        """
        Managed Object Storage service UUID.
        """
        return pulumi.get(self, "service_uuid")

    @service_uuid.setter
    def service_uuid(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service_uuid", value)

    @property
    @pulumi.getter(name="totalObjects")
    def total_objects(self) -> Optional[pulumi.Input[int]]:
        """
        Number of objects stored in the bucket.
        """
        return pulumi.get(self, "total_objects")

    @total_objects.setter
    def total_objects(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "total_objects", value)

    @property
    @pulumi.getter(name="totalSizeBytes")
    def total_size_bytes(self) -> Optional[pulumi.Input[int]]:
        """
        Total size of objects stored in the bucket.
        """
        return pulumi.get(self, "total_size_bytes")

    @total_size_bytes.setter
    def total_size_bytes(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "total_size_bytes", value)


class ManagedObjectStorageBucket(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 service_uuid: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        This resource represents an UpCloud Managed Object Storage bucket.

        > This resource uses the UpCloud API to manage the Managed Object Storage buckets. The main difference to S3 API is that the buckets can be deleted even when the bucket contains objects.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_upcloud as upcloud

        example_managed_object_storage = upcloud.ManagedObjectStorage("exampleManagedObjectStorage",
            region="europe-1",
            configured_status="started")
        example_managed_object_storage_bucket = upcloud.ManagedObjectStorageBucket("exampleManagedObjectStorageBucket", service_uuid=example_managed_object_storage.id)
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: Name of the bucket.
        :param pulumi.Input[str] service_uuid: Managed Object Storage service UUID.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ManagedObjectStorageBucketArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        This resource represents an UpCloud Managed Object Storage bucket.

        > This resource uses the UpCloud API to manage the Managed Object Storage buckets. The main difference to S3 API is that the buckets can be deleted even when the bucket contains objects.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_upcloud as upcloud

        example_managed_object_storage = upcloud.ManagedObjectStorage("exampleManagedObjectStorage",
            region="europe-1",
            configured_status="started")
        example_managed_object_storage_bucket = upcloud.ManagedObjectStorageBucket("exampleManagedObjectStorageBucket", service_uuid=example_managed_object_storage.id)
        ```

        :param str resource_name: The name of the resource.
        :param ManagedObjectStorageBucketArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ManagedObjectStorageBucketArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 service_uuid: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ManagedObjectStorageBucketArgs.__new__(ManagedObjectStorageBucketArgs)

            __props__.__dict__["name"] = name
            if service_uuid is None and not opts.urn:
                raise TypeError("Missing required property 'service_uuid'")
            __props__.__dict__["service_uuid"] = service_uuid
            __props__.__dict__["total_objects"] = None
            __props__.__dict__["total_size_bytes"] = None
        super(ManagedObjectStorageBucket, __self__).__init__(
            'upcloud:index/managedObjectStorageBucket:ManagedObjectStorageBucket',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            name: Optional[pulumi.Input[str]] = None,
            service_uuid: Optional[pulumi.Input[str]] = None,
            total_objects: Optional[pulumi.Input[int]] = None,
            total_size_bytes: Optional[pulumi.Input[int]] = None) -> 'ManagedObjectStorageBucket':
        """
        Get an existing ManagedObjectStorageBucket resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: Name of the bucket.
        :param pulumi.Input[str] service_uuid: Managed Object Storage service UUID.
        :param pulumi.Input[int] total_objects: Number of objects stored in the bucket.
        :param pulumi.Input[int] total_size_bytes: Total size of objects stored in the bucket.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ManagedObjectStorageBucketState.__new__(_ManagedObjectStorageBucketState)

        __props__.__dict__["name"] = name
        __props__.__dict__["service_uuid"] = service_uuid
        __props__.__dict__["total_objects"] = total_objects
        __props__.__dict__["total_size_bytes"] = total_size_bytes
        return ManagedObjectStorageBucket(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the bucket.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="serviceUuid")
    def service_uuid(self) -> pulumi.Output[str]:
        """
        Managed Object Storage service UUID.
        """
        return pulumi.get(self, "service_uuid")

    @property
    @pulumi.getter(name="totalObjects")
    def total_objects(self) -> pulumi.Output[int]:
        """
        Number of objects stored in the bucket.
        """
        return pulumi.get(self, "total_objects")

    @property
    @pulumi.getter(name="totalSizeBytes")
    def total_size_bytes(self) -> pulumi.Output[int]:
        """
        Total size of objects stored in the bucket.
        """
        return pulumi.get(self, "total_size_bytes")

