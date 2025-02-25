import asyncio
from collections.abc import Sequence
import inspect
import json
import os
import subprocess

import numpy as np


class JuliaBridge:
    def __init__(self, timeout: int = 5):
        self._included_files = []
        self._added_pkgs = []
        self._options = []
        self._timeout = timeout
        self._result = None  # 用于存储 Julia 函数的返回值
        self._index = 0  # 用于跟踪当前迭代的位置
        self._temp_dir = os.path.join(os.path.dirname(__file__), '.temp')
        os.makedirs(self._temp_dir, exist_ok=True)

    def __iter__(self):
        # 重置迭代器状态
        self._index = 0
        return self

    def __next__(self):
        if self._result is None:
            raise StopIteration('No result available to iterate over')

        if self._index >= len(self._result):
            raise StopIteration  # 停止迭代

        # 返回当前值并更新索引
        value = self._result[self._index]
        self._index += 1
        return value

    def __getattr__(self, name):
        def method(*args, **kwargs) -> Sequence | None:
            # 调用 Julia 函数
            if self.__init_julia(
                name,
                *args,
                included_files=self._included_files,
                added_pkgs=self._added_pkgs,
                **kwargs,
            ):
                try:
                    result = asyncio.run(self.__run_julia(self._timeout))
                    if result is not None:
                        return result  # 返回可迭代的结果（列表或元组）
                    else:
                        print('\033[93mNo result returned from Julia\033[0m')
                except Exception as e:
                    print(f'Error running Julia: {e}')
            else:
                raise ValueError('Failed to initialize Julia function')

        return method

    def add_option(self, *options: str) -> None:
        self._options.extend(options)

    def remove_option(self, *options: str) -> None:
        for option in options:
            if option in self._options:
                self._options.remove(option)

    def include(self, *modules: str) -> 'JuliaBridge':
        # 添加 include 模块
        for module in modules:
            full_path = self.__get_full_path_from_caller(module)
            self._included_files.append(full_path)
        return self

    def add_pkg(self, *pkgs) -> 'JuliaBridge':
        # 添加包
        self._added_pkgs.extend(pkgs)
        return self

    def __get_full_path_from_caller(self, subpath: str) -> str:
        """根据调用者的路径获取文件的绝对路径"""
        # 获取调用栈
        stack = inspect.stack()
        # 获取调用者的帧
        caller_frame = stack[2]
        # 获取调用者的文件名
        caller_filename = caller_frame.filename
        # 获取调用者的绝对路径
        caller_dir = os.path.dirname(os.path.abspath(caller_filename))
        # 拼接路径
        return os.path.join(caller_dir, subpath)

    def __init_julia(self, func: str, *args, included_files=None, added_pkgs=None, **kwargs) -> bool:
        try:
            # 将 numpy 数组转换为列表，并记录参数类型和维度数
            args_list = []
            args_type = []
            args_dim = []  # 用于记录每个 ndarray 的维数

            for arg in args:
                if isinstance(arg, np.ndarray):
                    args_list.append(arg.tolist())
                    args_type.append('ndarray')
                    args_dim.append(arg.shape)  # 保存 ndarray 的形状
                else:
                    args_list.append(arg)
                    args_type.append(type(arg).__name__)
                    args_dim.append(None)  # 对于非 ndarray，设置为 None

            kwargs_list = {}
            kwargs_type = {}
            kwargs_dim = {}  # 用于记录 kwargs 中 ndarray 的维数
            for k, v in kwargs.items():
                # 跳过 include 模块和 added_pkgs
                if k in ['included_files', 'added_pkgs']:
                    continue
                if isinstance(v, np.ndarray):
                    kwargs_list[k] = v.tolist()
                    kwargs_type[k] = 'ndarray'
                    kwargs_dim[k] = v.shape  # 保存 ndarray 的形状
                else:
                    kwargs_list[k] = v
                    kwargs_type[k] = type(v).__name__
                    kwargs_dim[k] = None  # 对于非 ndarray，设置为 None

            # 创建 payload，并将维度数信息一起存储
            payload = {
                'func': func,
                'args': args_list,
                'argstype': args_type,
                'argsdim': args_dim,  # 添加 ndarray 的形状
                'kwargs': kwargs_list,
                'kwargstype': kwargs_type,
                'kwargsdim': kwargs_dim,  # 添加 kwargs 中 ndarray 的形状
                'included_files': included_files,  # 添加 include 模块
                'added_pkgs': added_pkgs,  # 添加包
            }

            with open(os.path.join(self._temp_dir, 'payload.json'), 'w') as f:
                json.dump(payload, f)
            return True
        except Exception as e:
            print(e)
            return False

    async def __run_julia(self, timeout: int) -> Sequence | None:
        # 获取 main.py 文件所在目录，并构建 bridge.jl 的路径
        script_dir = os.path.dirname(os.path.abspath(__file__))  # 获取当前脚本所在目录
        # 构建命令行参数
        command = ['julia'] + self._options + [os.path.join(script_dir, 'bridge.jl')]

        # 创建并启动 subprocess 进程
        process = subprocess.Popen(command, stdout=None)

        # 使用 asyncio 的 wait_for 设置超时
        task = asyncio.create_task(self.__wait_for_result(timeout))

        # 等待进程或超时
        done, pending = await asyncio.wait([task], timeout=timeout)

        # 超时后终止进程
        if task in pending:
            process.kill()
            print('\033[1;35mJulia process killed due to timeout\033[0m')
            raise TimeoutError('Timed out waiting for result.json')

        # 进程没有超时的情况下处理结果
        if await task:
            try:
                with open(os.path.join(self._temp_dir, 'result.json')) as f:
                    result = json.load(f).get('result')
                    return result
            except Exception as e:
                print(f'Error reading or processing result.json: {e}')
            finally:
                # 删除 result.json, finished
                if os.path.exists(os.path.join(self._temp_dir, 'result.json')):
                    os.remove(os.path.join(self._temp_dir, 'result.json'))
                if os.path.exists(os.path.join(self._temp_dir, 'finished')):
                    os.remove(os.path.join(self._temp_dir, 'finished'))
        else:
            process.kill()
            print('\033[1;35mJulia process killed due to timeout\033[0m')
            raise TimeoutError('Timed out waiting for result.json')

    async def __wait_for_result(self, timeout: int) -> bool:
        try:
            # 使用 asyncio.wait_for 设定超时
            result = await asyncio.wait_for(self._wait_for_file(), timeout)
            if result:
                print('\033[1;32mJulia process finished\033[0m')
            return result
        except TimeoutError:
            print('\033[1;31mTimeout reached\033[0m')
            return False

    async def _wait_for_file(self):
        # 检查文件是否存在
        while not os.path.exists(os.path.join(self._temp_dir, 'finished')):
            await asyncio.sleep(0.1)
        return True
