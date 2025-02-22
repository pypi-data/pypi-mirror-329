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


class ModifyInstanceCustomPageDefaultRequest(JDCloudRequest):
    """
    修改实例页面错误状态码返回页面为为默认页面
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(ModifyInstanceCustomPageDefaultRequest, self).__init__(
            '/regions/{regionId}/instances/{instanceId}:modifyInstanceCustomPageDefault', 'POST', header, version)
        self.parameters = parameters


class ModifyInstanceCustomPageDefaultParameters(object):

    def __init__(self, regionId,instanceId,):
        """
        :param regionId: 区域 ID, 高防不区分区域, 传 cn-north-1 即可
        :param instanceId: 实例 ID
        """

        self.regionId = regionId
        self.instanceId = instanceId

