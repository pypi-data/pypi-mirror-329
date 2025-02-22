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


class DescribeBackupsRequest(JDCloudRequest):
    """
    查看该RDS实例下所有备份的详细信息，返回的备份列表按照备份开始时间（backupStartTime）降序排列。
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(DescribeBackupsRequest, self).__init__(
            '/regions/{regionId}/backups', 'GET', header, version)
        self.parameters = parameters


class DescribeBackupsParameters(object):

    def __init__(self,regionId, instanceId, pageNumber, pageSize, ):
        """
        :param regionId: 地域代码，取值范围参见[《各地域及可用区对照表》](../Enum-Definitions/Regions-AZ.md)
        :param instanceId: RDS实例ID，唯一标识一个实例
        :param pageNumber: 显示数据的页码，默认为1，取值范围：[-1,∞)。pageNumber为-1时，返回所有数据页码；
        :param pageSize: 每页显示的数据条数，默认为10，取值范围：[10,100]
        """

        self.regionId = regionId
        self.instanceId = instanceId
        self.auto = None
        self.backupTypeFilter = None
        self.dbNameFilter = None
        self.backupTimeRangeStartFilter = None
        self.backupTimeRangeEndFilter = None
        self.pageNumber = pageNumber
        self.pageSize = pageSize
        self.filters = None

    def setAuto(self, auto):
        """
        :param auto: (Optional) 查询备份类型，0为手动备份，1为自动备份，不传表示全部. <br>**- 测试参数，仅支持SQL Server，后续可能被其他参数取代**
        """
        self.auto = auto

    def setBackupTypeFilter(self, backupTypeFilter):
        """
        :param backupTypeFilter: (Optional) 返回backupType等于指定值的备份列表。full为全量备份，diff为增量备份<br>**- 测试参数，仅支持SQL Server，后续可能被其他参数取代**
        """
        self.backupTypeFilter = backupTypeFilter

    def setDbNameFilter(self, dbNameFilter):
        """
        :param dbNameFilter: (Optional) 返回dbName等于指定值的备份列表，不传或为空返回全部<br>**- 测试参数，仅支持SQL Server，后续可能被其他参数取代**
        """
        self.dbNameFilter = dbNameFilter

    def setBackupTimeRangeStartFilter(self, backupTimeRangeStartFilter):
        """
        :param backupTimeRangeStartFilter: (Optional) 返回备份开始时间大于该时间的备份列表<br>**- 测试参数，仅支持SQL Server，后续可能被其他参数取代**
        """
        self.backupTimeRangeStartFilter = backupTimeRangeStartFilter

    def setBackupTimeRangeEndFilter(self, backupTimeRangeEndFilter):
        """
        :param backupTimeRangeEndFilter: (Optional) 返回备份开始时间小于等于该时间的备份列表<br>**- 测试参数，仅支持SQL Server，后续可能被其他参数取代**
        """
        self.backupTimeRangeEndFilter = backupTimeRangeEndFilter

    def setFilters(self, filters):
        """
        :param filters: (Optional) 过滤参数，多个过滤参数之间的关系为“与”(and支持以下属性的过滤(默认等值)：)
- instanceId：RDS实例ID，唯一标识一个实例，operator仅支持eq
- instanceName：RDS实例名称，模糊搜索，operator仅支持eq、like
- backupId：备份ID，唯一标识一个备份，operator仅支持eq
- backupName：备份名称，模糊搜索，operator仅支持eq、like
- auto：备份类型，0为手动备份，1为自动备份，operator仅支持eq
- backupMethod：返回backupMethod等于指定值的备份列表，physical为物理备份，snapshot为快照备份备注，operator仅支持eq

        """
        self.filters = filters

