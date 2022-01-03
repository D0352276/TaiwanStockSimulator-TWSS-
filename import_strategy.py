import os
import sys
import importlib

def UpdateStrategy(strategy_dir):
    all_strategy=os.listdir(strategy_dir)
    fout=open(strategy_dir+"/__init__.py","w")
    for strategy in all_strategy:
        fout.write("from ."+strategy.split(".")[0]+" import *\n")
    fout.close()
    return

def ImportStrategy(strategy_dir,strategy):
    UpdateStrategy(strategy_dir)
    importlib.import_module(strategy_dir)
    return getattr(sys.modules[strategy_dir],strategy)
