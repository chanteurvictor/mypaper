import networkx as nx
import random
from networkx.algorithms import community

# from Girvan_Newman import GN #引用模块中的函数

# 读取文件中边关系，然后成为一个成熟的图,是有一个有效距离的。这里需要加


'''
有效距离的定义：度大点的传播距离较远。目前只有一个指标：根据度数的大小。度数越大，与他相连的边的权重越大。
越不容易传播、越可能在距离比较远的时间传播。以此为方法定义权重。
'''
from sklearn import preprocessing

import numpy as np

np.set_printoptions(threshold=np.inf)


def ContractDict(dir, G):
    with open(dir, 'r') as f:
        for line in f:
            line1 = line.split()
            G.add_edge(int(line1[0]), int(line1[1]))

    for edge in G.edges:
        G.add_edge(edge[0], edge[1], weight=1)
        # randomnum = random.random()
        # G.add_edge(edge[0], edge[1], weight=effectDistance(randomnum))

    return G


import math


def effectDistance(probily):
    return 1 - math.log(probily)


def sigmoid(num):
    sig_L = 0
    sig_L = (1 / (1 + np.exp(-num)))
    return sig_L


def disEffectDistance(weight):
    return math.pow(2, (1 - weight))


def Normalization(x):
    return [(float(i) - min(x)) / float(max(x) - min(x)) for i in x]


def Algorithm1(G, SourceList, time_sum, hlist):
    '''
    我们认为时间片是有问题的，这个时间片应该就是按照，不能是每隔一个时间片就传染一波。只能说每隔一个时间片就记录
    一线。传播也有有概率的。
    '''
    # this  are  two point to  传播
    # 每个传播节点都需要传播，让我们看看那些节点都需要传播
    nodelist = []
    edgelist = []
    infectionNodelist = []

    print('开始传染的点是' + str(SourceList))
    for j in range(len(SourceList)):
        infectList = []
        infectList.append(j)
        G.node[j]['SI'] = 2
        for time in range(0, 5):
            tempinfectList = []
            for node in infectList:
                for height in list(G.neighbors(node)):
                    randnum = random.random()
                    if 0.7< randnum:
                        G.node[height]['SI'] = 2
                        tempinfectList.append(height)
            infectList = tempinfectList
            # for timeInfectnode in tempinfectList:
            #     infectList.append(timeInfectnode)
        print('头两个感染社区点数为' + str(len(set(infectList))))

    return G


# 产生指定感染节点，需要参数节点个数。他们距离的最大值。图G
def contractSource(G, sourceNum, sourceMaxDistance):
    sumlist = list(G.nodes)
    flag = 0
    flag1 = 0
    rumorSourceList = []
    # 先随机找个点，然后找到距离它为>6,小于10的吧。
    while (flag == 0):

        if sourceNum == 1:
            # random_RumorSource = random.randint(0, 7000)
            random_Rumo = random.sample(sumlist, 1)
            random_RumorSource = random_Rumo[0]
            rumorSourceList.append(random_RumorSource)
            flag = 1

        elif sourceNum == 2:
            random_Rumo = random.sample(sumlist, 1)
            random_RumorSource = random_Rumo[0]
            # 在剩下的节点找到我们的第二个点。
            for node in list(G.nodes):
                if nx.has_path(G, node, random_RumorSource) == True:
                    if nx.shortest_path_length(G, node, random_RumorSource) > 4 and nx.shortest_path_length(G, node,
                                                                                                            random_RumorSource) < 6:
                        rumorSourceList.append(node)
                        rumorSourceList.append(random_RumorSource)
                        flag = 1
                        break
        elif sourceNum == 3:
            print('3源点情况。')
            threeNumberFLAG = 0
            while threeNumberFLAG == 0:
                # 先随机找一个点。

                random_RumorSource = random.choice(sumlist)
                # 找第二、三个点。
                for index in range(len(sumlist) - 2):
                    if nx.has_path(G, sumlist[index], random_RumorSource) == True and nx.has_path(G, sumlist[index + 1],
                                                                                                  random_RumorSource) == True:
                        if nx.shortest_path_length(G, source=sumlist[index],
                                                   target=random_RumorSource) > 4 and nx.shortest_path_length(G, source=
                        sumlist[index], target=random_RumorSource) < 6 and nx.shortest_path_length(G, source=sumlist[
                            index + 1], target=random_RumorSource) > 4 and nx.shortest_path_length(G, source=sumlist[
                            index + 1], target=random_RumorSource) < 6:
                            rumorSourceList.append(random_RumorSource)
                            rumorSourceList.append(sumlist[index])
                            rumorSourceList.append(sumlist[index + 1])
                            print('找到了3源点了。')
                            break
                if len(rumorSourceList) == 3:
                    print('找到了3个点')
                    threeNumberFLAG = 1
                    flag = 1
                else:
                    pass

        elif sourceNum == 4:

            flag = 0
            flag1 = 0
            while flag == 0:
                rumorSourceList = []
                random_Rumo = random.sample(sumlist, 1)
                random_RumorSource = random_Rumo[0]
                rumorSourceList.append(random_RumorSource)
                flag1 = 0
                while flag1 == 0:
                    print  ('随机产生的点为' + str(random_RumorSource))
                    resultList = list(nx.dfs_edges(G, source=random_RumorSource, depth_limit=5))
                    # print (resultList)
                    rumorSourceList.append(resultList[6][1])
                    random_RumorSource = resultList[6][1]
                    if len(rumorSourceList) == 4 and len(rumorSourceList) == len(set(rumorSourceList)):  # 重复或者数目达不到要求:
                        print('找到了4个点')
                        flag1 = 1
                        flag = 1
                    elif len(rumorSourceList) == 4 and len(rumorSourceList) != len(set(rumorSourceList)):
                        print ('是四个点，但是却有重复，只能够重新选择新的开始点')
                        flag1 = 1

            # flag1=0
            # while flag1==0:
            #
            #     #随机找个点，然后再找一个点。距离跟他有10个距离就可以。
            #     random_RumorSource = random.choice(sumlist)
            #     rumorSourceList=[random.choice(sumlist),random.choice(sumlist),random.choice(sumlist),random.choice(sumlist)]
            #     combinationList = list(combinations(rumorSourceList, 2))
            #
            #     flag2=0
            #     for sample in combinationList:
            #         if  nx.has_path(G, sample[0],sample[1]) == True:
            #
            #                 flag2=1
            #
            #     if flag2==1:
            #         flag1=0
            #     else:
            #         flag1=1
            # if len(rumorSourceList) != len(set(rumorSourceList)) and len(rumorSourceList) != 4:  # 重复或者数目达不到要求
            #     #有重复元素
            #     flag=0
            # else:
            #     flag=1


        elif sourceNum == 5:
            flag = 0
            flag1 = 0
            while flag == 0:
                rumorSourceList = []
                random_Rumo = random.sample(sumlist, 1)
                random_RumorSource = random_Rumo[0]
                rumorSourceList.append(random_RumorSource)
                flag1 = 0
                while flag1 == 0:
                    print('随机产生的点为' + str(random_RumorSource))
                    resultList = list(nx.dfs_edges(G, source=random_RumorSource, depth_limit=5))
                    # print (resultList)
                    rumorSourceList.append(resultList[4][1])
                    random_RumorSource = resultList[4][1]
                    if len(rumorSourceList) == 5 and len(rumorSourceList) == len(set(rumorSourceList)):  # 重复或者数目达不到要求:
                        print('找到了4个点')
                        flag1 = 1
                        flag = 1
                    elif len(rumorSourceList) == 5 and len(rumorSourceList) != len(set(rumorSourceList)):
                        print('是四个点，但是却有重复，只能够重新选择新的开始点')
                        flag1 = 1

    # 查看产生随机源点的个数2，并且他们距离为3.
    print('源点个数' + str(len(rumorSourceList)) + '以及产生的真实源点是' + str(rumorSourceList))
    # rumorSourceList=[125,4022]   #需要经过5个空。这两个源点。796, 806, 686, 698, 3437, 1085, 1494, 95
    print('真实两源感染是' + str(rumorSourceList))
    return rumorSourceList


import csv


def ConvertGToCsv(G, dir):
    # python2可以用file替代open
    with open(dir, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["source", "target", "weight"])
        for u, v in G.edges():
            # print (G.adj[u][v]['Infection'])
            writer.writerow([u, v, G.adj[u][v]['Infection']])


# 传播子图代入

def ConvertGToCsvSub(G, dir):
    # python2可以用file替代open
    with open(dir, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["source", "target", "weight"])
        for u, v in G.edges():
            # print (G.adj[u][v]['Infection'])
            writer.writerow([u, v, G.adj[u][v]['weight']])


from queues1 import *


def getTuresubinfectionG(infectG, randomInfectionsource):
    infectionNodeList = []
    for nodes in list(infectG.nodes):
        if infectG.node[nodes]['SI'] == 2:
            infectionNodeList.append(nodes)

    return infectionNodeList


def multiplelistTo_ormialy(mutiolist):
    alllist = []
    for i in range(len(mutiolist)):
        for j in range(len(mutiolist[i])):
            alllist.append(mutiolist[i][j])
    return alllist


import random


def getmultipleCommunity(infectionG):
    # return  multipleCommuniytlist
    multipleCommuniytlist = []

    # start  by  a  random  SInode
    randomInfectionNode = 0
    # sum  nodes  in  infect G:
    sumlist = list(infectionG.nodes)
    flag1 = 0
    flag2 = 0
    flag = 0
    while flag == 0:
        infectionList = []
        allList = []
        diff_list = []
        # 刚开始啥社区都没有
        if len(multipleCommuniytlist) == 0:
            print('在没有社区的操作')
            # 刚开始随机产生一个点。
            while flag1 == 0:
                randomnumber = random.sample(sumlist, 1)
                if infectionG.node[randomnumber[0]]['SI'] == 2:
                    randomInfectionNode = randomnumber[0]
                    flag1 = 1
            print('第一个感染社区随机开始的点感染点' + str(randomInfectionNode))
            partion1 = getTuresubinfectionG(infectionG, randomInfectionNode)
            multipleCommuniytlist.append(partion1)  # 第一个社区
            print('把第1个社区加入进去，现在感染社区点个数为' + str(len(multipleCommuniytlist)))
            flag = 1

    print('感染社区个数以及各自人数')
    print(len(multipleCommuniytlist))
    print(len(multipleCommuniytlist[0]))
    return multipleCommuniytlist


# 随机产生一个源点。
def randomSourcelist(subinfectG):
    nodelist = []
    for node in subinfectG:
        nodelist.append(node)
    slice = random.sample(nodelist, 1)
    print('随机产生的源点是' + str(slice))
    sllietemp = slice[0]
    return sllietemp


from itertools import combinations


def getkey(pos, value):
    return {value: key for key, value in pos.iteritems()}[value]


import matplotlib.pyplot  as plt


def findmultiplesource(singleRegionList, infectionG, trueSourcelist, sourceNum):
    # 首先需要判断是否多源。不断找源点去对这个区域。
    tempGraph = nx.Graph()
    tempGraphNodelist = []
    for edge in infectionG.edges:
        # if infectG.adj[edge[0]][edge[1]]['Infection']==2:      #作为保留项。
        if edge[0] in singleRegionList and edge[1] in singleRegionList:
            tempGraph.add_edges_from([edge], weight=1)
            tempGraphNodelist.append(edge[0])
            tempGraphNodelist.append(edge[1])

    print('这个传播子图的节点个数,也是我们用来做u的备选集合的' + str(len(set(tempGraphNodelist))))
    print('这个感染区域的传播图节点个数')
    print(tempGraph.number_of_nodes())
    Alternativenodeset = list(set(tempGraphNodelist))  # 备选集合。
    # 求出这个区域最远的路径出来。返回这个区域半径。
    print('这个感染区域的传播半径')


    minCoverlist = []
    print('在源点在' + str(sourceNum) + '个数的情况下')
    # print('在h为' + str(h) + '的情况下')
    if sourceNum == 1:  # 单源点。
        # 单源情况，怎么办。
        # 用jaya算法，总的list我们知道了的，但是我们也要知道jaya需要的x1和x2空间，注意我这里是离散型数据，就是x1，x2 是离散型的。非连续，怎么办？
        '''
        1 变种jaya算法，首先生成100个种群大小。
        2  然后，算出每个similir，然后有最坏的那个，还有最好的那个。把最坏的那个拿出来，最好的那个拿出来。
        3 开始计算，让其他98个节点，靠近最好（计算最短距离，然后靠近那个店），远离最坏（计算最短距离，不靠近那个店，随便选个点走。）。
        '''
        min = 200
        print('多源情况,先考察同时传播传播')
        print('源点个数为' + str(sourceNum) + '情况')
        # 先判断源点个数，从chooseList中随机挑选两点，进行h构建。
        # combinationList = list(combinations(Alternativenodeset, sourceNum))  # 这是排列组合，再次针对这个排列组合,这是所有的两个
        sourceAndH = []
        for htemp in range(2, 4):
            for sourcetmep in Alternativenodeset:
                sourceAndH.append([sourcetmep, htemp])  # sourceAndH 是所有的东西，就是[source,h]格式。
        # 从combinationList中寻找100个样本集。
        Sampleset = random.sample(sourceAndH, 50)
        print('样本集产生完毕，100个，是' + str(Sampleset))
        bestsourceNews = []
        # 迭代五次
        for i in range(1, 4):
            # 我这里根本不是靠近最优的那个嘛。就是随机，那就随机变好吧。每个都更新一遍。每个都更新，只要变好就行。
            for sourcesi in range(len(Sampleset)):
                print('当前输入list' + str(Sampleset[sourcesi]))
                mincover = getSimilir(Sampleset[sourcesi][0], Sampleset[sourcesi][1], singleRegionList,
                                      infectionG)
                # 往后5个位置找一个比它更好地点。只要找更好就行,找不到就返回不变就可以
                # 当前的下标
                currentindex = sourceAndH.index([Sampleset[sourcesi][0], Sampleset[sourcesi][1]])
                length = len(sourceAndH)
                for j in range(1, 100, 25):  # 要防止数组越界
                    if currentindex + j < length:  # 只要在范围里面才行。
                        lateelement = sourceAndH[currentindex + j]
                        print('当前输入的后面list' + str(lateelement))
                        latemincover = getSimilir(lateelement[0], lateelement[1], singleRegionList, infectionG)
                        if mincover > latemincover:
                            mincover = latemincover  # 有更好地就要替换
                            print("要进行替换了" + str(sourceAndH[sourcesi]) + '被替换成lateelement')
                            Sampleset[sourcesi] = lateelement  # 替换
                            print(Sampleset[sourcesi])

        print('经过5次迭代之后的sample的list为多少呢？' + str(Sampleset))
        # 计算样本集的similir，找出最好的。
        for sources in Sampleset:
            mincover = getSimilir(sources[0], sources[1], singleRegionList, infectionG)
            if mincover < min:
                min = mincover  # 这一次最好的覆盖误差率
                bestsourceNews = sources  # 最好的覆盖误差率对应的最好的那个解。

        print('得到多源点情况最小的覆盖率为' + str(min))
        minCoverlist.append([bestsourceNews[0], bestsourceNews[1], min])


    elif sourceNum == 2:



        #针对tempGraph，计算一个age，就是针对tempGraph。
        DA=0
        L = nx.normalized_laplacian_matrix(tempGraph)
        e = np.linalg.eigvals(L.A)
        print("Largest eigenvalue:", max(e))
        # print("Smallest eigenvalue:", min(e))

        MaxEigenvalue=max(e)
        nodeDaList=[]
        newTempGraph = nx.Graph()
        nodelist=list(tempGraph.nodes)
        for  node  in list(nodelist):
            #计算这个感染图所有的图节点对应的DA值，并统计一定范围的属于某个等级，注意，可能会有多个。
            newTempGraph.clear()
            newTempGraph=tempGraph.copy()
            newTempGraph.remove_node(node)
            L = nx.normalized_laplacian_matrix(newTempGraph)
            e = np.linalg.eigvals(L.A)
            nodeEigenvalue=max(e)
            print (nodeEigenvalue)
            nodeDa=abs(MaxEigenvalue-nodeEigenvalue)/MaxEigenvalue
            print ('--------------------------')
            print(str(node)+'---------'+str(nodeDa))
            nodeDaList.append([node,nodeDa])
        # nodeDaList= sorted(nodeDaList, key=lambda x: (x[1]))
        nodeDaList.sort(key=lambda x: (x[1]),reverse=True)
        print (nodeDaList)
        tempresultlist=nodeDaList[-2:]
        result=[tempresultlist[0][0],tempresultlist[1][0]]
        #
        #依次把从前到后比较

        # for everyNodeIndex in range(len(nodeDaList)-1):
        #     rankList = []
        #     if abs(nodeDaList[everyNodeIndex][1]-nodeDaList[everyNodeIndex+1][1])<0.005:
        #         rankList.append(nodeDaList[everyNodeIndex])
        #         rankList.append(nodeDaList[everyNodeIndex+1])
        #     else:
        #         newrRankList=[]
        #         newrRankList.append(nodeDaList[everyNodeIndex+1])

        return  result














    elif sourceNum == 3:

        resultList = []
        for l in range(0, 4):
            # 随机找两个源，开始
            sourcePartition = []
            randomSource = []
            for number in range(0, sourceNum):
                randomSource.append(random.choice(Alternativenodeset))
                sourcePartition.append([])
            for index in range(len(sourcePartition)):
                sourcePartition[index].append(randomSource[index])
                Alternativenodeset.remove(randomSource[index])
            print (sourcePartition)  # 3个区域划分完毕

            for node in Alternativenodeset:
                # 分别计算到两个源的距离。
                lengthlist = []
                for index1 in range(0, sourceNum):
                    lengthlist.append([index1, randomSource[index1],
                                       nx.shortest_path_length(infectionG, source=node, target=randomSource[index1])])
                resulttemp = sorted(lengthlist, key=lambda x: (x[2]))

                # 加入第一个队列中。
                sourcePartition[resulttemp[0][0]].append(node)

            result = []
            for singlePartition in sourcePartition:

                # ok,接下来已经分割完毕了。sourcePartion1，2就是我们的结果了.在这两个分区中寻找新的点，让目标函数成立。

                # 第一个分区
                nodeAnddistance = []
                for partion1node in singlePartition:  # 计算他们跟其他的距离。
                    nodedistanceSum = 0
                    for targetPartion1node in singlePartition:
                        if partion1node != targetPartion1node:
                            length = nx.shortest_path_length(infectionG, source=partion1node, target=targetPartion1node)
                            nodedistanceSum = nodedistanceSum + length
                    nodeAnddistance.append([partion1node, nodedistanceSum])

                result1 = sorted(nodeAnddistance, key=lambda x: (x[1]))  # 这就是这个源的结果，看看源是多少来着。
                print ('结果看看' + str(result1[0]))
                result.append(result1[0][0])
            return result









    elif sourceNum == 4:
        resultList = []
        for l in range(0, 4):
            # 随机找两个源，开始
            sourcePartition = []
            randomSource = []
            for number in range(0, sourceNum):
                randomSource.append(random.choice(Alternativenodeset))
                sourcePartition.append([])
            for index in range(len(sourcePartition)):
                sourcePartition[index].append(randomSource[index])
                Alternativenodeset.remove(randomSource[index])
            print (sourcePartition)  # 3个区域划分完毕

            for node in Alternativenodeset:
                # 分别计算到两个源的距离。
                lengthlist = []
                for index1 in range(0, sourceNum):
                    lengthlist.append([index1, randomSource[index1],
                                       nx.shortest_path_length(infectionG, source=node, target=randomSource[index1])])
                resulttemp = sorted(lengthlist, key=lambda x: (x[2]))

                # 加入第一个队列中。
                sourcePartition[resulttemp[0][0]].append(node)

            result = []
            for singlePartition in sourcePartition:

                # ok,接下来已经分割完毕了。sourcePartion1，2就是我们的结果了.在这两个分区中寻找新的点，让目标函数成立。

                # 第一个分区
                nodeAnddistance = []
                for partion1node in singlePartition:  # 计算他们跟其他的距离。
                    nodedistanceSum = 0
                    for targetPartion1node in singlePartition:
                        if partion1node != targetPartion1node:
                            length = nx.shortest_path_length(infectionG, source=partion1node, target=targetPartion1node)
                            nodedistanceSum = nodedistanceSum + length
                    nodeAnddistance.append([partion1node, nodedistanceSum])

                result1 = sorted(nodeAnddistance, key=lambda x: (x[1]))  # 这就是这个源的结果，看看源是多少来着。
                print ('结果看看' + str(result1[0]))
                result.append(result1[0][0])
            return result

    elif sourceNum == 5:
        # 两源情况，怎么办。
        # 用jaya算法，总的list我们知道了的，但是我们也要知道jaya需要的x1和x2空间，注意我这里是离散型数据，就是x1，x2 是离散型的。非连续，怎么办？
        '''
        1 变种jaya算法，首先生成100个种群大小。
        2  然后，算出每个similir，然后有最坏的那个，还有最好的那个。把最坏的那个拿出来，最好的那个拿出来。
        3 开始计算，让其他98个节点，靠近最好（计算最短距离，然后靠近那个店），远离最坏（计算最短距离，不靠近那个店，随便选个点走。）。

        '''
        min = 200
        print('多源情况,先考察同时传播传播')
        print('源点为' + str(sourceNum) + '情况')
        # 先判断源点个数，从chooseList中随机挑选两点，进行h构建。
        # combinationList = list(combinations(Alternativenodeset, sourceNum))  # 这是排列组合，再次针对这个排列组合,这是所有的两个
        print('这一步炸了')
        combinationList = []  # 样本集合
        # 随机产生这些可能性，随机生成种群50大小。
        for sampleindex in range(0, 53):
            combinationList.append([random.choice(Alternativenodeset), random.choice(Alternativenodeset),
                                    random.choice(Alternativenodeset), random.choice(Alternativenodeset),
                                    random.choice(Alternativenodeset)])

        sourceAndH = []
        hlists = [2, 3]
        for htemp in range(2, 4):
            for sourcetmep in combinationList:
                sourceAndH.append([sourcetmep, htemp])  # sourceAndH 是所有的东西，就是[source,h]格式。
        # 从combinationList中寻找100个样本集。
        Sampleset = random.sample(sourceAndH, 50)
        print('样本集产生完毕，100个，是' + str(Sampleset))
        bestsourceNews = []
        # 迭代五次
        for i in range(1, 4):
            # 我这里根本不是靠近最优的那个嘛。就是随机，那就随机变好吧。每个都更新一遍。每个都更新，只要变好就行。
            for sourcesi in range(len(Sampleset)):
                print('当前输入list' + str(Sampleset[sourcesi]))
                mincover = getSimilir(Sampleset[sourcesi][0], Sampleset[sourcesi][1], singleRegionList,
                                      infectionG)
                # 随机更换，看如何让变好
                # currentindex = sourceAndH.index([Sampleset[sourcesi][0], Sampleset[sourcesi][1]])
                length = len(sourceAndH)
                for j in range(1, 4, 1):  # 随机变4次，只要能变好
                    lateelement = [[random.choice(Alternativenodeset), random.choice(Alternativenodeset),
                                    random.choice(Alternativenodeset), random.choice(Alternativenodeset),
                                    random.choice(Alternativenodeset)],
                                   random.choice(hlists)]
                    print('当前输入的后面list' + str(lateelement))
                    latemincover = getSimilir(lateelement[0], lateelement[1], singleRegionList, infectionG)
                    if mincover > latemincover:
                        mincover = latemincover  # 有更好地就要替换
                        print("要进行替换了" + str(sourceAndH[sourcesi]) + '被替换成lateelement')
                        Sampleset[sourcesi] = lateelement  # 替换
                        print(Sampleset[sourcesi])

        print('经过5次迭代之后的sample的list为多少呢？' + str(Sampleset))
        # 计算样本集的similir，找出最好的。
        for sources in Sampleset:
            mincover = getSimilir(sources[0], sources[1], singleRegionList, infectionG)
            if mincover < min:
                min = mincover  # 这一次最好的覆盖误差率
                bestsourceNews = sources  # 最好的覆盖误差率对应的最好的那个解。

        print('得到多源点情况最小的覆盖率为' + str(min))
        minCoverlist.append([bestsourceNews[0], bestsourceNews[1], min])
        Comparisonlist = minCoverlist[-2:]  # 取最后两个元素，
        Difference = abs(Comparisonlist[0][2] - Comparisonlist[1][2])
        if Difference == 0:
            print('两次覆盖率一样')
            pass
        elif Difference < 0.00001:
            print('跳出for循环，两次覆盖率几乎相等那么预测源点个数为' + str(sourceNum - 1))

    listToTxt(minCoverlist, 'newresult.txt')
    print(minCoverlist)
    # 返回的应该是最可能的结果。获取mincover最小的返回。第三个元素才是需要考虑东西。
    # listToTxt(minCover, 'result.txt')
    result = sorted(minCoverlist, key=lambda x: (x[2]))
    # listToTxt(result[0], 'newresult.txt')
    return result[0]


def listToTxt(listTo, dir):
    fileObject = open(dir, 'a')
    fileObject.write(str(listTo))
    fileObject.write('\n')
    fileObject.close()


def getSimilir(ulist, hlist, singleRegionList, infectionG):
    '''
    S树-S感染。


    :param ulist:
    :param hlist:
    :param singleRegionList:
    :param infectionG:
    :return:
    '''
    if isinstance(ulist, int):
        circleNodesList = list(nx.bfs_tree(infectionG, source=ulist, depth_limit=hlist).nodes)  # 这包含了这个构建的圆的所有节点。
        # 计算列表相似度试试看
        # print ('感染源的h节点集合为'+str(circleNodesList))
        count = 0
        for i in circleNodesList:
            if i in singleRegionList:
                count = count + 1
        Intersection = list(set(circleNodesList).intersection(set(singleRegionList)))  # 交集
        Union = list(set(circleNodesList).union(set(singleRegionList)))
        ratios = len(Intersection) / len(Union)
        ratio = 1.0 - ratios
        print('在u为' + str(ulist) + 'h为' + str(hlist) + '情况下的覆盖率' + str(ratio))
        return abs(ratio)



    else:
        # 多源点,获得多源点的覆盖率
        circleNodesList = []
        for u in ulist:
            circleNodesList.extend(list(nx.bfs_tree(infectionG, source=u, depth_limit=hlist).nodes))
        circleNodesListnew = list(set(circleNodesList))
        count = 0
        for i in circleNodesList:
            if i in singleRegionList:
                count = count + 1
        # count
        Intersection = list(set(circleNodesList).intersection(set(singleRegionList)))  # 交集
        Union = list(set(circleNodesList).union(set(singleRegionList)))  # 并集
        ratios = len(Intersection) / len(Union)
        ratio = 1.0 - ratios
        print('在u为' + str(ulist) + 'h为' + str(hlist) + '情况下的覆盖率' + str(ratio))

        return abs(ratio)


import sys


def getListfortxt(rootdir):
    lines = []
    with open(rootdir, 'r') as file_to_read:
        while True:
            line = file_to_read.readline()
            if not line:
                break
            line = line.strip('\n')
            lines.append(line)

    lists = [x for x in lines if x != []]
    return lists


'''
this   function  :   to  get  sourcelist fo  everyRegionList  and   caluce  every  distance of  source and result


'''

import math


def multiplePartion(mutiplelist, infectionG, rumorSourceList, sourceNume):
    # 所有单源list
    allsigleSourceList = []
    allSigleSourceListNum = [2, 1]

    # 将第一个传播区域定下来。
    import datetime
    starttime = datetime.datetime.now()
    # long running,这里可以读的文件代替，就比较省时间。反正都是为了allsigleSourcellist填充

    '''   这个是保留项，我觉得反转算法有点问题，反正（u,h是写完了）,下面这个很好时间'''
    for sigleReionlist in mutiplelist:
        allsigleSourceList.append(findmultiplesource(sigleReionlist, infectionG, rumorSourceList, sourceNume))

    resultSource = []

    for sigleRegionSource in allsigleSourceList:
        if isinstance(sigleRegionSource, int):  # 单源点
            print('算出来的误差率最低单源点情况---------------------------')
            for source in sigleRegionSource:
                resultSource.append(source)
        elif len(sigleRegionSource) == 2:
            for source in sigleRegionSource:
                resultSource.append(source)
        elif len(sigleRegionSource) == 3:
            for source in sigleRegionSource:
                resultSource.append(source)
        elif len(sigleRegionSource) == 4:
            for source in sigleRegionSource:
                resultSource.append(source)
        elif len(sigleRegionSource) == 5:
            for source in sigleRegionSource:
                resultSource.append(source)

    print('总的用反转算法算出来的结果为' + str(resultSource))

    errordistanceFor = []
    # 上面这两个，可以干一架了。
    for turesourcelist in rumorSourceList:  # 真实源
        everydistion = []
        for resultsourceindex in resultSource:  # 自己算法找出的源。
            everydistion.append(nx.shortest_path_length(infectionG, source=turesourcelist, target=resultsourceindex))
        everydistion.sort()
        print(everydistion)
        errordistanceFor.append(everydistion[0])

    multipdistance = 0
    for error in errordistanceFor:
        multipdistance = multipdistance + error

    # errordistance=nx.shortest_path_length(infectionG,source=resultSource[0],target=rumorSourceList[0])
    print('误差距离为' + str(multipdistance))
    return multipdistance / len(errordistanceFor)


import numpy as np
import matplotlib.pyplot as plt


def plotform(x, y):
    x = range(1, 4)
    y_train = [1.0, 1.4, 1.1, 1.225, 1.44]
    y_test = [2.53, 2, 31, 2.12, 1]
    # plt.plot(x, y, 'ro-')
    # plt.plot(x, y1, 'bo-')
    # pl.xlim(-1, 11)  # 限定横轴的范围
    # pl.ylim(-1, 110)  # 限定纵轴的范围

    plt.plot(x, y_train, marker='o', mec='r', mfc='w', label='our method')
    plt.plot(x, y_test, marker='*', ms=10, label='other method')
    plt.legend()  # 让图例生效

    plt.margins(0)
    plt.subplots_adjust(bottom=0.10)
    plt.xlabel('Number of sources')  # X轴标签
    plt.ylabel("Average error  (in hops)")  # Y轴标签
    plt.title("Wiki-Vote  data")  # 标题
    plt.savefig('f1.png')
    plt.show()


import datetime

if __name__ == '__main__':

    starttime = datetime.datetime.now()
    '''

    1  产生一个社区，无非就是源点从1到5.然后用我们这种方式
    判断准确率。
    '''

    # 1 产生这个图。

    #  制造这个图
    Ginti = nx.Graph()
    # 初始化图,加很多节点
    # for index in range(1,1005):
    #     print (index)
    #     Ginti.add_node(index)

    # 构建图，这个图是有有效距离的。
    G = ContractDict('../data/email-Eu-core.txt', Ginti)

    # 因为邮件是一个有向图，我们这里构建的是无向图。
    print('一开始图的顶点个数', G.number_of_nodes())
    print('一开始图的边个数', G.number_of_edges())

    #  先给全体的Cn、Scn,time的0的赋值。
    for node in list(G.nodes):
        G.add_node(node, SI=1)

    # 初始化所有边是否感染。Infection
    for edge in list(G.edges):
        G.add_edge(edge[0], edge[1], Infection=1)
    print('这个图产生完毕')

    sourceList = []
    #  从1个源点产生到5个源点。但都是有交集的。按照交叉领域来比较？
    #
    # for  sourceNumber  in  range(1,4):
    #     sourceList.append(contractSource(G,sourceNumber,2))
    # print (sourceList)
    #
    # print ('产生3源点成功------------------------------------------')

    # 产生10次，每次都有误差，计算出来。并统计。

    for i in range(1, 11):
        sourceList.append(contractSource(G, 2, 2))


    errordistanceList = []  # 误差集合。
    errorSum = 0

    # 对每一个单源点都有这个操作。
    for singleSource in sourceList:
        #  先给全体的Cn、Scn,time的0的赋值。
        for node in list(G.nodes):
            G.add_node(node, SI=1)
        # 初始化所有边是否感染。Infection
        for edge in list(G.edges):
            G.add_edge(edge[0], edge[1], Infection=1)
        # 开始之前都要刷新这个图，
        infectG = Algorithm1(G, singleSource, 2, 6)
        print('源点传播成功')
        #  找社区，按照代理，只能找到一个社区的。
        multipList = getmultipleCommunity(infectG)
        errordistance = multiplePartion(multipList, infectG, singleSource, 2)
        errorSum = errorSum + errordistance
        errordistanceList.append(errordistance)
        print('误差集合为' + str(errordistanceList))
    print(errorSum / 10)

    # long running

    endtime = datetime.datetime.now()
    print('执行了这么长时间')
    print((endtime - starttime).seconds)





















