from qiniu import Auth
import json
def qiniutoken():
    ak = "hvNEDY7K1pYh_hS0pGLGpztuHnE2UoAVcUTRHGYN"
    sk = "M_pJxubIeA71x6RoQ_Qk5mP55Gncy1Jks3qNalCn"
    q = Auth(ak, sk)
    bucket_name = 'pjbbs'  # 仓库的名字
    token = q.upload_token(bucket_name)
    return json.dumps({'uptoken': token})