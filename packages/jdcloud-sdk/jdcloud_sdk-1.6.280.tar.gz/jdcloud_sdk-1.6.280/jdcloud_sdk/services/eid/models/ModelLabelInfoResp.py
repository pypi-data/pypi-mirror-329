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


class ModelLabelInfoResp(object):

    def __init__(self, id=None, labelName=None, weights=None, createTime=None, updateTime=None):
        """
        :param id: (Optional) id
        :param labelName: (Optional) 标签名称
        :param weights: (Optional) 权重
        :param createTime: (Optional) 创建时间,秒级时间戳
        :param updateTime: (Optional) 更新时间，秒级时间戳
        """

        self.id = id
        self.labelName = labelName
        self.weights = weights
        self.createTime = createTime
        self.updateTime = updateTime
