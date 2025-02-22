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


class DeleteLogsetRequest(JDCloudRequest):
    """
    删除日志集,删除多个日志集时，任意的日志集包含了日志主题的，将导致全部删除失败。
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(DeleteLogsetRequest, self).__init__(
            '/regions/{regionId}/logsets/{logsetUIDs}', 'DELETE', header, version)
        self.parameters = parameters


class DeleteLogsetParameters(object):

    def __init__(self,regionId, logsetUIDs):
        """
        :param regionId: 地域 Id
        :param logsetUIDs: 日志集ID，多个日志集ID以逗号分割
        """

        self.regionId = regionId
        self.logsetUIDs = logsetUIDs

