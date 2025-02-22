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


class GetCountResp(object):

    def __init__(self, totalNumber=None, getNumber=None, putNumber=None, czReportNumber=None, totalTodayNumber=None, czReportTodayNumber=None, putTodayNumber=None, getTodayNumber=None, totalYesterdayNumber=None, putYesterdayNumber=None, czReportYesterdayNumber=None, getYesterdayNumber=None):
        """
        :param totalNumber: (Optional) 存取证总数
        :param getNumber: (Optional) 总取证次数
        :param putNumber: (Optional) 总存证次数
        :param czReportNumber: (Optional) 总获取存证报告数
        :param totalTodayNumber: (Optional) 今日存取证总数
        :param czReportTodayNumber: (Optional) 今日获取存证报告数
        :param putTodayNumber: (Optional) 今日存证数
        :param getTodayNumber: (Optional) 今日取证数
        :param totalYesterdayNumber: (Optional) 昨日存取证总数
        :param putYesterdayNumber: (Optional) 昨日存证数
        :param czReportYesterdayNumber: (Optional) 昨日获取存证报告数
        :param getYesterdayNumber: (Optional) 昨日取证数
        """

        self.totalNumber = totalNumber
        self.getNumber = getNumber
        self.putNumber = putNumber
        self.czReportNumber = czReportNumber
        self.totalTodayNumber = totalTodayNumber
        self.czReportTodayNumber = czReportTodayNumber
        self.putTodayNumber = putTodayNumber
        self.getTodayNumber = getTodayNumber
        self.totalYesterdayNumber = totalYesterdayNumber
        self.putYesterdayNumber = putYesterdayNumber
        self.czReportYesterdayNumber = czReportYesterdayNumber
        self.getYesterdayNumber = getYesterdayNumber
