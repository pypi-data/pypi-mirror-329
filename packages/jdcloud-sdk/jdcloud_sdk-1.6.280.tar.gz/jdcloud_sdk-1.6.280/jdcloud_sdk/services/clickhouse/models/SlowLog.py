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


class SlowLog(object):

    def __init__(self, ip=None, requestId=None, segmentName=None, startTime=None, queryTime=None, sql=None, lineNumber=None, dataSize=None, executingResult=None, memoryUsage=None):
        """
        :param ip: (Optional) 源IP
        :param requestId: (Optional) 初始请求ID
        :param segmentName: (Optional) 节点名称
        :param startTime: (Optional) SQL开始时间
        :param queryTime: (Optional) 慢日志SQL执行时间
        :param sql: (Optional) SQL语句
        :param lineNumber: (Optional) 读取慢日志SQL的行数
        :param dataSize: (Optional) 读取慢日志SQL的数据量
        :param executingResult: (Optional) 返回结果数据量大小
        :param memoryUsage: (Optional) 返回结果内存使用量
        """

        self.ip = ip
        self.requestId = requestId
        self.segmentName = segmentName
        self.startTime = startTime
        self.queryTime = queryTime
        self.sql = sql
        self.lineNumber = lineNumber
        self.dataSize = dataSize
        self.executingResult = executingResult
        self.memoryUsage = memoryUsage
