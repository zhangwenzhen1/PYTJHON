# -*- coding: utf-8 -*-
import ConfigParser
import commands
import logging
import time
import threading

#自定义线程对象 获取返回值
class MyThread(threading.Thread):
    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None

#程序入口
def startTask():
    dic = getCof()
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    DATE_FORMAT = "%Y/%d/%m %H:%M:%S %p"
    logging.basicConfig(filename=dic['filename'], level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)
    executeSQL = "SELECT \"icpomp\".\"MAKE_DATA_PREPARE\"();"
    command = dic['psql']+""" -U %s -h %s -p %s -d %s --command '%s' """ % (
        dic['username'], dic['host'], dic['port'], dic['dbname'],executeSQL)
    # 执行主方法 MAKE_DATA_PREPARE
    executePgCommand(executeSQL, command, "MAKE_DATA_PREPARE")
    #并发执行五大厂商
    threads = []
    sqls = ["SELECT \"icpomp\".\"MAKE_DATA_UPLOAD_PRE_HUA\"();","SELECT \"icpomp\".\"MAKE_DATA_UPLOAD_PRE_ZX\"();",
            "SELECT \"icpomp\".\"MAKE_DATA_UPLOAD_PRE_NOK\"();","SELECT \"icpomp\".\"MAKE_DATA_UPLOAD_PRE_ERIC\"();",
            "SELECT \"icpomp\".\"MAKE_DATA_UPLOAD_PRE_DT\"();"]
    for sql in sqls:
        threadName = sql[17:-4]
        command = dic['psql']+""" -U %s -h %s -p %s -d %s --command '%s' """ % (
            dic['username'], dic['host'], dic['port'], dic['dbname'], sql)
        t = MyThread(executePgCommand, args=(sql,command,threadName))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    logging.info("-----------------------------------------五大厂商执行完成----------------------------------------------------------")
    # 五大厂商执行完成
    # 执行TEST_HUA_ECELL_3
    t = threading.Thread(target=huacell3, args=("/usr/bin/python ./huacell3.py",))
    t.start()
    logging.info("-----------------------------------------开始执行 TEST_HUA_ECELL_3------------------------------------------------------------")
    # 并行跑五大厂商子过程
    threads = []
    sqls = ["SELECT \"icpomp\".\"TEST_HUA_ECELL_1\"(current_date);",
            "SELECT \"icpomp\".\"TEST_HUA_ECELL_2\"(current_date);",
            "SELECT \"icpomp\".\"TEST_HUA_ENODEB_1\"(current_date);",
            "SELECT \"icpomp\".\"TEST_HUA_ENODEB_2\"(current_date);",
            "SELECT \"icpomp\".\"TEST_HUA_ENODEB_3\"(current_date);",
            "SELECT \"icpomp\".\"MAKE_DATA_UPLOAD_SIMPLE_ZX\"(current_date);",
            "SELECT \"icpomp\".\"MAKE_DATA_UPLOAD_COMPLEX_ZX\"(current_date);",
            "SELECT \"icpomp\".\"MAKE_DATA_UPLOAD_NEW_NOK\"(current_date);"
            ]
    for sql in sqls:
        threadName = sql[17:-16]
        command = dic['psql'] + """ -U %s -h %s -p %s -d %s --command '%s' """ % (
            dic['username'], dic['host'], dic['port'], dic['dbname'], sql)
        t = MyThread(executePgCommand, args=(sql, command, threadName))
        t.setName(threadName)
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    logging.info("-----------------------------------------------------------五大厂商子过程除了(TEST_HUA_ECELL_3) 其它都执行完了!!!-------------------------------------------------")
    #五大厂商子过程除了(TEST_HUA_ECELL_3) 其它都执行完了,

    # 并行跑如下函数
    # --select icpomp."GET_JT_IM_PARA_CHECK_RRU"(CURRENT_DATE);
    # --select icpomp."GET_JT_IM_PARA_CHECK_DATA"(CURRENT_DATE);
    # --select icpomp."GET_XGPC_COUNT_DATA"(CURRENT_DATE);
    # --select icpomp."GET_JT_PARA_CHECK_VOLTE_V2"();
    # --select icpomp."GET_PLAN_DATA_NEW"()";
    # --select icpomp."GET_GPXG_DATA"();
    allthreads = []
    sqls = [
            "SELECT \"icpomp\".\"GET_JT_IM_PARA_CHECK_DATA\"(current_date);",
            "SELECT \"icpomp\".\"GET_JT_IM_PARA_CHECK_RRU\"(current_date);",
            "SELECT \"icpomp\".\"GET_XGPC_COUNT_DATA\"(current_date);",
            "SELECT \"icpomp\".\"GET_GT_PARA_CHECK_DATA\"(CURRENT_DATE);",
            "SELECT \"icpomp\".\"GET_JT_PARA_IMPORT_PRO\"();",
            "SELECT \"icpomp\".\"UPDATE_SY_HPI_CSDB\"();"
            ]
    #不带参截取方法不一样
    noParameterSql = ["SELECT \"icpomp\".\"GET_JT_PARA_CHECK_VOLTE_V2\"();",
                      "SELECT \"icpomp\".\"GET_PLAN_DATA_NEW\"();",
                      "SELECT \"icpomp\".\"GET_GPXG_DATA\"();",
                      "SELECT \"icpomp\".\"GET_CHECK_SWITCH_DATA\"();",]
    for sql in noParameterSql:
        threadName = noParameterSql[17:-4]
        command = dic['psql']+""" -U %s -h %s -p %s -d %s --command '%s' """ % (
            dic['username'], dic['host'], dic['port'], dic['dbname'], sql)
        t = MyThread(executePgCommand, args=(sql,command,threadName))
        allthreads.append(t)
        t.start()
    for sql in sqls:
        threadName = sql[17:-16]
        command = dic['psql']+""" -U %s -h %s -p %s -d %s --command '%s' """ % (
            dic['username'], dic['host'], dic['port'], dic['dbname'], sql)
        t = MyThread(executePgCommand, args=(sql,command,threadName))
        allthreads.append(t)
        t.start()
    for t in allthreads:
        t.join()
        if "GET_JT_IM_PARA_CHECK_DATA" in t.get_result():
            #   --select icpomp."GET_JT_PARA_DETAILED_LIST"(CURRENT_DATE);
            # 执行VACUUM
            t = threading.Thread(target=vacuumImpList, args=("/usr/bin/python ./vacuumImpList.py",))
            t.start()
            t.join()
            logging.info("-----------------------------------------VACUUM for important parameter 完成------------------------------------------------------------")

            sql = "SELECT \"icpomp\".\"GET_JT_PARA_DETAILED_LIST\"(current_date);"
            threadName = sql[17:-16]
            command = dic['psql'] + """ -U %s -h %s -p %s -d %s --command '%s' """ % (
                dic['username'], dic['host'], dic['port'], dic['dbname'], sql)
            t1 = MyThread(executePgCommand, args=(sql, command, threadName))
            t1.start()
            t1.join()
    executeSQL = "SELECT \"icpomp\".\"generate_core_table_check\"();"
    command = dic['psql'] + """ -U %s -h %s -p %s -d %s --command '%s' """ % (
        dic['username'], dic['host'], dic['port'], dic['dbname'], executeSQL)
    # 执行方法 generate_core_table_check
    executePgCommand(executeSQL, command, "generate_core_table_check")


    pass

#获取配置文件信息
def getCof():
    # 读取配置文件
    conf = ConfigParser.ConfigParser()
    conf.read("./config.ini")
    # 获取pg配置信息
    username = conf.get('postgresql', 'username')
    password = conf.get('postgresql', 'password')
    dbname = conf.get('postgresql', 'db')
    host = conf.get('postgresql', 'host')
    port = conf.get('postgresql', 'port')
    psql = conf.get('postgresql', 'psql')
    # 获取日志配置信息 logging日志打印配置
    filename = conf.get('logging', 'filename')
    filename = filename + time.strftime("%Y-%m-%d", time.localtime()) + ".log"
    list = [('username', username), ('password', password), ('dbname', dbname), ('host', host), ('port', port),
            ('filename', filename),('psql',psql)]
    dic = dict(list)
    return dic

#执行pgSQL线程
def executePgCommand(sql,command,threadName):
    time_start = time.time()
    logging.info('执行函数[' + sql + ']')
    status, output = commands.getstatusoutput(command)
    if status != 0:
        logging.error('执行函数['+sql+"]出错:")
        logging.error('出错信息:'+output)
    else:
        logging.info('执行函数['+sql+"]完成:")
        logging.info(output)
    time_end = time.time()
    logging.info("执行函数["+sql+"]耗时"+str((time_end-time_start))+"秒")
    return threadName


def huacell3(execommand):
    commands.getoutput(execommand)
    pass

def vacuumImpList(execommand):
    commands.getoutput(execommand)
    pass

if __name__ == '__main__':
    startTask()
