import os
from nonebot.adapters.onebot.v11 import Bot
from pathlib import Path
import nonebot_plugin_localstore as store
__KERNEL_VERSION__:str = "V1.12-Public"
# 获取当前工作目录  
current_directory:str = os.getcwd()  
config_dir = store.get_plugin_config_dir()
data_dir = store.get_plugin_data_dir()
if not config_dir.exists():
    config_dir.mkdir()
group_memory = data_dir/"group"
if not group_memory.exists():
    group_memory.mkdir()
private_memory = data_dir/"private"
if not private_memory.exists():
    private_memory.mkdir()
main_config = config_dir/"config.json"
group_prompt = config_dir/"prompt_group.txt"
private_prompt = config_dir/"prompt_private.txt"
custom_models_dir = config_dir/"models"
def init(bot:Bot):
    global config_dir,data_dir
    config_dir = config_dir/bot.self_id
    data_dir = data_dir/bot.self_id

def get_private_memory_dir()->Path:
    return private_memory
def get_group_memory_dir()->Path:
    return group_memory
def get_config_dir()->Path:
    return config_dir
def get_config_file_path()->Path:
    return main_config
def get_current_directory()->str:
    return current_directory
def get_custom_models_dir()->Path:
    return custom_models_dir
def get_private_prompt_path()->Path:
    return private_prompt
def get_group_prompt_path()->Path:
    return group_prompt