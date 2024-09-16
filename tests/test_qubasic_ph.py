"""
测试QuBasicInfoPhase
"""

import logging
import logging.handlers
import os
import sys
import time
import traceback
import numpy

from datetime import datetime, timedelta
from camel.typing import ModelType

root = '/Users/mary/workspace/QuChatDev'
sys.path.append(root)

from chatdev.chat_chain import ChatChain

try:
    from openai.types.chat.chat_completion_message_tool_call import ChatCompletionMessageToolCall
    from openai.types.chat.chat_completion_message import FunctionCall

    openai_new_api = True  # new openai api version
except ImportError:
    openai_new_api = False  # old openai api version
    print(
        "Warning: Your OpenAI version is outdated. \n "
        "Please update as specified in requirement.txt. \n "
        "The old API interface is deprecated and will no longer be supported.")


from qufetcher import get_stock_codes, get_stock_bars
from qufetcher.basicinfo import get_mr_score, get_liuwp_score


config_dir = os.path.join(root, "CompanyConfig/Scholar")
print(config_dir)
config_files = [
    "ChatChainConfig.json",
    "PhaseConfig.json",
    "RoleConfig.json"
]

config_paths = []

for config_file in config_files:
    company_config_path = os.path.join(config_dir, config_file)
    print(company_config_path)
    config_paths.append(company_config_path)

config_path, config_phase_path, config_role_path = config_paths


# Start ChatDev

# ----------------------------------------
#          Init ChatChain
# ----------------------------------------

def get_report_by_code(code):
    _task_prompt_json = r'''
    {{
        "task": "公司A的股票是否会上涨？",
        "stock_code": "{}"
    }}
    '''.format(code)
    print(_task_prompt_json)
    chat_chain = ChatChain(config_path=config_path,
                        config_phase_path=config_phase_path,
                        config_role_path=config_role_path,
                        task_prompt=_task_prompt_json,
                        project_name="Test",
                        org_name="TestCompany",
                        model_type=ModelType.QWEN_MAX,
                        code_path="")

    # ----------------------------------------
    #          Init Log
    # ----------------------------------------
    print(chat_chain.log_filepath)
    print(chat_chain.start_time)
    time.sleep(2)
    #return ""
    logging.basicConfig(level=logging.INFO,
                        format='[%(asctime)s %(levelname)s] %(message)s',
                        datefmt='%Y-%d-%m %H:%M:%S', encoding="utf-8")
    logger = logging.getLogger()
    for hd in logger.handlers:
        logger.removeHandler(hd)
    handler = logging.FileHandler(chat_chain.log_filepath)
    logger.addHandler(handler)
    
    # ----------------------------------------
    #          Pre Processing
    # ----------------------------------------

    chat_chain.pre_processing()

    # ----------------------------------------
    #          Personnel Recruitment
    # ----------------------------------------

    chat_chain.make_recruitment()

    # ----------------------------------------
    #          Chat Chain
    # ----------------------------------------

    chat_chain.execute_chain()

    # ----------------------------------------
    #          Post Processing
    # ----------------------------------------

    chat_chain.post_processing()

    finaldir = os.path.join(root + "/WareHouse", "_".join(["Test", "TestCompany", chat_chain.start_time]))
    fid = open(os.path.join(finaldir, "manual.md"))
    ret = fid.read()
    fid.close()
    return ret

#
def send_result(content):
    try:
        from tests.test_send_email import sendemail
        sendemail("000001.SZ", content)
    except Exception as e:
        print(e)


def print_today_need_att():
    '''输出今日值得关注'''
    need_att = []
    #
    #for id, cont in df.iterrows():
    fid = open("tests/SZCodes.txt")
    lines = fid.readlines()
    fid.close()
    for lin in lines[:10]:
        ents = lin.split()
        code = ents[0]
        name = ''.join(ents[1])
        print(code, name)
        now = datetime.now()
        d40 = now - timedelta(40)
        try:
            #40天的数据
            dataf = get_stock_bars(code+'.SZ', d40.strftime(r"%Y%m%d"), now.strftime(r"%Y%m%d"))
            time.sleep(0.5)
            mrz = get_mr_score(code+'.SZ', dataf=dataf)
            liuwp = get_liuwp_score(code+'.SZ', dataf=dataf)
            #
            flag1 = mrz < -1.5
            flag2 = liuwp.at[liuwp.index[-1], 'cls_rolling_max'] < 0.7
            flag3 = numpy.all(liuwp.loc[liuwp.index[-20:], 'cls_rolling_min'] > 1.0)
            if flag1:# and flag2 and flag3:
                need_att.append(code+'.SZ')
        except Exception:
            traceback.print_exc()
            continue
    #
    print(len(need_att))
    fid = open("tests/__pycache__/need_att.txt", 'w')
    fid.write('\n'.join(need_att))
    fid.close()



def main():
    '''拉取一次所有的股票'''
    #df = get_stock_codes()
    #df.to_csv('tests/__pycache__/sc.csv')
    #
    #print_today_need_att()
    #return
    fid = open("tests/__pycache__/need_att.txt")
    need_att = [lin.strip() for lin in fid.readlines()]
    fid.close()
    #return
    #
    can_trade = []
    det_reprt = ""
    for na in need_att:
        #try:
        report = get_report_by_code(na)
        #except Exception as e:
        #    print(e)
        #    print(na + "没能正确运行")
        #    report = ""
        #    continue
        zdidx = report.find("是")
        print(zdidx)
        if report[zdidx-1] != "不":
            can_trade.append(na)
            det_reprt += na + "\n"
            det_reprt += report + "\n"
    print(can_trade)
    print(det_reprt)
    fid = open("tests/__pycache__/output.txt", 'w')
    fid.write(" ".join(can_trade) + '\n')
    fid.write(det_reprt + '\n')
    fid.close()


if __name__ == "__main__":
    main()


