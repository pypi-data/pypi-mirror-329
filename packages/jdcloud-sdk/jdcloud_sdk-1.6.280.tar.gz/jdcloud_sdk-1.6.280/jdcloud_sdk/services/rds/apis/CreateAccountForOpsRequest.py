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


class CreateAccountForOpsRequest(JDCloudRequest):
    """
    创建数据库临时运维账号。<br>如果在使用数据库过程中需要京东云提供技术支持,并且需要对您的实例进行操作，您可以把临时运维账号提供给技术支持人员。<br>临时运维账号默认授予全局Select、Process权限，且账号只能通过控制台或者OpenAPI进行创建、删除账号以及对账号授权等，用户不能通过SQL语句对账号进行相关操作。<br>- 仅支持 MySQL，Percona，MariaDB
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(CreateAccountForOpsRequest, self).__init__(
            '/regions/{regionId}/instances/{instanceId}/accountsForOps', 'POST', header, version)
        self.parameters = parameters


class CreateAccountForOpsParameters(object):

    def __init__(self,regionId, instanceId, ):
        """
        :param regionId: 地域代码，取值范围参见[《各地域及可用区对照表》](../Enum-Definitions/Regions-AZ.md)
        :param instanceId: RDS 实例ID，唯一标识一个RDS实例
        """

        self.regionId = regionId
        self.instanceId = instanceId
        self.expiredTime = None

    def setExpiredTime(self, expiredTime):
        """
        :param expiredTime: (Optional) 运维账号到期时间，UTC时间格式
        """
        self.expiredTime = expiredTime

