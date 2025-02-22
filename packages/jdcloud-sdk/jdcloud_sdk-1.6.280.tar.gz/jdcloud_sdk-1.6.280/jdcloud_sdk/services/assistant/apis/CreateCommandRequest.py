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


class CreateCommandRequest(JDCloudRequest):
    """
    
保存用户自定义命令。

详细操作说明请参考帮助文档：[用户自定义命令概述](https://docs.jdcloud.com/cn/virtual-machines/assistant-overview)

## 接口说明
- 该接口用于保存用户自定义命令。

    """

    def __init__(self, parameters, header=None, version="v1"):
        super(CreateCommandRequest, self).__init__(
            '/regions/{regionId}/createCommand', 'POST', header, version)
        self.parameters = parameters


class CreateCommandParameters(object):

    def __init__(self,regionId, commandName, commandContent, ):
        """
        :param regionId: 地域ID。
        :param commandName: 命令名称，长度为1\~128个字符，只允许中文、数字、大小写字母、英文下划线（\_）、连字符（-）及点（.）。

        :param commandContent: 以base64编码的命令内容，编码后长度小于36KB

        """

        self.regionId = regionId
        self.commandName = commandName
        self.commandType = None
        self.commandContent = commandContent
        self.timeout = None
        self.username = None
        self.workdir = None
        self.commandDescription = None
        self.enableParameter = None

    def setCommandType(self, commandType):
        """
        :param commandType: (Optional) 命令类型，可选值：shell和powershell，默认shell

        """
        self.commandType = commandType

    def setTimeout(self, timeout):
        """
        :param timeout: (Optional) 超时时间，取值范围：[10, 86400], 超过该时间后，尚未执行完的命令会置为失败。默认60s

        """
        self.timeout = timeout

    def setUsername(self, username):
        """
        :param username: (Optional) 用户名，执行该命令时的用户身份。在linux上默认是root，windows上默认是administrator。长度小于256

        """
        self.username = username

    def setWorkdir(self, workdir):
        """
        :param workdir: (Optional) 命令执行路径。在linux上默认是/root，windows上默认是C:\Windows\System32。长度小于256。

        """
        self.workdir = workdir

    def setCommandDescription(self, commandDescription):
        """
        :param commandDescription: (Optional) 命令描述，描述该命令详细信息，如功能、使用注意事项等。长度小于256。

        """
        self.commandDescription = commandDescription

    def setEnableParameter(self, enableParameter):
        """
        :param enableParameter: (Optional) 是否使用参数, 默认false，不使用参数
        """
        self.enableParameter = enableParameter

