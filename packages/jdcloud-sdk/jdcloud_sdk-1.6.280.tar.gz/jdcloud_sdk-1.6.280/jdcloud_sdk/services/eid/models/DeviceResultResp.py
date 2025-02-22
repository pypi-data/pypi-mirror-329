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


class DeviceResultResp(object):

    def __init__(self, id=None, appName=None, system=None, eid=None, riskTag=None, createTime=None, updateTime=None, count=None):
        """
        :param id: (Optional) Id
        :param appName: (Optional) 应用名称
        :param system: (Optional) 操作系统
        :param eid: (Optional) Eid
        :param riskTag: (Optional) 设备风险
        :param createTime: (Optional) 创建时间，毫秒级时间戳
        :param updateTime: (Optional) 最新采集时间，毫秒级时间戳
        :param count: (Optional) 采集次数
        """

        self.id = id
        self.appName = appName
        self.system = system
        self.eid = eid
        self.riskTag = riskTag
        self.createTime = createTime
        self.updateTime = updateTime
        self.count = count
