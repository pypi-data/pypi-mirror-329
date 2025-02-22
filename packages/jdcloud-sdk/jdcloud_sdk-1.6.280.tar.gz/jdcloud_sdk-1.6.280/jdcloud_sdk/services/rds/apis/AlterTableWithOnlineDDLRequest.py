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

from jdcloud_sdk.core.jdcloudrequest import JDCloudRequest


class AlterTableWithOnlineDDLRequest(JDCloudRequest):
    """
    通过 PT-OSC 服务来处理 DDL 命令, 避免锁表。此接口暂是对部分用户开放
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(AlterTableWithOnlineDDLRequest, self).__init__(
            '/regions/{regionId}/instances/{instanceId}:alterTableWithOnlineDDL', 'POST', header, version)
        self.parameters = parameters


class AlterTableWithOnlineDDLParameters(object):

    def __init__(self,regionId, instanceId, database, table, command):
        """
        :param regionId: 地域代码，取值范围参见[《各地域及可用区对照表》](../Enum-Definitions/Regions-AZ.md)
        :param instanceId: RDS 实例ID，唯一标识一个RDS实例
        :param database: DDL命令修改的库名
        :param table: DDL命令修改的表名
        :param command: 需要执行的的DDL命令
        """

        self.regionId = regionId
        self.instanceId = instanceId
        self.database = database
        self.table = table
        self.command = command

