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


class PolicyDetail(object):

    def __init__(self, policyId=None, name=None, jrn=None, description=None, policyType=None, version=None, currentDefaultEdition=None, content=None, createTime=None, updateTime=None):
        """
        :param policyId: (Optional) 策略id
        :param name: (Optional) 策略名称
        :param jrn: (Optional) 京东云资源标识(jrn)
        :param description: (Optional) 描述
        :param policyType: (Optional) 策略类型
        :param version: (Optional) 策略版本号
        :param currentDefaultEdition: (Optional) 当前默认策略文档版本
        :param content: (Optional) 权限策略内容（已废弃）
        :param createTime: (Optional) 策略创建时间
        :param updateTime: (Optional) 策略更新时间
        """

        self.policyId = policyId
        self.name = name
        self.jrn = jrn
        self.description = description
        self.policyType = policyType
        self.version = version
        self.currentDefaultEdition = currentDefaultEdition
        self.content = content
        self.createTime = createTime
        self.updateTime = updateTime
