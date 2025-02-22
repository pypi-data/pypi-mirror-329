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


class DescribeTargetsRequest(JDCloudRequest):
    """
    查询Target列表详情
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(DescribeTargetsRequest, self).__init__(
            '/regions/{regionId}/targetGroups/{targetGroupId}:describeTargets', 'GET', header, version)
        self.parameters = parameters


class DescribeTargetsParameters(object):

    def __init__(self,regionId, targetGroupId, ):
        """
        :param regionId: Region ID
        :param targetGroupId: TargetGroup Id
        """

        self.regionId = regionId
        self.targetGroupId = targetGroupId
        self.pageNumber = None
        self.pageSize = None
        self.filters = None

    def setPageNumber(self, pageNumber):
        """
        :param pageNumber: (Optional) 页码, 默认为1, 取值范围：[1,∞), 页码超过总页数时, 显示最后一页
        """
        self.pageNumber = pageNumber

    def setPageSize(self, pageSize):
        """
        :param pageSize: (Optional) 分页大小，默认为20，取值范围：[10,100]
        """
        self.pageSize = pageSize

    def setFilters(self, filters):
        """
        :param filters: (Optional) targetIds - Target ID列表，支持多个
instanceId - Instance ID,仅支持单个
type － vm, container, ip,仅支持单个
port - 端口,仅支持单个
ipAddress - ip地址,仅支持单个

        """
        self.filters = filters

