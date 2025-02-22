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


class DescribeCCGraphRequest(JDCloudRequest):
    """
    CC 防护流量报表
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(DescribeCCGraphRequest, self).__init__(
            '/regions/{regionId}/charts:CCGraph', 'GET', header, version)
        self.parameters = parameters


class DescribeCCGraphParameters(object):

    def __init__(self, regionId,startTime, ):
        """
        :param regionId: 区域 ID, 高防不区分区域, 传 cn-north-1 即可
        :param startTime: 开始时间, 只能查询最近 90 天以内的数据, UTC 时间, 格式: yyyy-MM-dd'T'HH:mm:ssZ
        """

        self.regionId = regionId
        self.startTime = startTime
        self.endTime = None
        self.instanceId = None
        self.subDomain = None

    def setEndTime(self, endTime):
        """
        :param endTime: (Optional) 查询的结束时间, UTC 时间, 格式: yyyy-MM-dd'T'HH:mm:ssZ
        """
        self.endTime = endTime

    def setInstanceId(self, instanceId):
        """
        :param instanceId: (Optional) 高防实例 Id 列表
        """
        self.instanceId = instanceId

    def setSubDomain(self, subDomain):
        """
        :param subDomain: (Optional) 规则域名列表
        """
        self.subDomain = subDomain

