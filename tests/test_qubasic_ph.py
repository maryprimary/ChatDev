"""
测试QuBasicInfoPhase
"""

import logging
import os
import sys

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

chat_chain = ChatChain(config_path=config_path,
                       config_phase_path=config_phase_path,
                       config_role_path=config_role_path,
                       task_prompt="公司A的股票是否值得关注？",
                       project_name="Test",
                       org_name="TestCompany",
                       model_type=ModelType.QWEN_MAX,
                       code_path="")

# ----------------------------------------
#          Init Log
# ----------------------------------------
logging.basicConfig(filename=chat_chain.log_filepath, level=logging.INFO,
                    format='[%(asctime)s %(levelname)s] %(message)s',
                    datefmt='%Y-%d-%m %H:%M:%S', encoding="utf-8")

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
