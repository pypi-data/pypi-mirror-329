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


class DistributorContractPolicyDTO(object):

    def __init__(self, id=None, distributorPin=None, mainFlag=None, returnPolicyId=None, returnPolicyName=None):
        """
        :param id: (Optional) ID
        :param distributorPin: (Optional) 服务商pin
        :param mainFlag: (Optional) 服务商主协议PIN(1是0否)
        :param returnPolicyId: (Optional) 服务商政策ID
        :param returnPolicyName: (Optional) 服务商政策名称
        """

        self.id = id
        self.distributorPin = distributorPin
        self.mainFlag = mainFlag
        self.returnPolicyId = returnPolicyId
        self.returnPolicyName = returnPolicyName
