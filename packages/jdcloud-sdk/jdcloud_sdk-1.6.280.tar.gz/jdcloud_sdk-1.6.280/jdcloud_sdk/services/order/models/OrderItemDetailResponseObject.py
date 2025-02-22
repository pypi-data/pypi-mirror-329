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


class OrderItemDetailResponseObject(object):

    def __init__(self, totalFee=None, actualFee=None, balancePay=None, chargeDuration=None, moneyPay=None, refundFee=None, chargeMode=None, createTime=None, expireDateAfter=None, expireDateBefore=None, extraInfo=None, extraInfoAfter=None, extraInfoBefore=None, favorableFee=None, formula=None, itemId=None, itemName=None, orderNumber=None, priceSnapshot=None, quantity=None, remark=None, resizeFormulaType=None, serviceName=None, siteType=None, status=None, unit=None, orderItemDetailResponse=None):
        """
        :param totalFee: (Optional) 订单总金额
        :param actualFee: (Optional) 应付金额（订单总金额-折扣金额）
        :param balancePay: (Optional) 余额支付金额
        :param chargeDuration: (Optional) 计费时长
        :param moneyPay: (Optional) 现金支付金额
        :param refundFee: (Optional) 退款金额
        :param chargeMode: (Optional) 计费类型(CONFIG-按配置,FLOW-按用量MONTHLY-包年包月,ONCE-按次付费)
        :param createTime: (Optional) 订单创建时间（格式：yyyy-MM-dd HH:mm:ss）
        :param expireDateAfter: (Optional) 续费后资源到期时间（格式：yyyy-MM-dd HH:mm:ss）
        :param expireDateBefore: (Optional) 续费前资源到期时间（格式：yyyy-MM-dd HH:mm:ss）
        :param extraInfo: (Optional) 销售属性
        :param extraInfoAfter: (Optional) 续费后资源到期-销售属性
        :param extraInfoBefore: (Optional) 续费前资源到期-销售属性
        :param favorableFee: (Optional) 代金券金额
        :param formula: (Optional) 配置计费项
        :param itemId: (Optional) 资源id
        :param itemName: (Optional) 资源名称
        :param orderNumber: (Optional) 订单号
        :param priceSnapshot: (Optional) 价格快照
        :param quantity: (Optional) 数量
        :param remark: (Optional) 备注
        :param resizeFormulaType: (Optional) 变配明细(UP-升配补差价，DOWN-降配延时,MODIFY_CONFIG-调整配置，RENEW-续费，RENEW_UP-续费升配，RENEW_DOWN-续费降配，MONTHLY-配置转包年包月，RENEW_FREE-补偿续费)
        :param serviceName: (Optional) 产品名称
        :param siteType: (Optional) 站点名称（MAIN_SITE-主站，INTERNATIONAL_SITE-国际站，SUQIAN_DEDICATED_CLOUD-宿迁专有云）
        :param status: (Optional) 资源状态（CREATING-创建中,SUCCESS-成功,FAIL-失败）
        :param unit: (Optional) 计费时长单位（HOUR-小时,DAY-天,MONTH-月,YEAR-年）
        :param orderItemDetailResponse: (Optional) 子订单
        """

        self.totalFee = totalFee
        self.actualFee = actualFee
        self.balancePay = balancePay
        self.chargeDuration = chargeDuration
        self.moneyPay = moneyPay
        self.refundFee = refundFee
        self.chargeMode = chargeMode
        self.createTime = createTime
        self.expireDateAfter = expireDateAfter
        self.expireDateBefore = expireDateBefore
        self.extraInfo = extraInfo
        self.extraInfoAfter = extraInfoAfter
        self.extraInfoBefore = extraInfoBefore
        self.favorableFee = favorableFee
        self.formula = formula
        self.itemId = itemId
        self.itemName = itemName
        self.orderNumber = orderNumber
        self.priceSnapshot = priceSnapshot
        self.quantity = quantity
        self.remark = remark
        self.resizeFormulaType = resizeFormulaType
        self.serviceName = serviceName
        self.siteType = siteType
        self.status = status
        self.unit = unit
        self.orderItemDetailResponse = orderItemDetailResponse
