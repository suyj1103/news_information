
from celery_tasks.main import app
from utils.yuntongxun.sms import CCP
import logging
logger = logging.getLogger('django')

@app.task(name='send_sms_code')
def send_sms_code(mobile,sms_num,expires,temp_id):
    try:
        result = CCP().send_template_sms(mobile, [sms_num, expires], temp_id)
    except Exception as e:
        logger.error('发送短信异常[mobile : %s message: %s]' % (mobile, e))
    else:
        if result == 0:
            logger.info('发送短信验证码成功[mobile : %s sms_code: %s]' % (mobile, sms_num))
        else:
            logger.warning('发送短信失败 mobile: {}'.format(mobile))
