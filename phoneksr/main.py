#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import argparse
import os
sys.path.append("/home/ljs/ksr/PcKsr/")
sys.path.append("/home/ljs/ksr/ServerKsr/")
sys.path.append("/home/ljs/ksr/FstClient/")
sys.path.append("/home/ljs/ksr/Swype")
sys.path.append("/home/ljs/ksr/PhoneKsr")
sys.path.append("/home/ljs/ksr/RnnKsr")
from ksrCalPc import ksrCal as ksrCalPc
from ksrCal3Gram import ksrCal as ksrCal3Gram
from ksrCalServer import ksrCal as ksrCalServer
from ksrCalFst import ksrCal as ksrCalFst
from swypeCal import swypeCal
from rnn import ksrCal as ksrCalRnn
logPath = "/home/ljs/ksr/log"
import PhoneTrigger as Phone
import ksrCalPc as PC
import ksrCalServer as SERVER
import ksrCalFst as FST
writeFileFlag = False
PC.writeFileFlag = writeFileFlag
SERVER.writeFileFlag = writeFileFlag
FST.writeFileFlag = writeFileFlag

def retFun(s):
    print s
    return s

def main():
    if not os.path.exists(logPath):
        os.mkdir(logPath)
    os.chdir(logPath)
    parser = argparse.ArgumentParser()
    product_choices = ['cmk', 'cmk_rnn', 'kika', 'gboard', "swift_key", 'typany', 'go', 'swype',
                       'aitype']
    type_choices = ['fst', 'server', 'pc', "swype", 'pc3gram']
    parser.add_argument('--input_file',  '-i', help = '--input_file filename(full path)')
    parser.add_argument('--output_file', "-o", default = "result.txt" , help = '--output_file  filename(full path)', )
    parser.add_argument('--product','-p', default = "cmk", choices = product_choices, help = '--product_type')
    parser.add_argument('--date_published','-d', default = "December 26, 2017", help = '--date_published, the publish date of test app')
    parser.add_argument('--type','-t', default = "pc", choices = type_choices, help = '--input_file  filename(full path)')
    parser.add_argument('--predict', type = int, default = 0, choices = [0, 1],help = '--predict 0 1')
    parser.add_argument('--language', '-l', default = "en")
    parser.add_argument('--dict', default = None , help = "Pc dict name")
    parser.add_argument('--history', type = int, default = 0, choices = [0, 1], help = 'Pc --history 0 1')
    parser.add_argument('--topn', type = int, default = 1, choices = range(1,19), help = '--topn 1~18')
    parser.add_argument('--lm_file', default = None, help = "fst model file(full path)")
    parser.add_argument('--lexicon_file', default = None, help = "fst dict file(full path)")
    parser.add_argument('--named_file', default = None, help = "fst named file(full path)")
    parser.add_argument('--trans_file', default = None, help = "fst trans file(full path)")
    # fst出词概率阈值
    parser.add_argument('--fst_threshold', default = 0.0, type = float, help = "->the word probability threshold")
    # fst词组惩罚系数, 词组惩罚参数,越小越不可能出词组, 默认为10即可
    parser.add_argument('--fst_word_group_threshold', default = 10.0, type = float, help = "the word group penalty coefficient")
    args = parser.parse_args()
    inputFile = args.input_file
    outputFile = args.output_file
    product = args.product
    date_published = args.date_published
    kind = args.type.lower()
    predict = args.predict
    language = args.language
    dictFile = args.dict
    history = args.history
    topn = int(args.topn)
    lm_file = args.lm_file
    lexicon_file = args.lexicon_file
    named_file = args.named_file
    trans_file = args.trans_file
    fst_threshold = args.fst_threshold
    fst_word_group_threshold = args.fst_word_group_threshold
    if not product or product not in product_choices:
        return retFun("product must in " + ''.join(product_choices))
    if not kind or kind not in type_choices:
        return retFun("type must in " + ''.join(type_choices))
    if not outputFile:
        return retFun("output can not null")
    if kind in ("fst",):
        if fst_threshold > 1 or fst_threshold < 0:
            return retFun("fst_threshold must in [0, 1]")
        for filename in (lm_file, ):
            if not filename or not os.path.exists(filename):
                return retFun("%s can not exist"%filename)
        for filename in (named_file, trans_file):
            if filename and not os.path.exists(filename):
                return retFun("%s can not exist"%filename)
    if product in product_choices[:1] and kind in ("pc", "swype", "pc3gram") \
            and (not dictFile or not os.path.exists(dictFile)):
        return retFun("kind = pc, dict can not null and dict must exists, dict = %s"%dictFile)
    if not inputFile or not os.path.exists(inputFile):
        return retFun("input = %s , input not exists"%inputFile)
    print "inputFile = %s"%str(inputFile)
    print "outputFile = %s"%str(outputFile)
    print "product = %s"%str(product)
    print "date_published = %s"%str(date_published)
    print "type = %s"%str(kind)
    print "predict = %s"%str(predict)
    print "dict = %s"%str(dictFile)
    print "history = %s"%str(history)
    print "language = %s"%str(language)
    print "topn = %s"%str(topn)
    print "lm_file = %s"%lm_file
    print "lexicon_file = %s"%lexicon_file
    print "named_file = %s"%named_file
    print "trans_file = %s"%trans_file
    print "fst_threshold = %s"%fst_threshold
    print "fst_word_group_threshold = %s"%fst_word_group_threshold
    ret = []
    if product_choices[0] == product:
        if "pc3gram" in kind:
            ret = ksrCal3Gram(inputFile, dictFile, language, outputFile, topn, predict)
        elif "pc" in kind:
            # ksrCalPc(textName, dictName, language, outputFileName, topn = 3, predict = False, history = False)
            ret = ksrCalPc(inputFile, dictFile, language, outputFile, topn, predict, history)
        elif "server" in kind:
            # ksrCalServer(inputFile, outputFile, language, predict, top)
            ret = ksrCalServer(inputFile, outputFile, language, predict, topn)
        elif "fst" in kind:
            ret = ksrCalFst(inputFile, outputFile, language, predict, topn,
                            lm_file, lexicon_file, named_file, trans_file,
                            fst_threshold, fst_word_group_threshold)
        elif "swype" in kind:
            # swypeCal(dictFile, inputFile, language)
            ret = swypeCal(dictFile, inputFile, language, outputFile)
        else:
            return retFun("type = %s error"%kind)
    elif product_choices[1] == product:
        ret = ksrCalRnn(inputFile, outputFile)
    else:
        ret = Phone.trigger_phone_task(product, date_published, inputFile, parse_task_id(outputFile))

    for i in ret:
        print i
    return ret


def parse_task_id(output):
    # /data1/shiny-server/dict_lab/www/result/task_
    task_prefix = 'task_'
    index = output.find(task_prefix)
    output = output[index + task_prefix.__len__():]
    index = output.find('/')
    return output[:index]


if __name__ == "__main__":
    # python main.py -i /home/ljs/ksr/data/ksr200.txt -o /home/ljs/ksr/log/output --dict /home/ljs/ksr/data/main_en.dict --predict 1 -t pc
    # python main.py -i /home/ljs/ksr/data/ksr200.txt -o /home/ljs/ksr/log/output --dict /data2/share/ljs/temp/main_en_US.dict --predict 1 -t pc3gram
    # python main.py -i /home/ljs/ksr/data/ksr200.txt -o /home/ljs/ksr/log/output --lexicon_file /data1/weisk/git/fstServer/fst/so/data2/1gram.dat --lm_file /data1/weisk/git/fstServer/fst/so/data2/en_fst.mod --predict 1 -t fst
    # python main.py -i /home/ljs/ksr/data/fst/test_en.txt -o /home/ljs/ksr/log/fst0710 --lexicon_file /home/ljs/ksr/data/fst/0710/1gram.dat --lm_file /home/ljs/ksr/data/fst/0710/en_fst.mod --predict 1 -t fst --topn 3
    # python main.py -i /home/ljs/ksr/data/ksr200.txt -o /home/ljs/ksr/log/output --predict 1 -t server
    # python main.py -i /home/ljs/ksr/data/swype1000.txt --dict /home/ljs/ksr/data/main_en.dict -t swype
    main()
