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


class PostActionUpdateSpec(object):

    def __init__(self, extendActionType, insertHeaderSpec=None, deleteHeaderSpec=None):
        """
        :param extendActionType:  负载均衡将后端服务器应答流量转发给客户端时的后置动作类型：3.插入http header动作；4.删除http header动作
        :param insertHeaderSpec: (Optional) 插入http header动作配置，当extendActionType为3时必须配置本参数
        :param deleteHeaderSpec: (Optional) 删除http header动作配置，当extendActionType为4时必须配置本参数
        """

        self.extendActionType = extendActionType
        self.insertHeaderSpec = insertHeaderSpec
        self.deleteHeaderSpec = deleteHeaderSpec
