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


class DnsConfigSpec(object):

    def __init__(self, nameservers=None, searches=None, options=None):
        """
        :param nameservers: (Optional) DNS服务器IP地址列表，重复的将会被移除。<br>
eg ["8.8.8.8", "4.2.2.2"]。列表长度：[0-20]，列表中元素符合IPv4格式。

        :param searches: (Optional) DNS搜索域列表，用于主机名查找。<br>
eg ["ns1.svc.cluster.local", "my.dns.search.suffix"]。列表长度：[0-6]，列表中所有字符总长度不超过256个。

        :param options: (Optional) DNS解析器选项列表。<br>
eg ["ndots":"2", "edns0":""]。列表长度：[0-10]
        """

        self.nameservers = nameservers
        self.searches = searches
        self.options = options
