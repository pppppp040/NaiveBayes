import os
import math
import numpy as np

ROOTPATH='D:\机器学习数据\sy发的数据\clean_data_frequence'
categories=  ['健康', '商业', '娱乐', '教育', '文化', '游戏', '烦恼', '生活', '电脑', '社会']#注意不可改变顺序！！！！
global cateCount
CATENUM=10#类别总数
global VOCABULARYNUM
global bigDic
global gmatrix

def form_big_dic():
    # 构造所有类别的词典
    global bigDic
    bigDic = dict()
    contents = os.listdir(ROOTPATH)  # 电脑、烦恼、健康。。。。
    for each in contents:  # each是电脑、烦恼、健康等某一类
        if os.path.isdir(ROOTPATH + '\\' + each):  # 判断是文件夹，打开
            bigDic[each] = read_file(ROOTPATH + '\\' + each + '\\' + 'dict.txt')
    # print(bigDic)
    # print(len(bigDic['电脑']))


#读一个字典向量文件，返回一个字典
def read_file(filepath):
    with open(filepath) as fp:
        content=fp.read();
        book=content.split('\n')
        d=dict();
        for each in book:
            if each:#each不为空
                temp=each.split()
                # print(temp)
                d[temp[0]]=int(temp[1])
    return d


def P(word,vj):
    # P(wk|vj)=(nk+1) / (n+|Vocabulary|)
    nk=bigDic[vj].get(word,0)#单词wk出现在Textj中的次数，若没有出现，则为0
    n=cateCount[vj]
    ans=(nk+1) / (n+VOCABULARYNUM)
    return ans

# V为所有类的向量，text为待分类文本string，返回值为分类结果
def Vnb(text,V):
    max=-9999999999999999999999999999999999999
    tans=0
    retu=''
    l=text.split()
    for j in V:#对于每一类
        for word in l:#对弈一篇文本中的每一个单词
            tans=tans+math.log(P(word,j),10)
        # print("tans=",tans)
        if tans>max:
            max=tans
            retu=j
        tans=0
    # print("j=",retu,"max=",max)
    return retu

def cal_cateCount(categories):
    n=0
    for vj in categories:#each为健康等类别
        for key in bigDic[vj]:
            # print("key=",key)
            n = n + bigDic[vj][key]

        cateCount[vj]=n
        n=0

def classify_all_texts(rootpath,matrix):
    contents = os.listdir(rootpath)  # 电脑、烦恼、健康。。。。
    # print(contents)#注意顺序！！！
    for each in contents:  # each是电脑、烦恼、健康等某一类
        if os.path.isdir(rootpath + '\\' + each):  # 判断是文件夹，打开
            texts = os.listdir(rootpath + '\\' + each + '\\' + 'test')
            for text in texts:
                with open(rootpath + '\\' + each + '\\' + 'test' + '\\' + text, encoding='utf-8') as fp:
                    string = fp.read()
                    vj = Vnb(string, categories)
                    i = categories.index(each)  # 实际值
                    j = categories.index(vj)  # 预测值
                    matrix[i][j][0] += 1
    print(matrix)

def cal_precision_and_recall(matrix):
    precisionList = []
    recallList = []
    for j in range(CATENUM):  # 先对列进行遍历
        sum = 0
        for i in range(CATENUM):
            sum = sum + matrix[i][j][0]

        a = matrix[j][j][0]
        recall = a / 5000
        precision = a / sum
        precisionList.append(precision)
        recallList.append(recall)
        print("类别：", categories[j])
        print("a:", a)
        print("sum:", sum)
        print("precision={} , recall={}".format(precision, recall))

    total_precision = np.mean(precisionList)
    total_recall = np.mean(recallList)
    print("total_precision={} , total_recall={}".format(total_precision, total_recall))


if __name__ == '__main__':
    # 计算十万篇文本的单词总数
    book=read_file(ROOTPATH+'\\'+"total_dict.txt")
    VOCABULARYNUM=len(book)
    # print(book)
    print("VOCABULARY=",VOCABULARYNUM)

    #构造所有类别的词典
    form_big_dic()

    #计算每一类的位置总数
    cateCount=dict()
    cal_cateCount(categories)
    print(cateCount)

    #测试一篇文章
    # with open("D:\机器学习数据\sy发的数据\clean_data _newdict\电脑\\test\\test20.txt", encoding='utf-8') as fp:
    #     string = fp.read()
    #     vj=Vnb(string,categories)

    #对所有文章进行分类
    gmatrix = [[[0] for j in range(CATENUM)] for i in range(CATENUM)]
    classify_all_texts(ROOTPATH,gmatrix)

    #计算准确率和召回率
    cal_precision_and_recall(gmatrix)