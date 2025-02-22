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


class BankCardOCRRequest(JDCloudRequest):
    """
    银行卡OCR
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(BankCardOCRRequest, self).__init__(
            '/ocr:BankCard', 'POST', header, version)
        self.parameters = parameters


class BankCardOCRParameters(object):

    def __init__(self,imageData):
        """
        :param imageData: 银行卡图像base64(支持base64编码后小于3M)
        """

        self.imageData = imageData

