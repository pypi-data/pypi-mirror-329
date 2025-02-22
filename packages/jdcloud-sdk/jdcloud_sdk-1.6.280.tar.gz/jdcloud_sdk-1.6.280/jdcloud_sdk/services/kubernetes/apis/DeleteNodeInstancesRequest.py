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


class DeleteNodeInstancesRequest(JDCloudRequest):
    """
    从工作节点组中删除指定实例
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(DeleteNodeInstancesRequest, self).__init__(
            '/regions/{regionId}/nodeGroups/{nodeGroupId}:deleteNodeInstances', 'POST', header, version)
        self.parameters = parameters


class DeleteNodeInstancesParameters(object):

    def __init__(self,regionId, nodeGroupId, instanceIds):
        """
        :param regionId: 地域 ID
        :param nodeGroupId: 工作节点组 ID
        :param instanceIds: 需要从工作节点组中删除的实例
- 不可将一个集群中的实例全部删除

        """

        self.regionId = regionId
        self.nodeGroupId = nodeGroupId
        self.instanceIds = instanceIds

