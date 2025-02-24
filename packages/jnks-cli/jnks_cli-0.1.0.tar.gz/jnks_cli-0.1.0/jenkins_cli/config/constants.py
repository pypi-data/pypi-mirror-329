"""Constants used throughout the application"""
import os

CONFIG_DIR = os.path.expanduser("~/.jenkins")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.yaml")
LOCAL_CONFIG = ".jenkins.yaml"