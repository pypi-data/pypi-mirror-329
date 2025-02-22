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


class Bill(object):

    def __init__(self, dataSource=None, sourceId=None, globalId=None, pin=None, startTime=None, endTime=None, region=None, appCode=None, serviceCode=None, resourceId=None, billingType=None, billFee=None, actualFee=None, billTime=None, currency=None, payState=None, payTime=None, discountFee=None, eraseFee=None, balancePayFee=None, cashPayFee=None, cashCouponFee=None, freeCashCouponFee=None, payCashCouponFee=None, wire=None, consumeTime=None, transactionNo=None, refundNo=None, site=None, org=None, tradeType=None, billType=None, formulaDesc=None, isDeleted=None, favorableInfo=None, az=None):
        """
        :param dataSource: (Optional) 数据来源：10、物联网 11、视频云 12、CDN 13、PCDN 14、IDC 15、通信云
        :param sourceId: (Optional) 账单唯一ID
        :param globalId: (Optional) 全局唯一ID
        :param pin: (Optional) 用户pin
        :param startTime: (Optional) 开始时间
        :param endTime: (Optional) 结束时间
        :param region: (Optional) 地域
        :param appCode: (Optional) 业务线
        :param serviceCode: (Optional) 产品编码
        :param resourceId: (Optional) 资源id
        :param billingType: (Optional) 计费类型： 1、按配置 2、按用量 3、包年包月 4、按次（一次性）
        :param billFee: (Optional) 账单原价,6位精度
        :param actualFee: (Optional) 应付金额，2位精度
        :param billTime: (Optional) 出账时间
        :param currency: (Optional) 币种 CNY 人民币， USD 美元， HKD 港元， IDR 印尼卢比
        :param payState: (Optional) 支付状态 0、未支付 1、己支付
        :param payTime: (Optional) 支付时间
        :param discountFee: (Optional) 折扣金额，6位精度
        :param eraseFee: (Optional) 抹零金额，6位精度
        :param balancePayFee: (Optional) 余额支付金额：2位精度
        :param cashPayFee: (Optional) 现金支付金额：2位精度
        :param cashCouponFee: (Optional) 代金券支付金额，2位精度
        :param freeCashCouponFee: (Optional) 免费代金券金额，2位精度
        :param payCashCouponFee: (Optional) 付费代金券金额，2位精度
        :param wire: (Optional) 电汇金额，2位精度
        :param consumeTime: (Optional) 消费时间
        :param transactionNo: (Optional) 交易单号
        :param refundNo: (Optional) 退款单号
        :param site: (Optional) 站点，0:国内
        :param org: (Optional) 组织机构代码
        :param tradeType: (Optional) 交易类型 1、使用 2、 新购 3、续费 4、配置变更 5、退款
        :param billType: (Optional) 账单类型 0-普通账单 1-退款账单 2-调账账单 3-保底账单
        :param formulaDesc: (Optional) 配置描述
        :param isDeleted: (Optional) 是否删除 0:未删除 1:己删除
        :param favorableInfo: (Optional) 优惠明细
        :param az: (Optional) 可用区
        """

        self.dataSource = dataSource
        self.sourceId = sourceId
        self.globalId = globalId
        self.pin = pin
        self.startTime = startTime
        self.endTime = endTime
        self.region = region
        self.appCode = appCode
        self.serviceCode = serviceCode
        self.resourceId = resourceId
        self.billingType = billingType
        self.billFee = billFee
        self.actualFee = actualFee
        self.billTime = billTime
        self.currency = currency
        self.payState = payState
        self.payTime = payTime
        self.discountFee = discountFee
        self.eraseFee = eraseFee
        self.balancePayFee = balancePayFee
        self.cashPayFee = cashPayFee
        self.cashCouponFee = cashCouponFee
        self.freeCashCouponFee = freeCashCouponFee
        self.payCashCouponFee = payCashCouponFee
        self.wire = wire
        self.consumeTime = consumeTime
        self.transactionNo = transactionNo
        self.refundNo = refundNo
        self.site = site
        self.org = org
        self.tradeType = tradeType
        self.billType = billType
        self.formulaDesc = formulaDesc
        self.isDeleted = isDeleted
        self.favorableInfo = favorableInfo
        self.az = az
