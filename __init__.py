# -*- coding: utf-8 -*-
import subprocess
import functools
from itertools import chain

from plugin import blueprint, menu, plugin_load, plugin_unload, plugin_info

def prefix_function(oldfunction, wrapfunction):
    @functools.wraps(oldfunction)
    def run(*args, **kwargs):
        return wrapfunction(oldfunction, *args, **kwargs)
    return run

def to_str_list(obj):
    if(isinstance(obj, str)):
        return [obj]
    return obj

def popen_hook(popen, command, *args, **kwargs):
    headers = None
    header_idx = None
    for elem in command:
        if('-headers' in elem):
            header_idx = command.index(elem)
            headers = elem.split(' ')
    if(headers is not None):
        command = list(chain(*map(to_str_list, [command[:header_idx] + command[header_idx+1:]])))
        input_idx = command.index('-i')
        command = list(chain(*map(to_str_list, [command[:input_idx], headers[:-1], command[input_idx], headers[-1], command[input_idx+1:]])))
    return popen(command, *args, **kwargs)

subprocess.Popen = prefix_function(
    subprocess.Popen, popen_hook)