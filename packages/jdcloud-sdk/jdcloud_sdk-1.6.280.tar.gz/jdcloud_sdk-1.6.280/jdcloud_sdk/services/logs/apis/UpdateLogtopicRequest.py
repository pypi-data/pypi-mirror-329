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


class UpdateLogtopicRequest(JDCloudRequest):
    """
    更新日志主题。日志主题名称不可更新。
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(UpdateLogtopicRequest, self).__init__(
            '/regions/{regionId}/logtopics/{logtopicUID}', 'PUT', header, version)
        self.parameters = parameters


class UpdateLogtopicParameters(object):

    def __init__(self,regionId, logtopicUID, description, ):
        """
        :param regionId: 地域 Id
        :param logtopicUID: 日志主题 UID
        :param description: 日志主题描述
        """

        self.regionId = regionId
        self.logtopicUID = logtopicUID
        self.name = None
        self.description = description
        self.lifeCycle = None
        self.inOrder = None

    def setName(self, name):
        """
        :param name: (Optional) 日志主题名称
        """
        self.name = name

    def setLifeCycle(self, lifeCycle):
        """
        :param lifeCycle: (Optional) 保存周期，只能是 7， 15， 30
        """
        self.lifeCycle = lifeCycle

    def setInOrder(self, inOrder):
        """
        :param inOrder: (Optional) 保序
        """
        self.inOrder = inOrder

