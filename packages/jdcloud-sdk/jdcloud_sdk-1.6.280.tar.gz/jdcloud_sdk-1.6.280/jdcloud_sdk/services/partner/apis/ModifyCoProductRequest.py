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


class ModifyCoProductRequest(JDCloudRequest):
    """
    编辑合作产品
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(ModifyCoProductRequest, self).__init__(
            '/regions/{regionId}/CooperationInfo:modifyCoProduct', 'POST', header, version)
        self.parameters = parameters


class ModifyCoProductParameters(object):

    def __init__(self,regionId, ):
        """
        :param regionId: 区域(如:cn-north-1)
        """

        self.regionId = regionId
        self.cooperationId = None
        self.productName = None
        self.name = None
        self.productType = None
        self.productMode = None
        self.productDesc = None
        self.targetCustomer = None
        self.marketSize = None
        self.comparableProduct = None
        self.sellingForm = None
        self.sellingMode = None
        self.pricing = None
        self.productStatus = None
        self.incomeForecast = None
        self.costStructure = None
        self.grossMarginForecast = None
        self.pricingStrategy = None
        self.settlementMode = None
        self.settlementCycle = None
        self.riskSuggestion = None
        self.erp = None
        self.uuid = None

    def setCooperationId(self, cooperationId):
        """
        :param cooperationId: (Optional) 合作id
        """
        self.cooperationId = cooperationId

    def setProductName(self, productName):
        """
        :param productName: (Optional) 合作产品名称
        """
        self.productName = productName

    def setName(self, name):
        """
        :param name: (Optional) 合作名称
        """
        self.name = name

    def setProductType(self, productType):
        """
        :param productType: (Optional) 产品类型
        """
        self.productType = productType

    def setProductMode(self, productMode):
        """
        :param productMode: (Optional) 产品模式
        """
        self.productMode = productMode

    def setProductDesc(self, productDesc):
        """
        :param productDesc: (Optional) 产品简介
        """
        self.productDesc = productDesc

    def setTargetCustomer(self, targetCustomer):
        """
        :param targetCustomer: (Optional) 目标客户
        """
        self.targetCustomer = targetCustomer

    def setMarketSize(self, marketSize):
        """
        :param marketSize: (Optional) 市场规模
        """
        self.marketSize = marketSize

    def setComparableProduct(self, comparableProduct):
        """
        :param comparableProduct: (Optional) 主要竞品
        """
        self.comparableProduct = comparableProduct

    def setSellingForm(self, sellingForm):
        """
        :param sellingForm: (Optional) 售卖形态  1套/n年、2套/n月、3套、4次
        """
        self.sellingForm = sellingForm

    def setSellingMode(self, sellingMode):
        """
        :param sellingMode: (Optional) 售卖方式  1直销，2渠道，3代理
        """
        self.sellingMode = sellingMode

    def setPricing(self, pricing):
        """
        :param pricing: (Optional) 定价
        """
        self.pricing = pricing

    def setProductStatus(self, productStatus):
        """
        :param productStatus: (Optional) 产品状态
        """
        self.productStatus = productStatus

    def setIncomeForecast(self, incomeForecast):
        """
        :param incomeForecast: (Optional) 收入预测
        """
        self.incomeForecast = incomeForecast

    def setCostStructure(self, costStructure):
        """
        :param costStructure: (Optional) 成本结构
        """
        self.costStructure = costStructure

    def setGrossMarginForecast(self, grossMarginForecast):
        """
        :param grossMarginForecast: (Optional) 毛利率预测
        """
        self.grossMarginForecast = grossMarginForecast

    def setPricingStrategy(self, pricingStrategy):
        """
        :param pricingStrategy: (Optional) 定价策略 1市场对标， 2总成本加成，3变动成本加成
        """
        self.pricingStrategy = pricingStrategy

    def setSettlementMode(self, settlementMode):
        """
        :param settlementMode: (Optional) 结算方式 1固定金额结算，2实际售价固定比例结算，3实际售价浮动比例结算
        """
        self.settlementMode = settlementMode

    def setSettlementCycle(self, settlementCycle):
        """
        :param settlementCycle: (Optional) 结算周期 1周结后付款、2月结后付款、3季结后付款、4年结后付款，5 PO预付款
        """
        self.settlementCycle = settlementCycle

    def setRiskSuggestion(self, riskSuggestion):
        """
        :param riskSuggestion: (Optional) 风险及建议
        """
        self.riskSuggestion = riskSuggestion

    def setErp(self, erp):
        """
        :param erp: (Optional) erp
        """
        self.erp = erp

    def setUuid(self, uuid):
        """
        :param uuid: (Optional) 产品唯一标识id
        """
        self.uuid = uuid

