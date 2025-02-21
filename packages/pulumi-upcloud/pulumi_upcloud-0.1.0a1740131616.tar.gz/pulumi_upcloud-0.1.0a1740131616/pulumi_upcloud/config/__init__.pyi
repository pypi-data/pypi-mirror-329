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
from .. import _utilities

password: Optional[str]
"""
Password for UpCloud API user. Can also be configured using the `UPCLOUD_PASSWORD` environment variable.
"""

requestTimeoutSec: Optional[int]
"""
The duration (in seconds) that the provider waits for an HTTP request towards UpCloud API to complete. Defaults to 120
seconds
"""

retryMax: Optional[int]
"""
Maximum number of retries
"""

retryWaitMaxSec: Optional[int]
"""
Maximum time to wait between retries
"""

retryWaitMinSec: Optional[int]
"""
Minimum time to wait between retries
"""

username: Optional[str]
"""
UpCloud username with API access. Can also be configured using the `UPCLOUD_USERNAME` environment variable.
"""

