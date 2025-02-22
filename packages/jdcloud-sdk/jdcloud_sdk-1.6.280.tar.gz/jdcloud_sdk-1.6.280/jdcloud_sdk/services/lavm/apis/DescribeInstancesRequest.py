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


class DescribeInstancesRequest(JDCloudRequest):
    """
    查询轻量应用云主机列表。

    """

    def __init__(self, parameters, header=None, version="v1"):
        super(DescribeInstancesRequest, self).__init__(
            '/regions/{regionId}/instances', 'GET', header, version)
        self.parameters = parameters


class DescribeInstancesParameters(object):

    def __init__(self,regionId, ):
        """
        :param regionId: regionId

        """

        self.regionId = regionId
        self.instanceIds = None
        self.chargeType = None
        self.publicIpAddresses = None
        self.names = None
        self.pageNumber = None
        self.pageSize = None

    def setInstanceIds(self, instanceIds):
        """
        :param instanceIds: (Optional) 轻量应用云主机的实例ID, `[\"lavm-xxx\", \"lavm-yyy\"]`, json array 字串

        """
        self.instanceIds = instanceIds

    def setChargeType(self, chargeType):
        """
        :param chargeType: (Optional) 实例的计费方式, 目前只支持且默认值prepaid_by_duration, 包年包月, 

        """
        self.chargeType = chargeType

    def setPublicIpAddresses(self, publicIpAddresses):
        """
        :param publicIpAddresses: (Optional) 轻量应用云主机的公网IP, 例如: `[\"114.1.x.y\", \"114.2.x.z\"]`, json array 字串

        """
        self.publicIpAddresses = publicIpAddresses

    def setNames(self, names):
        """
        :param names: (Optional) 轻量应用云主机的实例名称, 支持模糊搜索, 例如: `[\"instanceName-1\", \"instanceName-2\"]`, json array 字串

        """
        self.names = names

    def setPageNumber(self, pageNumber):
        """
        :param pageNumber: (Optional) 页码；默认为1。
        """
        self.pageNumber = pageNumber

    def setPageSize(self, pageSize):
        """
        :param pageSize: (Optional) 分页大小；<br>默认为20；取值范围[10, 100]。
        """
        self.pageSize = pageSize

