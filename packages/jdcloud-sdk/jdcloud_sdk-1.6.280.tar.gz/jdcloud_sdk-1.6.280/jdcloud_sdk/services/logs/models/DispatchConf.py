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


class DispatchConf(object):

    def __init__(self, tenantName=None, clusterName=None, zoneName=None, nodeIp=None, conf=None):
        """
        :param tenantName: (Optional) 租户字段
        :param clusterName: (Optional) 集群字段
        :param zoneName: (Optional) 机房字段
        :param nodeIp: (Optional) node-ip字段
        :param conf: (Optional) 采集配置字段
        """

        self.tenantName = tenantName
        self.clusterName = clusterName
        self.zoneName = zoneName
        self.nodeIp = nodeIp
        self.conf = conf
