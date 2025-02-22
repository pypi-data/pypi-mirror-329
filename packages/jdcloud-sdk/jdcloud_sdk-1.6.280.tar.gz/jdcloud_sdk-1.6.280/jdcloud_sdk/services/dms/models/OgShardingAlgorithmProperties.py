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


class OgShardingAlgorithmProperties(object):

    def __init__(self, shardingAlgorithmType=None, shardingCount=None, rangeLower=None, rangeUpper=None, shardingVolume=None, shardingRanges=None, dateTimeLower=None, dateTimeUpper=None, shardingSeconds=None, allowRangeQueryWithInlineSharding=None, datetimePattern=None, shardingSuffixPattern=None, dateTimeIntervalAmount=None, dateTimeIntervalUnit=None):
        """
        :param shardingAlgorithmType: (Optional) 算法名称 MOD:取模,HASH_MOD:哈希取模,VOLUME_RANGE:基于分片容量的范围分片算法,BOUNDARY_RANGE:基于分片边界的范围分片算法,AUTO_INTERVAL:自动时间段分片算法。
        :param shardingCount: (Optional) 切分数量，算法为MOD/HASH_MOD时传入。
        :param rangeLower: (Optional) 开始范围，算法为VOLUME_RANGE时传入。
        :param rangeUpper: (Optional) 终止范围，算法为VOLUME_RANGE时传入。
        :param shardingVolume: (Optional) 范围分片容量，算法为VOLUME_RANGE时传入。
        :param shardingRanges: (Optional) 分片范围边界，算法为BOUNDARY_RANGE时传入。
        :param dateTimeLower: (Optional) 开始时间，算法为AUTO_INTERVAL/INTERVAL时传入。
        :param dateTimeUpper: (Optional) 结束时间，算法为AUTO_INTERVAL/INTERVAL时传入。
        :param shardingSeconds: (Optional) 单一分片能承载的最大时间，算法为AUTO_INTERVAL时传入，单位为秒。
        :param allowRangeQueryWithInlineSharding: (Optional) 是否容许在线切分查询，算法为inline时传入（非必须）。
        :param datetimePattern: (Optional) 时间格式，算法为interval时传入(分表后缀 传yyyy/yyyyMM/yyyyMMdd....)。
        :param shardingSuffixPattern: (Optional) 后缀模式，算法为interval时传入(分表后缀 传yyyy/yyyyMM/yyyyMMdd)。
        :param dateTimeIntervalAmount: (Optional) 分片时间间隔数量，算法为interval时传入。
        :param dateTimeIntervalUnit: (Optional) 分片时间间隔单位，算法为interval时传入（YEARS/MONTHS/WEEKS/DAYS/HOURS/MINUTES/SECONDS）。
        """

        self.shardingAlgorithmType = shardingAlgorithmType
        self.shardingCount = shardingCount
        self.rangeLower = rangeLower
        self.rangeUpper = rangeUpper
        self.shardingVolume = shardingVolume
        self.shardingRanges = shardingRanges
        self.dateTimeLower = dateTimeLower
        self.dateTimeUpper = dateTimeUpper
        self.shardingSeconds = shardingSeconds
        self.allowRangeQueryWithInlineSharding = allowRangeQueryWithInlineSharding
        self.datetimePattern = datetimePattern
        self.shardingSuffixPattern = shardingSuffixPattern
        self.dateTimeIntervalAmount = dateTimeIntervalAmount
        self.dateTimeIntervalUnit = dateTimeIntervalUnit
