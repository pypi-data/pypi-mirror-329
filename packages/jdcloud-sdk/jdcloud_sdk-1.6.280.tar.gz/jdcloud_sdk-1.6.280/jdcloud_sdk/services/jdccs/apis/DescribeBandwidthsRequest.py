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


class DescribeBandwidthsRequest(JDCloudRequest):
    """
    查询带宽（出口）列表
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(DescribeBandwidthsRequest, self).__init__(
            '/idcs/{idc}/bandwidths', 'GET', header, version)
        self.parameters = parameters


class DescribeBandwidthsParameters(object):

    def __init__(self,idc, ):
        """
        :param idc: IDC机房ID
        """

        self.idc = idc
        self.pageNumber = None
        self.pageSize = None
        self.lineType = None
        self.chargeType = None
        self.bandwidthName = None
        self.relatedIp = None
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

    def setLineType(self, lineType):
        """
        :param lineType: (Optional) 线路类型 dynamicBGP:动态BGP thirdLineBGP:三线BGP telecom:电信单线 unicom:联通单线 mobile:移动单线
        """
        self.lineType = lineType

    def setChargeType(self, chargeType):
        """
        :param chargeType: (Optional) 计费方式 fixedBandwidth:固定带宽 95thPercentile:95峰值 merge95thPercentile:合并95峰值
        """
        self.chargeType = chargeType

    def setBandwidthName(self, bandwidthName):
        """
        :param bandwidthName: (Optional) 带宽（出口）名称
        """
        self.bandwidthName = bandwidthName

    def setRelatedIp(self, relatedIp):
        """
        :param relatedIp: (Optional) 关联的公网IP
        """
        self.relatedIp = relatedIp

    def setFilters(self, filters):
        """
        :param filters: (Optional) bandwidthId - 带宽实例ID，精确匹配，支持多个

        """
        self.filters = filters

    def setSorts(self, sorts):
        """
        :param sorts: (Optional) null
        """
        self.sorts = sorts

