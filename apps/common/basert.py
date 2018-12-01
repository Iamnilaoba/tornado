


class Basecode(object):
    SUCCESS = 200  # 成功
    UNAUTHERROR = 401  # 没有权限
    PARAMERR = 402  # 参数错误

class Basert(object):
    def __init__(self,code,msg,data=None):
        self.code=code
        self.msg=msg
        self.data=data

def reSuccess(msg,data=None):
    return Basert(code=Basecode.SUCCESS,msg=msg,data=data).__dict__

def respParamErr(msg="参数错误",data=None):
    return Basert(code=Basecode.PARAMERR,msg=msg,data=data).__dict__

def respUnAutherr(msg="没有访问权限"):
    return Basert(code=Basecode.UNAUTHERROR,msg=msg).__dict__
