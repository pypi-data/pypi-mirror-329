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


class CreateAccountRequest(JDCloudRequest):
    """
    创建数据库的高权限管理账号，用户可以使用客户端、应用程序等通过该账号和密码登录 TiDB 实例，然后通过SQL创建数据库和其他用户。一个数据库实例只能创建一个高权限账号。
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(CreateAccountRequest, self).__init__(
            '/regions/{regionId}/instances/{instanceId}/accounts', 'POST', header, version)
        self.parameters = parameters


class CreateAccountParameters(object):

    def __init__(self,regionId, instanceId, accountName, accountPassword):
        """
        :param regionId: 地域代码
        :param instanceId: 实例ID
        :param accountName: 账号名
        :param accountPassword: 密码
        """

        self.regionId = regionId
        self.instanceId = instanceId
        self.accountName = accountName
        self.accountPassword = accountPassword

