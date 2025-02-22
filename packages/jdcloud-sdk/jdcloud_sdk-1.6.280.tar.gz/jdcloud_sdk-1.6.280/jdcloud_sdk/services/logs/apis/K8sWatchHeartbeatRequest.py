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


class K8sWatchHeartbeatRequest(JDCloudRequest):
    """
    k8s watch heartbeat
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(K8sWatchHeartbeatRequest, self).__init__(
            '/k8sWatchHeartbeat', 'POST', header, version)
        self.parameters = parameters


class K8sWatchHeartbeatParameters(object):

    def __init__(self,):
        """
        """

        self.cluster = None
        self.devId = None
        self.cloud = None
        self.nodeCount = None
        self.containerCount = None
        self.latestPodChangeTime = None

    def setCluster(self, cluster):
        """
        :param cluster: (Optional) 集群
        """
        self.cluster = cluster

    def setDevId(self, devId):
        """
        :param devId: (Optional) 设备id
        """
        self.devId = devId

    def setCloud(self, cloud):
        """
        :param cloud: (Optional) 公有云集群标识
        """
        self.cloud = cloud

    def setNodeCount(self, nodeCount):
        """
        :param nodeCount: (Optional) node数量
        """
        self.nodeCount = nodeCount

    def setContainerCount(self, containerCount):
        """
        :param containerCount: (Optional) 容器数量
        """
        self.containerCount = containerCount

    def setLatestPodChangeTime(self, latestPodChangeTime):
        """
        :param latestPodChangeTime: (Optional) 最新容器变化时间
        """
        self.latestPodChangeTime = latestPodChangeTime

