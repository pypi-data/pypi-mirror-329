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


class AssignSecondaryIpsRequest(JDCloudRequest):
    """
    给网卡分配secondaryIp接口
    """

    def __init__(self, parameters, header=None, version="v2"):
        super(AssignSecondaryIpsRequest, self).__init__(
            '/regions/{regionId}/ydNetworkInterfaces/{networkInterfaceId}:assignSecondaryIps', 'POST', header, version)
        self.parameters = parameters


class AssignSecondaryIpsParameters(object):

    def __init__(self,regionId, networkInterfaceId, ):
        """
        :param regionId: Region ID
        :param networkInterfaceId: networkInterface ID
        """

        self.regionId = regionId
        self.networkInterfaceId = networkInterfaceId
        self.force = None
        self.secondaryIps = None
        self.secondaryIpCount = None
        self.secondaryIpMaskLen = None
        self.secondaryIpAddress = None

    def setForce(self, force):
        """
        :param force: (Optional) secondary ip被其他接口占用时，是否抢占。false：非抢占重分配，true：抢占重分配；按网段分配时，默认非抢占重分配，指定IP或者个数时，默认抢占重分配。
        """
        self.force = force

    def setSecondaryIps(self, secondaryIps):
        """
        :param secondaryIps: (Optional) 指定分配的secondaryIp地址
        """
        self.secondaryIps = secondaryIps

    def setSecondaryIpCount(self, secondaryIpCount):
        """
        :param secondaryIpCount: (Optional) 指定自动分配的secondaryIp个数
        """
        self.secondaryIpCount = secondaryIpCount

    def setSecondaryIpMaskLen(self, secondaryIpMaskLen):
        """
        :param secondaryIpMaskLen: (Optional) 指定分配的网段掩码长度, 支持24-28位掩码长度，不能与secondaryIpCount或secondaryIps同时指定，不支持抢占重分配
        """
        self.secondaryIpMaskLen = secondaryIpMaskLen

    def setSecondaryIpAddress(self, secondaryIpAddress):
        """
        :param secondaryIpAddress: (Optional) 指定分配的网段中第一个secondaryIp地址，不能与secondaryIpCount或secondaryIps同时指定，secondaryIpAddress与secondaryIpMaskLen需要保持一致，否则无法创建
        """
        self.secondaryIpAddress = secondaryIpAddress

