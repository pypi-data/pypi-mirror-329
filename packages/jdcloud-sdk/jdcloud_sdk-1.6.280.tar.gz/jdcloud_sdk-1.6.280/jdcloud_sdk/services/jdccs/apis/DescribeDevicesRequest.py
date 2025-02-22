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


class DescribeDevicesRequest(JDCloudRequest):
    """
    查询设备列表
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(DescribeDevicesRequest, self).__init__(
            '/idcs/{idc}/devices', 'GET', header, version)
        self.parameters = parameters


class DescribeDevicesParameters(object):

    def __init__(self,idc, ):
        """
        :param idc: IDC机房ID
        """

        self.idc = idc
        self.pageNumber = None
        self.pageSize = None
        self.cabinetId = None
        self.deviceType = None
        self.assetStatus = None
        self.assetBelong = None
        self.deviceNo = None
        self.snNo = None
        self.filters = None
        self.sorts = None

    def setPageNumber(self, pageNumber):
        """
        :param pageNumber: (Optional) 页码, 默认为1
        """
        self.pageNumber = pageNumber

    def setPageSize(self, pageSize):
        """
        :param pageSize: (Optional) 分页大小，默认为20
        """
        self.pageSize = pageSize

    def setCabinetId(self, cabinetId):
        """
        :param cabinetId: (Optional) 机柜ID
        """
        self.cabinetId = cabinetId

    def setDeviceType(self, deviceType):
        """
        :param deviceType: (Optional) 设备类型 server:服务器 network:网络设备 storage:存储设备 other:其他设备
        """
        self.deviceType = deviceType

    def setAssetStatus(self, assetStatus):
        """
        :param assetStatus: (Optional) 资产状态 launched:已上架 opened:已开通 canceling:退订中 operating:操作中 modifing:变更中
        """
        self.assetStatus = assetStatus

    def setAssetBelong(self, assetBelong):
        """
        :param assetBelong: (Optional) 资产归属 own:自备 lease:租赁
        """
        self.assetBelong = assetBelong

    def setDeviceNo(self, deviceNo):
        """
        :param deviceNo: (Optional) 设备编码
        """
        self.deviceNo = deviceNo

    def setSnNo(self, snNo):
        """
        :param snNo: (Optional) 设备SN号
        """
        self.snNo = snNo

    def setFilters(self, filters):
        """
        :param filters: (Optional) deviceId - 设备实例ID，精确匹配，支持多个
snNo - 设备SN号，精确匹配，支持多个
deviceNo - 设备编码，精确匹配，支持多个
cabinetNo - 机柜编码，精确匹配，支持多个

        """
        self.filters = filters

    def setSorts(self, sorts):
        """
        :param sorts: (Optional) deviceNo - 设备编码 cabinetNo - 机柜编码
        """
        self.sorts = sorts

