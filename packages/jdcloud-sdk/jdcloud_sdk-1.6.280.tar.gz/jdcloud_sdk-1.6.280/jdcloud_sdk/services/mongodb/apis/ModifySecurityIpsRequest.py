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


class ModifySecurityIpsRequest(JDCloudRequest):
    """
    修改实例访问白名单
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(ModifySecurityIpsRequest, self).__init__(
            '/regions/{regionId}/instances/{instanceId}/securityIps', 'POST', header, version)
        self.parameters = parameters


class ModifySecurityIpsParameters(object):

    def __init__(self, regionId, instanceId, modifyMode, securityIps):
        """
        :param regionId: Region ID
        :param instanceId: Instance ID
        :param modifyMode: 修改方式,Add 增加白名单,Delete 删除白名单.
        :param securityIps: IP白名单分组下的IP列表，最多45个以逗号隔开，格式如下：0.0.0.0/0，10.23.12.24（IP），或者10.23.12.24/24（CIDR模式，无类域间路由，/24表示了地址中前缀的长度，范围[1，32]）。
        """

        self.regionId = regionId
        self.instanceId = instanceId
        self.modifyMode = modifyMode
        self.securityIps = securityIps

