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


class InstanceClass(object):

    def __init__(self, role=None, nodeClassCode=None, nodeCpu=None, nodeMemoryGB=None, nodeCount=None, nodeDiskType=None, nodeDiskGB=None):
        """
        :param role: (Optional) 角色
        :param nodeClassCode: (Optional) 节点规格代码
        :param nodeCpu: (Optional) 节点cpu核数
        :param nodeMemoryGB: (Optional) 节点内存单位GB
        :param nodeCount: (Optional) 节点个数
        :param nodeDiskType: (Optional) 磁盘类型
        :param nodeDiskGB: (Optional) 单节点磁盘大小单位GB
        """

        self.role = role
        self.nodeClassCode = nodeClassCode
        self.nodeCpu = nodeCpu
        self.nodeMemoryGB = nodeMemoryGB
        self.nodeCount = nodeCount
        self.nodeDiskType = nodeDiskType
        self.nodeDiskGB = nodeDiskGB
