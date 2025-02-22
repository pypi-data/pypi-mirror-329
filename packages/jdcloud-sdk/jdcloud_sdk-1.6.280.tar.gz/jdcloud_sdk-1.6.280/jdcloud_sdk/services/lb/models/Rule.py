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


class Rule(object):

    def __init__(self, ruleId=None, host=None, path=None, action=None, backendId=None, redirectAction=None, preActions=None, postActions=None):
        """
        :param ruleId: (Optional) 转发规则Id
        :param host: (Optional) 域名，用于匹配URL的host字段，支持输入IPv4地址和域名。域名支持精确匹配和通配符匹配：1、仅支持输入大小写字母、数字、英文中划线“-”和点“.”，最少包括一个点"."，不能以点"."和中划线"-"开头或结尾，中划线"-"前后不能为点"."，不区分大小写，且不能超过110字符；2、通配符匹配支持包括一个星"\*"，输入格式为\*.XXX或XXX.\*，不支持仅输入一个星“\*”
        :param path: (Optional) URL访问路径，用于匹配URL的path字段。URL路径支持精确匹配和前缀匹配：1、必须以/开头，仅支持输入大小写字母、数字和特殊字符：$-_.+!'()%:@&=/，区分大小写，且不能超过128字符；2、前缀匹配支持包括一个星"\*"，输入格式为/XXX\*或/\*。仅输入"/"表示精确匹配
        :param action: (Optional) 匹配转发规则后执行的动作，取值为Forward或Redirect。默认为Forward。
        :param backendId: (Optional) 后端服务的Id。当action选择Forward时显示本参数
        :param redirectAction: (Optional) 重定向的相关参数。当action选择Redirect时显示相关参数
        :param preActions: (Optional) 负载均衡将客户端流量向后端服务器转发时的前置动作配置
        :param postActions: (Optional) 负载均衡将后端服务器应答流量转发给客户端时的后置动作配置
        """

        self.ruleId = ruleId
        self.host = host
        self.path = path
        self.action = action
        self.backendId = backendId
        self.redirectAction = redirectAction
        self.preActions = preActions
        self.postActions = postActions
