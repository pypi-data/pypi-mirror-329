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


class ListHistoricalReplicatTasksRequest(JDCloudRequest):
    """
    根据bucket名称获取该bucket下的同步任务列表
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(ListHistoricalReplicatTasksRequest, self).__init__(
            '/regions/{regionId}/buckets/{bucketName}/historical_replicat_task/', 'GET', header, version)
        self.parameters = parameters


class ListHistoricalReplicatTasksParameters(object):

    def __init__(self,regionId, bucketName, ):
        """
        :param regionId: 区域ID
        :param bucketName: Bucket名称
        """

        self.regionId = regionId
        self.bucketName = bucketName
        self.marker = None
        self.limit = None

    def setMarker(self, marker):
        """
        :param marker: (Optional) 同步任务列表开始的key
        """
        self.marker = marker

    def setLimit(self, limit):
        """
        :param limit: (Optional) 每次查询返回的结果数，默认为1000
        """
        self.limit = limit

