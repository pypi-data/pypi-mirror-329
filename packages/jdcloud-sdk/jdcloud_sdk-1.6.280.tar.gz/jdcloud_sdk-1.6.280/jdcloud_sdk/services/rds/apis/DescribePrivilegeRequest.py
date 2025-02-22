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


class DescribePrivilegeRequest(JDCloudRequest):
    """
    查看云数据库 RDS 的权限信息 - 仅支持 MySQL，Percona，MariaDB
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(DescribePrivilegeRequest, self).__init__(
            '/regions/{regionId}/common:describePrivilege', 'GET', header, version)
        self.parameters = parameters


class DescribePrivilegeParameters(object):

    def __init__(self,regionId, engine, ):
        """
        :param regionId: 地域代码，取值范围参见[《各地域及可用区对照表》](../Enum-Definitions/Regions-AZ.md)
        :param engine: 设置可见的引擎类型，如 MySQL 等
        """

        self.regionId = regionId
        self.engine = engine
        self.instanceId = None
        self.allAdminPrivileges = None

    def setInstanceId(self, instanceId):
        """
        :param instanceId: (Optional) RDS 实例ID，唯一标识一个RDS实例
        """
        self.instanceId = instanceId

    def setAllAdminPrivileges(self, allAdminPrivileges):
        """
        :param allAdminPrivileges: (Optional) true表示展示高权限，默认false
        """
        self.allAdminPrivileges = allAdminPrivileges

