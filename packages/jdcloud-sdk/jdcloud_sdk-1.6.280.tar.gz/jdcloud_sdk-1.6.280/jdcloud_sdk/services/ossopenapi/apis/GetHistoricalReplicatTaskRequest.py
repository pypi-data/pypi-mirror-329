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


class GetHistoricalReplicatTaskRequest(JDCloudRequest):
    """
    根据bucket名称获取该bucket下的同步任务
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(GetHistoricalReplicatTaskRequest, self).__init__(
            '/regions/{regionId}/buckets/{bucketName}/historical_replicat_task/{taskId}', 'GET', header, version)
        self.parameters = parameters


class GetHistoricalReplicatTaskParameters(object):

    def __init__(self,regionId, bucketName, taskId):
        """
        :param regionId: 区域ID
        :param bucketName: Bucket名称
        :param taskId: 任务ID
        """

        self.regionId = regionId
        self.bucketName = bucketName
        self.taskId = taskId

