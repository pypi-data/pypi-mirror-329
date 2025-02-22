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


class DomainData(object):

    def __init__(self, dataList=None, currentCount=None, totalCount=None, totalPage=None):
        """
        :param dataList: (Optional) 域名数组
        :param currentCount: (Optional) 当前页的个数
        :param totalCount: (Optional) 域名的总数
        :param totalPage: (Optional) 域名的总页数
        """

        self.dataList = dataList
        self.currentCount = currentCount
        self.totalCount = totalCount
        self.totalPage = totalPage
