from enum import Enum


class ClientTypeEnum(Enum):
    # 邮箱登录
    USER_EMAIL = 100
    # 手机登录
    USER_MOBILE = 101
    # 昵称登录
    USER_NICKNAME = 102


class RoleTypeEnum(Enum):
    # 1：管理员 2:教员 3：学生
    administrator = 1
    instructor = 2
    student = 3

    @classmethod
    def step_str(cls, step):
        key_map = {
            cls.administrator: '管理员',
            cls.instructor: '教员',
            cls.student: '学生',
        }
        return key_map[step]

# class ScopeTypeEnum(Enum):
#     # 1:全开放 2：半开放 3:不开放
#     FullOpenScope = 1
#     HalfOpenScope = 2
#     NoOpenScope = 3
#
#     @classmethod
#     def step_str(cls, step):
#         key_map = {
#             cls.FullOpenScope: '全开放',
#             cls.HalfOpenScope: '半开放',
#             cls.NoOpenScope: '不开放',
#         }
#         return key_map[step]

class SignalTypeEnum(Enum):
    # 1:辐射噪声 2：目标回声 3:主动脉冲
    RadiatedNoise = 1
    TargetEcho = 2
    ActivePulse = 3

    @classmethod
    def step_str(cls, step):
        key_map = {
            cls.RadiatedNoise: '辐射噪声',
            cls.TargetEcho: '目标回声',
            cls.ActivePulse: '主动脉冲',
        }
        return key_map[step]


# class Feature_Step(Enum):
#     no_operation = 0
#     pre_process = 1
#     feature_extraction_power = 2
#     feature_extraction_low_frequency = 3
#     feature_extraction_modulation = 4
#     feature_extraction_listening = 5
#     feature_extraction_aortic_impulse = 6
#     evaluation_lose = 7
#     evaluation_quality = 8
#     excercise_listening = 9
#
#     # 1: 预处理，
#     # 2：特征提取——功率谱特征提取，
#     # 3：特征提取——低频线谱特征提取，
#     # 4：特征提取——调制谱特征提取，
#     # 5：特征提取——听音特征提取，
#     # 6：特征提取——主动脉冲特征提取，
#     # 7：质量评估——失真分析，
#     # 8：质量评估——质量评价，
#     # 9：听音训练
#     # 无操作: 0
#
#     @classmethod
#     def step_str(cls, step):
#         key_map = {
#             cls.no_operation: '无操作',
#             cls.pre_process: '预处理',
#             cls.feature_extraction_power: '功率谱特征提取',
#             cls.feature_extraction_low_frequency: '低频线谱特征提取',
#             cls.feature_extraction_modulation: '调制谱特征提取',
#             cls.feature_extraction_listening: '听音特征提取',
#             cls.feature_extraction_aortic_impulse: '主动脉冲特征提取',
#             cls.evaluation_lose: '失真分析',
#             cls.evaluation_quality: '质量评价',
#             cls.excercise_listening: '听音训练'
#         }
#         return key_map[step]

#
# if __name__ == '__main__':
    # active_pulse = ActivePulse()
    # a = SignalTypeEnum.active_pulse.value
    # a = 3
    # print(a)

