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


class DomainGroupItem(object):

    def __init__(self, domains=None, primaryDomain=None, shareCache=None, domainGroupName=None, id=None):
        """
        :param domains: (Optional) 域名组成员
        :param primaryDomain: (Optional) 主域名
        :param shareCache: (Optional) 是否共享缓存
        :param domainGroupName: (Optional) 域名组名称
        :param id: (Optional) 域名组id
        """

        self.domains = domains
        self.primaryDomain = primaryDomain
        self.shareCache = shareCache
        self.domainGroupName = domainGroupName
        self.id = id
