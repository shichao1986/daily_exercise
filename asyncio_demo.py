# -*- coding: utf-8 -*-
"""
时间: 2019/10/11 11:28

作者: shichao

更改记录:

重要说明:异步IO的事件驱动（asyncio.get_event_loop()）能够驱动fd，和task（future），如果要使用协程，需要通过loop
为我们调度任务的执行。本demo介绍三种协程的使用方式：反应堆模式、多任务并发、异步任务回调
上边三种关于协程的用法覆盖了大部分的使用场景，欢迎补充O(∩_∩)O
"""

import asyncio
import functools
import random
import time
import threading

# 模拟异步IO的协程，返回str类型的应答
async def async_stub_get_response(response:str='async-response') -> str:
    await asyncio.sleep(5)
    return response

# 设计模式为反应堆模式时的协程应用,程序启动后完全靠事件驱动
# 这种模式下我们需要加入一个永久循行的任务来做整个程序业务的驱动，例如tornado通过加入httpserver（基于fd的驱动）
# 常见的基于socket的server端都可以使用这种方式，参考tornado.TcpServer的实现
# 本例中使用func1作为永久运行的任务（基于task的驱动）
def mainthread_loop():

    async def func2():
        print('func2 run one time start')
        response = await async_stub_get_response('func2 response')
        # 对于开发人员来说，此后的语句更像是同步操作
        print('get result:{}'.format(response))
        return 'abc'

    # 回调函数的参数是Task（future）
    # arg1 和arg2 传递业务参数
    def func2_callback(f, arg2, arg1):
        print('func2_callback:{}'.format(f))
        print('business args:{}'.format((arg1, arg2)))

    async def func1():
        idx = 1
        while True:
            print('before sleep,idx={}'.format(idx))
            if idx % 10 == 0:
                print('add a new task to eventloop')
                newtask = asyncio.get_event_loop().create_task(func2())
                # 回调函数根据业务需要进行配置，如果不需要回调则不需要添加
                # 使用偏函数为回调函数携带多余的参数
                newtask.add_done_callback(functools.partial(func2_callback, arg1=1, arg2=2))
            await asyncio.sleep(1)
            idx += 1
            print('after sleep')

    loop = asyncio.get_event_loop()
    loop.create_task(func1())

    loop.run_forever()

    assert False, 'never been here!!!/(ㄒoㄒ)/~~'

# 多任务并发时使用协程，这种使用协程的方式一般是解决固定数量的任务，一次性的使用
# 本例模拟多个任务同时执行，每个任务耗时在2-4秒
def multitask_loop():

    # 模拟原有业务执行，然后我们突然有多个并发任务想快速处理
    print('business in processing...')
    time.sleep(3)

    # 定义协程
    async def task1(a, b, c):
        print('start one task...')
        await asyncio.sleep(2 + random.random()*2)
        print('task finished')

    arg = [1,5,10]
    k = lambda a: random.shuffle(a) or a
    # 生成协程list
    tasks = [task1(*k(arg)) for i in range(10)]

    loop = asyncio.get_event_loop()

    start = time.time()
    print('Start concurrent task, time is {}'.format(start))
    # gather函数将多个协程聚合
    loop.run_until_complete(asyncio.gather(*tasks))
    end = time.time()
    use_time = end - start
    print('Concurrent task finished, time is {}, use {}'.format(end, use_time))

    # 原有业务继续干其他事
    print('business in processing...')
    while True:
        time.sleep(1)


# 异步任务回调与反应堆模式在使用协程的方式上相似，只是在软件设计模式上有所不同，
# 本例的设计模式为异步执行回调模式，ioloop运行在一个守护线程中，本用例的使用方式
# 适用于那些软件架构已经固定，不可修改、不易修改以及不便于以反应堆模式实现的场景
readytask = []
def callback_loop():

    cond = threading.Condition()

    loop = asyncio.get_event_loop()

    global readytask
    # 启动一个守护线程运行eventloop, eventloop 需要被传递到线程
    def loop_run(loop):
        global readytask
        while True:
            # print('eventloop[{}] therad is running...'.format(id(loop)))
            with cond:
                if len(readytask) == 0:
                    cond.wait()
                fs = readytask[:]
                readytask = []
            # print('get asynctask notify')
            try:
                loop.run_until_complete(asyncio.gather(*fs))
            except Exception as e:
                print(e)

    # 主程序启动时需要启动守护线程
    threading.Thread(target=loop_run, args=(loop, ), daemon=True).start()

    # 这个就是一个异步任务
    async def asynctask(idx):
        # print('do one asynctask begin...')
        resp = await async_stub_get_response('task response')
        print('asynctask finished:{}'.format(idx))
        return idx

    # 这个是异步任务的回调
    def task_cb(f):
        result = f.result()
        print('asynctask callback and result is :{}'.format(result))

    # import pdb; pdb.set_trace()
    def run_async_task(idx):
        print('add async task {}'.format(idx))
        atask = loop.create_task(asynctask(idx))
        atask.add_done_callback(task_cb)

        with cond:
            readytask.append(atask)
            cond.notify()

    # 原有业务与异步任务一起运行，我们周期的创建一个异步任务，并用idx记录他们的执行
    print('business in processing...')
    idx = 1
    while True:
        time.sleep(1)
        if idx <= 50:
            run_async_task(idx)
            idx += 1


if __name__ == '__main__':
    # mainthread_loop()

    # multitask_loop()

    callback_loop()