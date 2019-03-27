#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import logging.config
import os
import pymysql.cursors
import shutil
import sys
import zipfile

if __name__=="__main__":
    logging.basicConfig(filename = os.path.join("../","data", 'log.txt'), level = logging.DEBUG)
    log = logging.getLogger('root')


    dbconn=pymysql.Connect(
        host="10.1.92.67",
        database="tphh_report",
        user="tphhadmin",
        password="Tphhadmin@123",
        port=3306,
        charset='utf8'
    )
    # dbconn=pymysql.Connect(
    #     host="localhost",
    #     database="yanwei_mall",
    #     user="root",
    #     password="yeli",
    #     port=3306,
    #     charset='utf8'
    # )
    dbconn.autocommit(True)

    file_path=r"d:\桌面文件\桌面\huihui\交易-payment\files\101"
    table_name=["statis_expenditure_file","statis_expenditure_detail"]
    account_id=101
    pay_mode=1#日结
    # 执行sql语句
    try:
        dbcursor=dbconn.cursor()
        true_flag=True
        if true_flag is True:
        # with dbconn.cursor() as cursor:
            # 执行sql语句，插入记录
            sql1 = 'INSERT INTO {} (file_date,settlement_id,total_amount,account_id,settlement_type,pay_mode,start_time,end_time)' \
                  ' VALUES (%s,%s, %s, %s, %s, %s,%s,%s)'.format(table_name[0])
            sql2='INSERT INTO {}(file_date,settlement_id,settlement_type,account_id,order_id,order_amount,' \
                 'actual_amount,merchant_id,order_type,organ_type,order_organ_id,order_organ_name,order_amount_time,' \
                 'payer_id,payer_name,sys_order_id,refund_id,refund_amount,application_time)' \
                 ' VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'.format(table_name[1])
            print(sql1)
            print(sql2)

            # for i in range(0,5):
            #     print("正在插入数据：" + str(i))
                # cursor.execute(sql, (data.iloc[i,0], data.iloc[i,1], data.iloc[i,2],data.iloc[i,3],data.iloc[i,4],data.iloc[i,5],data.iloc[i,6],data.iloc[i,7]))
                # # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
                # dbconn.commit()



    # config=configparser.ConfigParser()
    # config.readfp(open("default.ini"))
    # prod_news_mysql_config = config.get("default", "prod_news_mysql_config").strip()
    # logging.getLogger().info("init prod_news_mysql_config connection for " + prod_news_mysql_config )



        if os.path.isdir(file_path) is False:
            log.error("invalid file_path:{}".format(file_path))
            pass
        tmp_path=file_path+r"\tmp"
        log.debug("tmp_path:{}".format(tmp_path))
        if os.path.isdir(tmp_path):
            shutil.rmtree(tmp_path)
            # os.remove(tmp_path)
            os.mkdir(tmp_path)
        else:
            os.mkdir(tmp_path)

        # settelment重复
        settles=[]
        insert_list_f=[]
        insert_list_d=[]

        for dir_path,_,dir_files in os.walk(file_path):
            for file in dir_files:
                file_date=file.split(".")[0]
                log.info("file:{},file_date:{}".format(file,file_date))
                fullpath=os.path.join(dir_path,file)
                log.info("deal zip file:{}".format(fullpath))
                shutil.rmtree(tmp_path)
                os.mkdir(tmp_path)

                zf=zipfile.ZipFile(fullpath,'r')
                zf.extractall(tmp_path)
            # if tarfile.is_tarfile(fullpath):
            #         t=tarfile.open(fullpath)
            #         t.extract(tmp_path)
                for tmp_file_path,_,txt_files in os.walk(tmp_path):
                    for txt_file in txt_files:
                        tmp_settleId="0"
                        insert_list_d.clear()
                        insert_list_f.clear()
                        filepath=os.path.join(tmp_file_path,txt_file)
                        log.info("deal json file:{}".format(filepath))
                        # print("d:{},f:{}".format(tmp_file_path,txt_file))
                        settlement_type=1 if"income"==txt_file.split("-")[0] else 2
                        # if filepath.contains("income"):
                        #     continue
                        size=os.path.getsize(filepath)
                        log.info(" file:{} as size:{}".format(filepath,size))
                        if size<10:
                            log.info("ignore file:{} as size:{}".format(filepath,size))
                            continue
                        for line in open(filepath,'r',encoding='UTF-8'):
                            a=line.strip()
                            # print(a)
                            b=json.loads(a)
                            if tmp_settleId=="0":
                                insert_list_f.append((file_date,b["settlementId"],float(b["totalAmount"])*100000,account_id,settlement_type,pay_mode,b["startTime"],b["endTime"]))
                            elif b["settlementId"]!=tmp_settleId:
                                log.error("conflict settlement_id in file:{},tmp_s:{},settle:{}".format(filepath,tmp_settleId,b["settlementId"]))
                                insert_list_f.append((file_date,b["settlementId"],float(b["totalAmount"])*100000,account_id,settlement_type,pay_mode,b["startTime"],b["endTime"]))
                            tmp_settleId= b["settlementId"]
                            detail=b["orderInfo"]
                            insert_list_d.append((file_date,tmp_settleId,settlement_type,account_id,detail["orderId"],float(detail["orderAmount"])*100000,float(detail["actualAmount"])*100000
                             ,detail["orderMerchantName"],detail["orderType"],detail["orgnType"],detail["orderOrgnId"],detail["orderOrgnName"],
                            detail.get("orderAmountTime"),detail["buyerId"],detail["buyerName"],detail["sysOrderId"],
                            detail.get("refundId"),0 if detail.get("refundAmount") is None else float(detail.get("refundAmount"))*100000,detail.get("refundTime")))
                            # print(insert_list_d)
                            # print(insert_list_f)
                            # print(sql2)
                            # print(b)
                        log.info("settle size:{},detail size:{}".format(len(insert_list_f),len(insert_list_d)))
                        dbcursor.executemany(sql1,insert_list_f)
                        dbcursor.executemany(sql2,insert_list_d)
                        dbconn.commit()
                        # sys.exit(0)

        dbcursor.close()
    except Exception as e:
        print(e)
        print("Error{}".format(e.args))
        sys.exit(1)
    finally:
        dbconn.close()
        print ('数据已插入，插入数据库成功！')

