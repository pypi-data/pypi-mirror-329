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


class ListTopicsRequest(JDCloudRequest):
    """
    获取Topic列表
    """

    def __init__(self, parameters, header=None, version="v2"):
        super(ListTopicsRequest, self).__init__(
            '/regions/{regionId}/endpoint/{endpointId}/topic', 'POST', header, version)
        self.parameters = parameters


class ListTopicsParameters(object):

    def __init__(self,regionId, endpointId, endpoint):
        """
        :param regionId: 地域代码，取值范围参见[《各地域及可用区对照表》]
        :param endpointId: DTS连接模板ID
        :param endpoint: 连接模板信息
        """

        self.regionId = regionId
        self.endpointId = endpointId
        self.taskId = None
        self.endpoint = endpoint

    def setTaskId(self, taskId):
        """
        :param taskId: (Optional) 数据传输任务ID
        """
        self.taskId = taskId

