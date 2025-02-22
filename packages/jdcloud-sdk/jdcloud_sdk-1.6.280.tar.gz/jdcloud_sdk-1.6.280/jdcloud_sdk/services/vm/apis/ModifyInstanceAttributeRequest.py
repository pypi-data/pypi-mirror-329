# coding=utf8

# Copyright 2018 JDCLOUD.COM
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# NOTE: This class is auto generated by the jdcloud code generator program.

from jdcloud_sdk.core.jdcloudrequest import JDCloudRequest


class ModifyInstanceAttributeRequest(JDCloudRequest):
    """
    
修改一台云主机的属性。

详细操作说明请参考帮助文档：
[修改实例名称](https://docs.jdcloud.com/cn/virtual-machines/modify-instance-name)
[自定义数据](https://docs.jdcloud.com/cn/virtual-machines/userdata)
[实例元数据](https://docs.jdcloud.com/cn/virtual-machines/instance-metadata)

## 接口说明
- 支持修改实例的名称、描述、hostname、自定义数据、实例元数据。

    """

    def __init__(self, parameters, header=None, version="v1"):
        super(ModifyInstanceAttributeRequest, self).__init__(
            '/regions/{regionId}/instances/{instanceId}:modifyInstanceAttribute', 'POST', header, version)
        self.parameters = parameters


class ModifyInstanceAttributeParameters(object):

    def __init__(self,regionId, instanceId, ):
        """
        :param regionId: 地域ID。
        :param instanceId: 云主机ID。
        """

        self.regionId = regionId
        self.instanceId = instanceId
        self.name = None
        self.description = None
        self.hostname = None
        self.metadata = None
        self.userdata = None

    def setName(self, name):
        """
        :param name: (Optional) 实例名称。长度为2\~128个字符，只允许中文、数字、大小写字母、英文下划线（\_）、连字符（-）及点（.），不能以（.）作为首尾。

        """
        self.name = name

    def setDescription(self, description):
        """
        :param description: (Optional) 实例描述。256字符以内。

        """
        self.description = description

    def setHostname(self, hostname):
        """
        :param hostname: (Optional) 实例hostname。
**Windows系统**：长度为2\~15个字符，允许大小写字母、数字或连字符（-），不能以连字符（-）开头或结尾，不能连续使用连字符（-），也不能全部使用数字。不支持点号（.）。
**Linux系统**：长度为2-64个字符，允许支持多个点号，点之间为一段，每段允许使用大小写字母、数字或连字符（-），但不能连续使用点号（.）或连字符（-），不能以点号（.）或连字符（-）开头或结尾。

        """
        self.hostname = hostname

    def setMetadata(self, metadata):
        """
        :param metadata: (Optional) 用户自定义元数据。
以 `key-value` 键值对形式指定，可在实例系统内通过元数据服务查询获取。最多支持40对键值对，且 `key` 不超过256字符，`value` 不超过16KB，不区分大小写。
注意：`key` 不要以连字符(-)结尾，否则此 `key` 不生效。

        """
        self.metadata = metadata

    def setUserdata(self, userdata):
        """
        :param userdata: (Optional) 自定义脚本。
目前仅支持启动脚本，即 `launch-script`，须Base64编码且编码前数据长度不能超过16KB。
**linux系统**：支持bash和python，编码前须分别以 `#!/bin/bash` 和 `#!/usr/bin/env python` 作为内容首行。
**Windows系统**：支持 `bat` 和 `powershell` ，编码前须分别以 `<cmd></cmd>和<powershell></powershell>` 作为内容首、尾行。

        """
        self.userdata = userdata

