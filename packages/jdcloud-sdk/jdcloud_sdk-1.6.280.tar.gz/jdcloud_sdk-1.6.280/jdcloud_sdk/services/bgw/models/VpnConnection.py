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


class VpnConnection(object):

    def __init__(self, vpnConnectionId=None, vpnConnectionName=None, bgwId=None, cgwId=None, bgpEnabled=None, localAsn=None, cloudPublicIp=None, providers=None, haStatus=None, description=None, createdTime=None, updatedTime=None, charge=None, trafficSelectors=None, azType=None, az=None):
        """
        :param vpnConnectionId: (Optional) VPN connection的Id
        :param vpnConnectionName: (Optional) VPN connection的名称
        :param bgwId: (Optional) 边界网关的Id
        :param cgwId: (Optional) 客户网关的Id
        :param bgpEnabled: (Optional) 是否使能BGP路由
        :param localAsn: (Optional) 本地的BGP ASN号
        :param cloudPublicIp: (Optional) VPN connection上分配的本端公网可路由的两个IPv4地址
        :param providers: (Optional) VPN连接的2个公网IP线路信息。当VPN为标准VPN时，2个线路都为bgp。当VPN为边缘VPN时，显示使用的2个公网IP线路
        :param haStatus: (Optional) 当前隧道状态是否满足高可用, 取值范围为: redundancy, no_redundancy
        :param description: (Optional) VPN connection的描述
        :param createdTime: (Optional) 客户网关的创建时间
        :param updatedTime: (Optional) 客户网关的更新时间
        :param charge: (Optional) 计费信息
        :param trafficSelectors: (Optional) vpn connection policy，IPSec VPN的感兴趣流，用于第二阶段协商
        :param azType: (Optional) VPN az类型，取值：standard(标准VPN)，edge(边缘VPN)
        :param az: (Optional) VPN可用区
        """

        self.vpnConnectionId = vpnConnectionId
        self.vpnConnectionName = vpnConnectionName
        self.bgwId = bgwId
        self.cgwId = cgwId
        self.bgpEnabled = bgpEnabled
        self.localAsn = localAsn
        self.cloudPublicIp = cloudPublicIp
        self.providers = providers
        self.haStatus = haStatus
        self.description = description
        self.createdTime = createdTime
        self.updatedTime = updatedTime
        self.charge = charge
        self.trafficSelectors = trafficSelectors
        self.azType = azType
        self.az = az
