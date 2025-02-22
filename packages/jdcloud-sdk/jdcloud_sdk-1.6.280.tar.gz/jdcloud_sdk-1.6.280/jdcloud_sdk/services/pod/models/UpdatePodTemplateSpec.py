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


class UpdatePodTemplateSpec(object):

    def __init__(self, instanceType=None, restartPolicy=None, terminationGracePeriodSeconds=None, dnsConfig=None, logConfig=None, hostAliases=None, volumes=None, containers=None, elasticIp=None, noElasticIp=None, primaryNetworkInterface=None, secondaryNetworkInterfaces=None, userTags=None, removeUserTags=None):
        """
        :param instanceType: (Optional) 实例类型；参考[文档](https://www.jdcloud.com/help/detail/1992/isCatalog/1)
        :param restartPolicy: (Optional) pod中容器重启策略；Always, OnFailure, Never；默认：Always
        :param terminationGracePeriodSeconds: (Optional) 优雅关机宽限时长，如果超时，则触发强制关机。默认：30s，值不能是负数，范围：[0-300]
        :param dnsConfig: (Optional) pod内容器的/etc/resolv.conf配置。如指定了该参数则覆盖原有参数。
        :param logConfig: (Optional) 容器日志配置信息；默认会在本地分配10MB的存储空间。如指定了该参数则覆盖原有参数。
        :param hostAliases: (Optional) 域名和IP映射的信息；</br> 最大10个alias。如指定了该参数则覆盖原有参数，如果传空列表则清空原有配置。
        :param volumes: (Optional) Pod的volume列表，可以挂载到container上。长度范围：[0,7]。如指定了该参数则覆盖原有参数，如果传空列表则清空原有配置。
        :param containers: (Optional) Pod的容器列表，至少一个容器。长度范围[1,8]。如指定了该参数则覆盖原有参数。
        :param elasticIp: (Optional) 主网卡主IP关联的弹性IP规格。如指定了该参数则覆盖原有参数。
        :param noElasticIp: (Optional) 传 true 则会清空模板配置的公网IP参数。
        :param primaryNetworkInterface: (Optional) 主网卡配置信息。
        :param secondaryNetworkInterfaces: (Optional) 辅助网卡配置信息。如指定了该参数则覆盖原有参数，如果传空列表则清空配置。
        :param userTags: (Optional) 用户自定义标签集合，用于指定需要修改或者添加的标签。
        :param removeUserTags: (Optional) 移除模板中的自定义标签，指定要移除标签的key。
        """

        self.instanceType = instanceType
        self.restartPolicy = restartPolicy
        self.terminationGracePeriodSeconds = terminationGracePeriodSeconds
        self.dnsConfig = dnsConfig
        self.logConfig = logConfig
        self.hostAliases = hostAliases
        self.volumes = volumes
        self.containers = containers
        self.elasticIp = elasticIp
        self.noElasticIp = noElasticIp
        self.primaryNetworkInterface = primaryNetworkInterface
        self.secondaryNetworkInterfaces = secondaryNetworkInterfaces
        self.userTags = userTags
        self.removeUserTags = removeUserTags
