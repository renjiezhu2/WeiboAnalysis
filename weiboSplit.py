#!/usr/bin/python
# coding:utf-8

# Check whether string contains Chinese character or not
# def check_contain_chinese(check_str):
#    for ch in check_str.decode('utf-8'):
#        if u'\u4e00' <= ch <= u'\u9fff':
#            return True
#    return False

inputFileName = raw_input("Enter a file name for input File: \n")

outputAll = open("./WeiboInLine.txt", "wb")
outputGene = open("./WeiboInLineGene.txt", "wb")
outputGeneClean = open("./WeiboInLineGeneClean.txt", "wb")
outputNetwork = open("./WeiboNetwork.txt", "wb")

with open(inputFileName) as f:
    # Record weibo id for each user to filter duplicate weibo
    weiboIdDic = {}

    for line in f:
        # Empty the list for every user
        weiboIdDic.clear()

        weiboClip = line.split("||	||")
        for element in weiboClip:
            if element:
                if element.find("./UserWeibos") == -1:
                    wordClip = element.split("\t")
                    weiboId = wordClip[0]

                    if weiboIdDic.has_key(weiboId) == False:
                        weiboIdDic.update({weiboId: 0})
                        outputAll.write(element + "\n")

                        if element.find("转基因") != -1:
                            outputGene.write(element + "\n")
                            # Write out the weibo in format:
                            # 转发者，转发内容， 源微博作者， 源微博内容；源微博作者， 源微博内容
                            index = 1
                            for word in wordClip:
                                if index == 2:
                                    outputGeneClean.write(word.strip())
                                else:
                                    if index == 3 or index == 50 or index == 51:
                                        outputGeneClean.write("\t" + word.strip())
                                index += 1
                            outputGeneClean.write("\n")

                            # Build Network for Page Rank
                            validRecord = True
                            if wordClip[1] != "" and wordClip[49] != "":
                                user_1 = wordClip[1]
                                user_2 = ""

                                if wordClip[2].find("//@") != -1:
                                    userClip = wordClip[2].split("//@")
                                    #Normal Flow
                                    if userClip[1].find(":") != -1:
                                        user = userClip[1][0:userClip[1].find(":")].split()

                                        if len(user) > 1:
                                            # To Cope With Case: //@飞翔的烟囱 回复@古海游:
                                            user_2 = user[0]
                                        # To Cope With Case: //@飞翔的烟囱:
                                        else:
                                            user_2 = userClip[1][0:userClip[1].find(":")]
                                            # To Cope With Case: //@:
                                            if user_2 == "":
                                                validRecord = False
                                    # To Cope With Case (no : between user and weibo content): //@飞翔的烟囱 .....
                                    else:
                                        user = userClip[1].split()
                                        user_2 = user[0]
                                else:
                                    user_2 = wordClip[49]

                                if validRecord:
                                    outputNetwork.write(user_1 + "\t" + user_2 + "\n")

outputAll.close()
outputGene.close()
outputGeneClean.close()
outputNetwork.close()
