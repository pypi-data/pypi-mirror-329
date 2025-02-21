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

__all__ = ['ManagedObjectStorageUserAccessKeyArgs', 'ManagedObjectStorageUserAccessKey']

@pulumi.input_type
class ManagedObjectStorageUserAccessKeyArgs:
    def __init__(__self__, *,
                 service_uuid: pulumi.Input[str],
                 status: pulumi.Input[str],
                 username: pulumi.Input[str]):
        """
        The set of arguments for constructing a ManagedObjectStorageUserAccessKey resource.
        :param pulumi.Input[str] service_uuid: Managed Object Storage service UUID.
        :param pulumi.Input[str] status: Status of the key. Valid values: `Active`|`Inactive`
        :param pulumi.Input[str] username: Username.
        """
        pulumi.set(__self__, "service_uuid", service_uuid)
        pulumi.set(__self__, "status", status)
        pulumi.set(__self__, "username", username)

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
    def status(self) -> pulumi.Input[str]:
        """
        Status of the key. Valid values: `Active`|`Inactive`
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: pulumi.Input[str]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter
    def username(self) -> pulumi.Input[str]:
        """
        Username.
        """
        return pulumi.get(self, "username")

    @username.setter
    def username(self, value: pulumi.Input[str]):
        pulumi.set(self, "username", value)


@pulumi.input_type
class _ManagedObjectStorageUserAccessKeyState:
    def __init__(__self__, *,
                 access_key_id: Optional[pulumi.Input[str]] = None,
                 created_at: Optional[pulumi.Input[str]] = None,
                 last_used_at: Optional[pulumi.Input[str]] = None,
                 secret_access_key: Optional[pulumi.Input[str]] = None,
                 service_uuid: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 username: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ManagedObjectStorageUserAccessKey resources.
        :param pulumi.Input[str] access_key_id: Access key id.
        :param pulumi.Input[str] created_at: Creation time.
        :param pulumi.Input[str] last_used_at: Last used.
        :param pulumi.Input[str] secret_access_key: Secret access key.
        :param pulumi.Input[str] service_uuid: Managed Object Storage service UUID.
        :param pulumi.Input[str] status: Status of the key. Valid values: `Active`|`Inactive`
        :param pulumi.Input[str] username: Username.
        """
        if access_key_id is not None:
            pulumi.set(__self__, "access_key_id", access_key_id)
        if created_at is not None:
            pulumi.set(__self__, "created_at", created_at)
        if last_used_at is not None:
            pulumi.set(__self__, "last_used_at", last_used_at)
        if secret_access_key is not None:
            pulumi.set(__self__, "secret_access_key", secret_access_key)
        if service_uuid is not None:
            pulumi.set(__self__, "service_uuid", service_uuid)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if username is not None:
            pulumi.set(__self__, "username", username)

    @property
    @pulumi.getter(name="accessKeyId")
    def access_key_id(self) -> Optional[pulumi.Input[str]]:
        """
        Access key id.
        """
        return pulumi.get(self, "access_key_id")

    @access_key_id.setter
    def access_key_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "access_key_id", value)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[pulumi.Input[str]]:
        """
        Creation time.
        """
        return pulumi.get(self, "created_at")

    @created_at.setter
    def created_at(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "created_at", value)

    @property
    @pulumi.getter(name="lastUsedAt")
    def last_used_at(self) -> Optional[pulumi.Input[str]]:
        """
        Last used.
        """
        return pulumi.get(self, "last_used_at")

    @last_used_at.setter
    def last_used_at(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "last_used_at", value)

    @property
    @pulumi.getter(name="secretAccessKey")
    def secret_access_key(self) -> Optional[pulumi.Input[str]]:
        """
        Secret access key.
        """
        return pulumi.get(self, "secret_access_key")

    @secret_access_key.setter
    def secret_access_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "secret_access_key", value)

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
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        Status of the key. Valid values: `Active`|`Inactive`
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter
    def username(self) -> Optional[pulumi.Input[str]]:
        """
        Username.
        """
        return pulumi.get(self, "username")

    @username.setter
    def username(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "username", value)


class ManagedObjectStorageUserAccessKey(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 service_uuid: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 username: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        This resource represents an UpCloud Managed Object Storage user access key.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_upcloud as upcloud

        this_managed_object_storage = upcloud.ManagedObjectStorage("thisManagedObjectStorage",
            region="europe-1",
            configured_status="started")
        this_managed_object_storage_user = upcloud.ManagedObjectStorageUser("thisManagedObjectStorageUser",
            username="example",
            service_uuid=this_managed_object_storage.id)
        this_managed_object_storage_user_access_key = upcloud.ManagedObjectStorageUserAccessKey("thisManagedObjectStorageUserAccessKey",
            username=this_managed_object_storage_user.username,
            service_uuid=this_managed_object_storage.id,
            status="Active")
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] service_uuid: Managed Object Storage service UUID.
        :param pulumi.Input[str] status: Status of the key. Valid values: `Active`|`Inactive`
        :param pulumi.Input[str] username: Username.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ManagedObjectStorageUserAccessKeyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        This resource represents an UpCloud Managed Object Storage user access key.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_upcloud as upcloud

        this_managed_object_storage = upcloud.ManagedObjectStorage("thisManagedObjectStorage",
            region="europe-1",
            configured_status="started")
        this_managed_object_storage_user = upcloud.ManagedObjectStorageUser("thisManagedObjectStorageUser",
            username="example",
            service_uuid=this_managed_object_storage.id)
        this_managed_object_storage_user_access_key = upcloud.ManagedObjectStorageUserAccessKey("thisManagedObjectStorageUserAccessKey",
            username=this_managed_object_storage_user.username,
            service_uuid=this_managed_object_storage.id,
            status="Active")
        ```

        :param str resource_name: The name of the resource.
        :param ManagedObjectStorageUserAccessKeyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ManagedObjectStorageUserAccessKeyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 service_uuid: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 username: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ManagedObjectStorageUserAccessKeyArgs.__new__(ManagedObjectStorageUserAccessKeyArgs)

            if service_uuid is None and not opts.urn:
                raise TypeError("Missing required property 'service_uuid'")
            __props__.__dict__["service_uuid"] = service_uuid
            if status is None and not opts.urn:
                raise TypeError("Missing required property 'status'")
            __props__.__dict__["status"] = status
            if username is None and not opts.urn:
                raise TypeError("Missing required property 'username'")
            __props__.__dict__["username"] = username
            __props__.__dict__["access_key_id"] = None
            __props__.__dict__["created_at"] = None
            __props__.__dict__["last_used_at"] = None
            __props__.__dict__["secret_access_key"] = None
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["secretAccessKey"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(ManagedObjectStorageUserAccessKey, __self__).__init__(
            'upcloud:index/managedObjectStorageUserAccessKey:ManagedObjectStorageUserAccessKey',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            access_key_id: Optional[pulumi.Input[str]] = None,
            created_at: Optional[pulumi.Input[str]] = None,
            last_used_at: Optional[pulumi.Input[str]] = None,
            secret_access_key: Optional[pulumi.Input[str]] = None,
            service_uuid: Optional[pulumi.Input[str]] = None,
            status: Optional[pulumi.Input[str]] = None,
            username: Optional[pulumi.Input[str]] = None) -> 'ManagedObjectStorageUserAccessKey':
        """
        Get an existing ManagedObjectStorageUserAccessKey resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] access_key_id: Access key id.
        :param pulumi.Input[str] created_at: Creation time.
        :param pulumi.Input[str] last_used_at: Last used.
        :param pulumi.Input[str] secret_access_key: Secret access key.
        :param pulumi.Input[str] service_uuid: Managed Object Storage service UUID.
        :param pulumi.Input[str] status: Status of the key. Valid values: `Active`|`Inactive`
        :param pulumi.Input[str] username: Username.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ManagedObjectStorageUserAccessKeyState.__new__(_ManagedObjectStorageUserAccessKeyState)

        __props__.__dict__["access_key_id"] = access_key_id
        __props__.__dict__["created_at"] = created_at
        __props__.__dict__["last_used_at"] = last_used_at
        __props__.__dict__["secret_access_key"] = secret_access_key
        __props__.__dict__["service_uuid"] = service_uuid
        __props__.__dict__["status"] = status
        __props__.__dict__["username"] = username
        return ManagedObjectStorageUserAccessKey(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accessKeyId")
    def access_key_id(self) -> pulumi.Output[str]:
        """
        Access key id.
        """
        return pulumi.get(self, "access_key_id")

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> pulumi.Output[str]:
        """
        Creation time.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="lastUsedAt")
    def last_used_at(self) -> pulumi.Output[str]:
        """
        Last used.
        """
        return pulumi.get(self, "last_used_at")

    @property
    @pulumi.getter(name="secretAccessKey")
    def secret_access_key(self) -> pulumi.Output[str]:
        """
        Secret access key.
        """
        return pulumi.get(self, "secret_access_key")

    @property
    @pulumi.getter(name="serviceUuid")
    def service_uuid(self) -> pulumi.Output[str]:
        """
        Managed Object Storage service UUID.
        """
        return pulumi.get(self, "service_uuid")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        Status of the key. Valid values: `Active`|`Inactive`
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def username(self) -> pulumi.Output[str]:
        """
        Username.
        """
        return pulumi.get(self, "username")

