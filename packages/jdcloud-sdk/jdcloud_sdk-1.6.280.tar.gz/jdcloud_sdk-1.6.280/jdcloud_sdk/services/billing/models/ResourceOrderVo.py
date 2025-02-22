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


class ResourceOrderVo(object):

    def __init__(self, id=None, transactionNo=None, resourceId=None, billingType=None, timeUnit=None, timeSpan=None, status=None, billingStatus=None, networkOperator=None, pin=None, appCode=None, serviceCode=None, site=None, region=None, formula=None, isOnTrial=None, startTime=None, endTime=None, createTime=None, payTime=None, formulaStr=None, chargeMode=None, chargeDuration=None, chargeUnit=None, aeStatus=None, releasingTime=None, sourceId=None, billingStartTime=None, priceMap=None, priceSnapshot=None, price=None, discountedPrice=None, expiringDays=None, billingCategoryDescription=None, description=None, refundNo=None, billingTypeName=None, favorableInfo=None, resourceName=None, processType=None, applicant=None, billingMode=None, operateTime=None, arrearsType=None, recycleBinReleasingTime=None):
        """
        :param id: (Optional) 主键id
        :param transactionNo: (Optional) 交易单唯一标识
        :param resourceId: (Optional) 资源id
        :param billingType: (Optional) 计费类型 1:按配置 2:按用量 3:包年包月 4:一次性
        :param timeUnit: (Optional) 时长类型 1:小时 2:天 3:月 4:年 5:周
        :param timeSpan: (Optional) 时长字段，与timeUnit字段构成具体时长
        :param status: (Optional) 资源状态 1:正常 2:停服 3:删除
        :param billingStatus: (Optional) 计费状态 0:停止计费 1:计费中
        :param networkOperator: (Optional) 网络类型0:无 1: non-BGP, 2: BGP
        :param pin: (Optional) 用户pin
        :param appCode: (Optional) 应用码
        :param serviceCode: (Optional) 服务码
        :param site: (Optional) 站点标识0:中国 1:国际
        :param region: (Optional) 资源区域
        :param formula: (Optional) 配置信息
        :param isOnTrial: (Optional) 否为试用资源 0:非试用 1:试用
        :param startTime: (Optional) 开始时间
        :param endTime: (Optional) 结束时间
        :param createTime: (Optional) 创建时间
        :param payTime: (Optional) 支付时间
        :param formulaStr: (Optional) formula转换成字符串
        :param chargeMode: (Optional) billingType兼容交易系统字段
        :param chargeDuration: (Optional) timeSpan兼容交易系统字段
        :param chargeUnit: (Optional) timeUnit兼容交易系统字段
        :param aeStatus: (Optional) 欠费过期状态，1:包年包月正常 2：包年包月到期  3:按配置、按用量正常  4：按配置、按用量欠费
        :param releasingTime: (Optional) 欠费、过期资源释放时间
        :param sourceId: (Optional) 交易单模块sourceId 计费不关心
        :param billingStartTime: (Optional) 计费开始时间 续费时本次续费周期开始时间
        :param priceMap: (Optional) 最新价格map
        :param priceSnapshot: (Optional) 价格快照
        :param price: (Optional) 订单折扣前总价
        :param discountedPrice: (Optional) 折扣后订单价格
        :param expiringDays: (Optional) 即将到期天数
        :param billingCategoryDescription: (Optional) 计费类型描述 例如:按配置、包年包月
        :param description: (Optional) 计费详情描述 例如:按配置、包年包月（一年）
        :param refundNo: (Optional) refundNo
        :param billingTypeName: (Optional) 计费类型单号
        :param favorableInfo: (Optional) 促销明细
        :param resourceName: (Optional) 资源名
        :param processType: (Optional) 变配明细（1-升配，2-降配，3-调整配置,4-续费,5-续费升配,6-续费降配,7-配置转包年包月）
        :param applicant: (Optional) 资源申请人
        :param billingMode: (Optional) 计费模式  1.停服停止计费  2.关机停止计费
        :param operateTime: (Optional) 启服、停服、停止计费时间
        :param arrearsType: (Optional) 欠费类型 1、无欠费，2、按配置欠费，3、按用量欠费，4、按配置和按用量都欠费
        :param recycleBinReleasingTime: (Optional) 欠费、过期资源释放时间-仅面向资源回收站使用
        """

        self.id = id
        self.transactionNo = transactionNo
        self.resourceId = resourceId
        self.billingType = billingType
        self.timeUnit = timeUnit
        self.timeSpan = timeSpan
        self.status = status
        self.billingStatus = billingStatus
        self.networkOperator = networkOperator
        self.pin = pin
        self.appCode = appCode
        self.serviceCode = serviceCode
        self.site = site
        self.region = region
        self.formula = formula
        self.isOnTrial = isOnTrial
        self.startTime = startTime
        self.endTime = endTime
        self.createTime = createTime
        self.payTime = payTime
        self.formulaStr = formulaStr
        self.chargeMode = chargeMode
        self.chargeDuration = chargeDuration
        self.chargeUnit = chargeUnit
        self.aeStatus = aeStatus
        self.releasingTime = releasingTime
        self.sourceId = sourceId
        self.billingStartTime = billingStartTime
        self.priceMap = priceMap
        self.priceSnapshot = priceSnapshot
        self.price = price
        self.discountedPrice = discountedPrice
        self.expiringDays = expiringDays
        self.billingCategoryDescription = billingCategoryDescription
        self.description = description
        self.refundNo = refundNo
        self.billingTypeName = billingTypeName
        self.favorableInfo = favorableInfo
        self.resourceName = resourceName
        self.processType = processType
        self.applicant = applicant
        self.billingMode = billingMode
        self.operateTime = operateTime
        self.arrearsType = arrearsType
        self.recycleBinReleasingTime = recycleBinReleasingTime
