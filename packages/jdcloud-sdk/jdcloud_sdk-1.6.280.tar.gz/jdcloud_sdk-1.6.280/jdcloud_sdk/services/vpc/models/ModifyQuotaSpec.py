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


class ModifyQuotaSpec(object):

    def __init__(self, type, maxLimit, parentResourceId=None):
        """
        :param type:  资源类型，取值范围：vpc、elastic_ip、subnet、security_group、vpcpeering、network_interface（配额只统计辅助网卡）、acl、aclRule、routeTable、route、staticRoute、propagatedRoute、securityGroupRule、network_interface_cidr、bwpByUsage、bandwidthPackageIp、natGateway、natGatewayFip、trafficMirrorSession、trafficMirrorFilter、trafficMirrorFilterRule、trafficMirrorSource,haVip,haVipBinding
        :param parentResourceId: (Optional) type为vpc、elastic_ip、network_interface、bwpByUsage、natGateway、trafficMirrorSession、trafficMirrorFilter不设置, type为subnet、security_group、vpcpeering、acl、routeTable设置为vpcId, type为aclRule设置为aclId, type为route、staticRoute、propagatedRoute设置为routeTableId, type为securityGroupRule为securityGroupId, type为network_interface_cidr设置为networkInterfaceId，type为bandwidthPackageIp设置为bandwidthPackageId，natGatewayFip设置为natGatewayId,trafficMirrorFilterRule设置为trafficMirrorFilterId,trafficMirrorSource设置为trafficMirrorSessionId,haVip设置为vpcId,haVipBinding设置为haVipId
        :param maxLimit:  配额大小
        """

        self.type = type
        self.parentResourceId = parentResourceId
        self.maxLimit = maxLimit
