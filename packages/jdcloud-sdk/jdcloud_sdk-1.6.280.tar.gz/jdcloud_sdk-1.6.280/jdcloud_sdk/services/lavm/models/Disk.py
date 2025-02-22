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


class Disk(object):

    def __init__(self, createdTime=None, status=None, device=None, size=None, diskName=None, diskChargeType=None, diskType=None, category=None, diskId=None, instanceId=None, regionId=None):
        """
        :param createdTime: (Optional) 创建时间
        :param status: (Optional) 磁盘状态
        :param device: (Optional) 磁盘挂载服务器中的设备名
        :param size: (Optional) 磁盘大小
        :param diskName: (Optional) 磁盘名称
        :param diskChargeType: (Optional) 磁盘的计费方式
        :param diskType: (Optional) 磁盘类型
        :param category: (Optional) 磁盘种类
        :param diskId: (Optional) 磁盘ID
        :param instanceId: (Optional) 磁盘对应的轻量应用云主机的实例ID
        :param regionId: (Optional) 地域ID
        """

        self.createdTime = createdTime
        self.status = status
        self.device = device
        self.size = size
        self.diskName = diskName
        self.diskChargeType = diskChargeType
        self.diskType = diskType
        self.category = category
        self.diskId = diskId
        self.instanceId = instanceId
        self.regionId = regionId
