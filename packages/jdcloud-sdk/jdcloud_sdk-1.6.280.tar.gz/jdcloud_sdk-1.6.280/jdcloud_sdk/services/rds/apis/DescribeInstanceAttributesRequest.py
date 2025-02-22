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


class DescribeInstanceAttributesRequest(JDCloudRequest):
    """
    查询RDS实例（MySQL、SQL Server等）的详细信息以及MySQL/PostgreSQL只读实例详细信息
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(DescribeInstanceAttributesRequest, self).__init__(
            '/regions/{regionId}/instances/{instanceId}', 'GET', header, version)
        self.parameters = parameters


class DescribeInstanceAttributesParameters(object):

    def __init__(self,regionId, instanceId, ):
        """
        :param regionId: 地域代码，取值范围参见[《各地域及可用区对照表》](../Enum-Definitions/Regions-AZ.md)
        :param instanceId: RDS 实例ID，唯一标识一个RDS实例
        """

        self.regionId = regionId
        self.instanceId = instanceId
        self.instanceExistence = None

    def setInstanceExistence(self, instanceExistence):
        """
        :param instanceExistence: (Optional) 默认不传，返回当前未删除的实例的实例详情 **仅支持 MySQL，Percona，MariaDB。<br>请求参数：<br>- 0:当前存在的实例；<br>- 1:已删除的实例；<br>- 2:全部实例，不区分实例是否删除;
        """
        self.instanceExistence = instanceExistence

