class Scope:
    allow_api = []
    allow_module = []
    forbidden = []

    # 运算符重载  实现对象和对象直接相加
    def __add__(self, other):
        self.allow_api = self.allow_api + other.allow_api
        self.allow_api = list(set(self.allow_api))  # 转成集合去重

        self.allow_module = self.allow_module + other.allow_module
        self.allow_module = list(set(self.allow_module))  # 转成集合去重

        self.forbidden = self.forbidden + other.forbidden
        self.forbidden = list(set(self.forbidden))  # 转成集合去重

        return self  # 返回实例对象，使其能够支持链式调用


class AdministratorScope(Scope):
    allow_api = ['v1.file+export_data', ]
    allow_module = ['v1.admin', 'v1.ffile', 'v1.evaluation']

    def __init__(self):
        self + InstructorScope()
        pass

    pass


class InstructorScope(Scope):
    # allow_api = []
    forbidden = ['v1.file+export_data', ]
    allow_module = ['v1.user', 'v1.type', 'v1.sound', 'v1.file', 'v1.pretreatment', 'v1.feature', 'v1.classification',
                    'v1.evaluation','v1.ffile','v1.teacher']
    # def __init__(self):
    #     self + AdminScope()
    pass


class StudentScope(Scope):
    allow_api = ['v1.user+get_role_count', 'v1.user+update_nickname', 'v1.user+update_password', 'v1.type+get_rn_type',
                 'v1.type+get_te_type', 'v1.type+get_ap_type', 'v1.type+get_as_type', 'v1.type+get_countries',
                 'v1.type+get_power_engine', 'v1.type+get_propeller','v1.sound+sound_detail',
                 'v1.sound+sound_list','v1.sound+sound_list_new', 'v1.sound+search_sounds', 'v1.sound+search_sounds_stype',
                 'v1.sound+search_sounds_fleet_name', 'v1.sound+search_sounds_depth', 'v1.sound+search_sounds_platform',
                 'v1.sound+search_sounds_task', 'v1.sound+search_sounds_location', 'v1.sound+search_sounds_ct',
                 'v1.sound+search_sounds_power_engine', 'v1.sound+search_sounds_propeller',
                 'v1.sound+search_sounds_country', 'v1.sound+search_sounds_ap', 'v1.sound+search_sounds_as',
                 'v1.sound+search_sounds_rn', 'v1.sound+search_sounds_te', 'v1.sound+all_version_asc',
                 'v1.sound+all_version_desc', 'v1.sound+search_sounds_distance', 'v1.sound+search_sounds_speed',
                 'v1.sound+search_sounds_water', 'v1.sound+search_sounds_pm', 'v1.sound+search_sounds_am',
                 'v1.file+picture_url', 'v1.file+audio_url', 'v1.file+now_version_url', 'v1.file+now_version_path',
                 'v1.file+duplicate_url', 'v1.file+duplicate_path',
                 'v1.feature+getMCFFbyURL', 'v1.feature+getZero_CrossingbyURL', 'v1.feature+feature_power',
                 'v1.feature+feature_onethree', 'v1.feature+amalysis_demon', 'v1.feature+amalysis_lofar',
                 'v1.feature+feature_ms',
                 'v1.pretreatment+get_tips', 'v1.pretreatment+save_tips', 'v1.pretreatment+roll_back',
                 'v1.pretreatment+reset', 'v1.pretreatment+save', 'v1.pretreatment+edit_audio', ]
    allow_module = ['v1.classification', 'v1.evaluation','v1.ffile','v1.student']
    pass
    # def __init__(self):
    #     self + UserScope() + AdminScope()
    #     self.forbidden = []


# 这里的endpoint 会带有蓝图v1 例如  v1.super_get_user
def is_in_scope(scope, endpoint):
    # endpoint = blueprint.view_function
    # globals() 实现'反射'
    # globals 会将当前模块下的类转换为字典
    scope = globals()[scope]()  # 根据scope 实例化一个权限对象scope
    # 分离出 模块名，以便进行模块级别的验证
    splits = endpoint.split('+')
    red_name = splits[0]
    if endpoint in scope.allow_api:
        return True
    if endpoint in scope.forbidden:
        return False
    if red_name in scope.allow_module:
        return True

    else:
        return False
