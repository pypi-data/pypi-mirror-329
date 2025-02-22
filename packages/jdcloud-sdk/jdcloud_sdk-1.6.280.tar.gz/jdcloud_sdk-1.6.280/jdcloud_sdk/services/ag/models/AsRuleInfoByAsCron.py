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


class AsRuleInfoByAsCron(object):

    def __init__(self, asRuleId=None, name=None, description=None, asRuleType=None, simpleAsRuleInfo=None, createTime=None, updateTime=None):
        """
        :param asRuleId: (Optional) 伸缩规则ID
        :param name: (Optional) 伸缩规则名称
        :param description: (Optional) 伸缩规则描述
        :param asRuleType: (Optional) 伸缩规则类型
        :param simpleAsRuleInfo: (Optional) 关联的简单规则信息
        :param createTime: (Optional) 创建时间
        :param updateTime: (Optional) 更新时间
        """

        self.asRuleId = asRuleId
        self.name = name
        self.description = description
        self.asRuleType = asRuleType
        self.simpleAsRuleInfo = simpleAsRuleInfo
        self.createTime = createTime
        self.updateTime = updateTime
