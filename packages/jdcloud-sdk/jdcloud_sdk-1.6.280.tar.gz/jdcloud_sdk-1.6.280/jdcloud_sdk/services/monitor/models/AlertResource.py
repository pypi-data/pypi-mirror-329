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


class AlertResource(object):

    def __init__(self, alertCount=None, product=None, productName=None, resourceId=None):
        """
        :param alertCount: (Optional) 报警个数
        :param product: (Optional) 产品
        :param productName: (Optional) 产品名称
        :param resourceId: (Optional) 资源id
        """

        self.alertCount = alertCount
        self.product = product
        self.productName = productName
        self.resourceId = resourceId
