import re, os, numpy, math, sys, pandas as pd

def removePostfix(word):
    postfix=['ور', 'وں', 'ے','یوں','ؤں','یاں','یں','ئیں', 'دار', 'کی', 'ی']
    predictedStem=word
    # یوں
    checkPostfix=re.search(rf"{postfix[0]}\Z", word)
    checkPostfix=re.search(rf"{postfix[3]}\Z", word)
    if checkPostfix:    
        predictedStem = word[:checkPostfix.span(0)[0]]
        predictedStem=predictedStem+'ی'
        return predictedStem
    # ئیں
    checkPostfix=re.search(rf"{postfix[7]}\Z", word)
    if checkPostfix:    
        predictedStem = word[:checkPostfix.span(0)[0]]
        return predictedStem
    # ور
    if checkPostfix: 
        predictedStem = word[:checkPostfix.span(0)[0]-1]#check with your own corpus
        return predictedStem
    # وں
    checkPostfix=re.search(rf"{postfix[1]}\Z", word)
    if checkPostfix:    
        predictedStem = word[:checkPostfix.span(0)[0]]
        return predictedStem
    # ے
    checkPostfix=re.search(rf"{postfix[2]}\Z", word)
    if checkPostfix:    
        predictedStem = word[:checkPostfix.span(0)[0]]
        predictedStem=predictedStem+'ا'
        return predictedStem
    # ؤں
    checkPostfix=re.search(rf"{postfix[4]}\Z", word)
    if checkPostfix:    
        predictedStem = word[:checkPostfix.span(0)[0]]
        return predictedStem
    # یاں
    checkPostfix=re.search(rf"{postfix[5]}\Z", word)
    if checkPostfix:    
        predictedStem = word[:checkPostfix.span(0)[0]]
        predictedStem=predictedStem+'ی'
        return predictedStem
    # یں
    checkPostfix=re.search(rf"{postfix[6]}\Z", word)
    if checkPostfix:    
        predictedStem = word[:checkPostfix.span(0)[0]]
        return predictedStem
    # # دار
    # checkPostfix=re.search(rf"{postfix[8]}\Z", word)
    # if checkPostfix:    
    #     predictedStem = word[:checkPostfix.span(0)[0]]
    #     return predictedStem
    # # کی
    # checkPostfix=re.search(rf"{postfix[9]}\Z", word)
    # if checkPostfix:    
    #     predictedStem = word[:checkPostfix.span(0)[0]]
    #     return predictedStem
    # ی
    # checkPostfix=re.search(rf"{postfix[10]}\Z", word)
    # if checkPostfix:    
    #     predictedStem = word[:checkPostfix.span(0)[0]]
    #     return predictedStem
    
    return predictedStem

def removePrefix(word):
    prefix=['نیم', 'کم ', 'اہل', 'بد', 'بے', 'لا', 'نا', 'ذیلی']
    predictedStem=word
    # بے
    checkPrefix = re.search(rf'\A{prefix[4]}', word)
    if checkPrefix:    
        predictedStem = word[checkPrefix.span(0)[-1]:]
        return predictedStem
    # بد
    checkPrefix = re.search(rf'\A{prefix[3]}', word)
    if checkPrefix:    
        predictedStem = word[checkPrefix.span(0)[-1]:]
        return predictedStem
    # نیم
    checkPrefix = re.search(rf'\A{prefix[0]}', word)
    if checkPrefix:    
        predictedStem = word[checkPrefix.span(0)[-1]:]
        return predictedStem
    # کم
    checkPrefix = re.search(rf'\A{prefix[1]}', word)
    if checkPrefix:    
        predictedStem = word[checkPrefix.span(0)[-1]:]
        return predictedStem
    # اہل
    checkPrefix = re.search(rf'\A{prefix[2]}', word)
    if checkPrefix:    
        predictedStem = word[checkPrefix.span(0)[-1]:]
        return predictedStem
    # لا
    checkPrefix = re.search(rf'\A{prefix[5]}', word)
    if checkPrefix:    
        predictedStem = word[checkPrefix.span(0)[-1]:]
        return predictedStem
    # نا
    checkPrefix = re.search(rf'\A{prefix[6]}', word)
    if checkPrefix:    
        predictedStem = word[checkPrefix.span(0)[-1]:]
        return predictedStem
    # ذیلی
    checkPrefix = re.search(rf'\A{prefix[7]}', word)
    if checkPrefix:    
        predictedStem = word[checkPrefix.span(0)[-1]:]
        return predictedStem
    return predictedStem
        

def stopwordsList():
    stopwords = open('Urdu Stopwords.txt', "r", encoding="utf-8")
    stopwords=stopwords.readlines()
    for i in range(len(stopwords)):
        stopwords[i]=stopwords[i].replace('\n', '')
    return stopwords


def wordsToRemove(file):
    stopwords=stopwordsList()
    listToRemove=[]
    for stopword in stopwords:
        for wordIndex in range(len(file)):
            if(stopword==file[wordIndex]):
                listToRemove.append(wordIndex)
    listToRemove=[*set(listToRemove)]
    return listToRemove


# Remove unwanted symbols
def removeExtras(string):
    remove=['؛', '،', '٫', '؟', '۔', '٪', ':', '?', '’', '”', '@', '“']
    string=string.replace(remove[0], '').replace(remove[1], '').replace(remove[2], '')
    string=string.replace(remove[3], '').replace(remove[4], '').replace(remove[5], '')
    string=string.replace(remove[6], '').replace(remove[7], '').replace(remove[8], '')
    string=string.replace(remove[9], '').replace(remove[10], '').replace(remove[11], '')
    string=string.replace('  ', ' ')
    return string

# Remove stopwords from the given list of words
def removeStopwords(file):
    listToRemove=wordsToRemove(file)
    # print(listToRemove)
    listToRemove.sort()
    for wordIndex in range(len(listToRemove)-1, -1, -1):
        del file[listToRemove[wordIndex]]
    # print(file)
    return file


# Apply stemming to the given list of words
def applyStemming(file):
    for wordIndex in range(len(file)):
        file[wordIndex]=removePrefix(file[wordIndex])
        file[wordIndex]=removePostfix(file[wordIndex])
    return file

# return term ids stored in our list of all given words inthe query
def term_ids(query):
    totalTerms=open('term_ids.txt', "r", encoding="utf-8").readlines()
    termids=list()
    for word in query:
        # print(word)
        for term in totalTerms:
            term=term.split('\n')[0].split('\\')
            # print(term)
            if(term[1]==word):
                termids.append(int(term[0]))
                break
    return termids

# return document frequencies of all given termids
def df(termids):
    termIndex=open('terms_info.txt', "r", encoding="utf-8").readlines()
    dfs=list()
    for id in termids:
        for term in termIndex:
            term=term.split('\n')[0].split('\\')
            if(int(term[0])==id):
                # print(term[2])
                dfs.append(int(term[2]))
                break
    return dfs


def init_list_of_objects(size, terms):
    list_of_objects = list()
    for i in range(0,size):
        list_of_objects.append( [0]*terms ) #different object reference each time
    return list_of_objects

# return term frequencies in a document of all given termids
def tf(termids):
    docids=open('docids.txt', "r", encoding="utf-8").readlines()
    tfs=init_list_of_objects(len(docids), len(termids))
    term_index=open('inverted_term_index.txt', "r", encoding="utf-8").readlines()
    ind=-1
    for id in termids:
        ind+=1
        for term in term_index:
            term=term.split('\n')[0].split('\\')
            # print(term, '\n')
            doc=0
            tfdoc=0
            if(int(term[0])==id):
                # print(term[0])
                for i in range(1, len(term)):
                    info=term[i].split(':')
                    if(int(info[0])==0):
                        tfdoc+=1
                        # tfs[doc-1].append(0)
                    else:
                        # print(doc, tfdoc, '\n')
                        tfs[doc-1][ind]=tfdoc
                        doc+=int(info[0])
                        tfdoc=1
                break
    # print(tfs)
    return tfs
        # break
    # for 
    # break


sentence='وزیراطلاعات فواد چوہدری کا کہنا ہے۔'
# TF-IDF algorithm 

# tf_idf(sentence)

# print(l)
# import textract
# text = textract.process("queries.docx", encoding="utf-8")
# print(text)
# for i in text:
#     print(i)








# t=[[0]*3]*3
# t.append([0]*2)
# t[0][1]=10
# t[2][0]=20
# t[1][2]=30
# t.append([0]*2)
# print(t)
# t2=list()
# t2.append([0]*3)
# t2.append([0]*3)
# t2.append([0]*3)
# print(t2)
# t3=t2
# t2[0][0]=5
# print(t3)


# tfs=[list()]*3000
# term_index=open('term_index.txt', "r", encoding="utf-8").readlines()
# for term in term_index:
#     term=term.split('\n')[0].split('\\')
#     # print(term, '\n')
#     doc=0
#     tfdoc=0
#     if(int(term[0])==3):
#         # print(term[0])
#         for i in range(1, len(term)):
#             info=term[i].split(':')
#             # print(info[0])
#             if(int(info[0])==0):
#                 tfdoc+=1
#             else:
#                 print(doc, tfdoc, '\n')
#                 tfs[doc-1]=tfs[doc-1].append(tfdoc)
#                 doc+=int(info[0])
#                 tfdoc=1
#         break

# print(tfs)

# t=init_list_of_objects(2)
# t=[[]]*2
# print(t)
# t[0]=[1, 2, 3]
# t[0][0]=t[0][0]+1
# # t[0].append(5)
# # t[0]=t[0].insert(len(t[0]), 4)
# print(t)
# t[0]=[2, 3, 4]
# t[1]=[1, 2, 3]
# print(t[0])
# print(t[1])
# t=[list()]*2
# t.append(10)
# t.append(20)
# t.append(30)
# t[1]=t[1].append(20)
# )[1, 2, 3]
# print(t)











# l=[list()]*10
# print((l))

def doc_lengths():
    docs=open('inverted_doc_index.txt', "r", encoding="utf-8").readlines()
    lengths=[0]*len(docs)
    for i in range(len(docs)):
        length=len(docs[i].split('\n')[0].split('\\'))
        lengths[i]=length-1
    # print(lengths)
    return lengths
    # print(numpy.average(lengths))

# doc_lengths()

def tf_idf(query):
    q=removeExtras(query)
    q=q.split(' ')
    q=removeStopwords(q)
    q=applyStemming(q)
    # print(q)
    termids=term_ids(q)
    # print(termids)
    D=len(open('docids.txt', "r", encoding="utf-8").readlines())
    # print(D)
    dfs=df(termids)

    IDF=list()
    for f in dfs:
        IDF.append(math.log(D/f,10))
    tfs=tf(termids)
    # print("TFS: ",tfs)
    TFIDF=init_list_of_objects(D, 1)
    for i in range(len(tfs)):
        weight=0
        for j in range(len(IDF)):
            weight+=tfs[i][j]*IDF[j]
        TFIDF[i]=weight
    # index=TFIDF.index(max(TFIDF))
    ranking=open("TFIDF/TF-IDF"+query+'.txt', "a", encoding="utf-8")
    docs=open('docids.txt', "r", encoding="utf-8").readlines()
    # for j in range(len(docs)):
    #     ranking.write(docs[j].split('\n')[0].split('\\')[1]+" "+str(counter)+" "+str(sortedTFIDF[i])+'\n')
    sortedTFIDF=TFIDF[:]
    sortedTFIDF.sort()
    # print(len(TFIDF))
    # print((sortedTFIDF))
    counter=1
    identicalScores=0
    for i in range(len(sortedTFIDF)-1,  -1, -1):
        if sortedTFIDF[i]!=sortedTFIDF[i-1]:
            index=TFIDF.index(sortedTFIDF[i])
            # ranking.write()
            for ind in range(len(TFIDF)):
                if TFIDF[ind]==sortedTFIDF[i]:
                    for j in range(len(docs)):
                        if(ind==int(docs[j].split('\n')[0].split('\\')[0])-1):
                            ranking.write(docs[j].split('\n')[0].split('\\')[1]+" "+str(counter)+" "+str(sortedTFIDF[i])+'\n')
                            counter+=1
                            identicalScores-=1
                            break
                if identicalScores<0:
                    break
            identicalScores=0
        else:
            identicalScores+=1

    index=TFIDF.index(max(TFIDF))
    print('Using TFIDF for: ', query)
    print("Most relevent document ID is: ",open('docids.txt', "r", encoding="utf-8").readlines()[index].split('\n')[0].split('\\')[1])
    print("With TF*IDF score of: ",max(TFIDF))
    return TFIDF

# OKAPI BM25
def BM25(query):
    q=removeExtras(query)
    q=q.split(' ')
    q=removeStopwords(q)
    q=applyStemming(q)
    # print(query)
    termids=term_ids(q)
    # print(termids)
    # D=len(open('docids.txt', "r", encoding="utf-8").readlines())
    # print(D)
    dfs=df(termids)
    tfs=tf(termids)
    len_d=doc_lengths()
    # print(dfs)
    # constants
    avg_len=numpy.average(len_d)
    D=len(len_d)
    k1=1.2
    b=0.75
    k2=100
    # print('length', len(len_d))
    bm25=init_list_of_objects(D, 1)
    for i in range(D):
        weight=0
        K=((1-b)+b*(len_d[i]/avg_len))
        for j in range(len(dfs)):
            weight+=(math.log((D+0.5)/(dfs[j]+0.5)))*(((1+k1)*tfs[i][j])/(K+tfs[i][j]))*(((1+k2)*tfs[i][j])/(k2+tfs[i][j]))
        bm25[i]=weight
    
    ranking=open("BM25/BM25"+query+'.txt', "a", encoding="utf-8")
    docs=open('docids.txt', "r", encoding="utf-8").readlines()
    sortedbm25=bm25[:]
    sortedbm25.sort()
    counter=1

    identicalScores=0
    for i in range(len(sortedbm25)-1,  -1, -1):
        if sortedbm25[i]!=sortedbm25[i-1]:
            index=bm25.index(sortedbm25[i])
            # ranking.write()
            for ind in range(len(bm25)):
                if bm25[ind]==sortedbm25[i]:
                    for j in range(len(docs)):
                        if(index==int(docs[j].split('\n')[0].split('\\')[0])-1):
                            ranking.write(docs[j].split('\n')[0].split('\\')[1]+" "+str(counter)+" "+str(sortedbm25[i])+'\n')
                            counter+=1
                            identicalScores-=1
                            break
                if identicalScores<0:
                    break
            identicalScores=0
        else:
            identicalScores+=1


    # for i in range(len(sortedbm25)-1,  -1, -1):
    #     index=bm25.index(sortedbm25[i])
    #     # ranking.write()
    #     for j in range(len(docs)):
    #         if(index==int(docs[j].split('\n')[0].split('\\')[0])-1):
    #             ranking.write(docs[j].split('\n')[0].split('\\')[1]+" "+str(counter)+" "+str(sortedbm25[i])+'\n')
    #             counter+=1
    #             break
    index=bm25.index(max(bm25))
    print("Using BM25 for: ", query)
    print("Most relevent document ID is: ",open('docids.txt', "r", encoding="utf-8").readlines()[index].split('\n')[0].split('\\')[1])
    print("With BM25 score of: ",max(bm25))

# BM25(sentence)
# Dirichlet smoothin
def dirichlet(query):
    q=removeExtras(query)
    q=q.split(' ')
    q=removeStopwords(q)
    q=applyStemming(q)
    termids=term_ids(q)
    len_d=doc_lengths()#use len on this variable fo docs count
    # query within document
    Q_D=tf(termids)
    # query within whole corpus
    Q_C=[0]*len(termids)
    print(Q_C)
    for i in range(len(len_d)):
        for j in range(len(termids)):
            Q_C[j]+=(Q_D)[i][j]
    print(Q_C)
    
    # average document size in corpus
    mu=numpy.average(len_d)
    # size of corpus
    C=sum(len_d)
    print('C', C)
    dirich=init_list_of_objects(len(len_d), 1)
    for i in range(len(len_d)):
        sol=1
        for j in range(len(termids)):
            P_Q_D=Q_D[i][j]/len_d[i]
            P_Q_C=Q_C[j]/C
            N=len_d[i]
            sol*=((N/(N+mu))*P_Q_D)+((mu/(N+mu))*P_Q_C)
        dirich[i]=sol
        # break
    ranking=open("Dirichlet/Dirichlet"+query+'.txt', "a", encoding="utf-8")
    docs=open('docids.txt', "r", encoding="utf-8").readlines()
    sortedDirichlet=dirich[:]
    sortedDirichlet.sort()
    counter=1
    identicalScores=0
    for i in range(len(sortedDirichlet)-1,  -1, -1):
        if sortedDirichlet[i]!=sortedDirichlet[i-1]:
            index=dirich.index(sortedDirichlet[i])
            # ranking.write()
            for ind in range(len(dirich)):
                if dirich[ind]==sortedDirichlet[i]:
                    for j in range(len(docs)):
                        if(ind==int(docs[j].split('\n')[0].split('\\')[0])-1):
                            ranking.write(docs[j].split('\n')[0].split('\\')[1]+" "+str(counter)+" "+str(sortedDirichlet[i])+'\n')
                            counter+=1
                            identicalScores-=1
                            break
                if identicalScores<0:
                    break
            identicalScores=0
        else:
           identicalScores+=1

    # for i in range(len(sortedDirichlet)-1,  -1, -1):
    #     index=dirich.index(sortedDirichlet[i])
    #     # ranking.write()
    #     for j in range(len(docs)):
    #         if(index==int(docs[j].split('\n')[0].split('\\')[0])-1):
    #             ranking.write(docs[j].split('\n')[0].split('\\')[1]+" "+str(counter)+" "+str(sortedDirichlet[i])+'\n')
    #             counter+=1
    #             break
    index=dirich.index(max(dirich))
    print("Using Dirichlet for: ", query)
    print("Most relevent document ID is: ",open('docids.txt', "r", encoding="utf-8").readlines()[index].split('\n')[0].split('\\')[1])
    print("With Dirichlet score of: ",max(dirich))

# dirichlet(sentence)



queries=[
    'وکلاء کی ہڑتال اور ریلیاں',
    'احتساب عدالت کے مقدمات',
    'انسانوں کی اسمگلنگ اور انسداد انسانی سمگلنگ کے اقدامات',
    'انسداد تمباکو نوشی کے اقدامات اور آگاہی',
    'بچوں کے خلاف تشدد اور اغوا',
    'خفیہ ایجنسیاں اور جاسوس',
    'عورتوں پر ظلم و تشدد , قتل اور اغوا',
    'مجرم کو پھانسی دے دی گئی',
    'مزدور طبقے کی خوشحالی کے اقدامات',
    'احتجاجی دھرنے, جلوس اور ریلیاں',
]

def scoring():
    if(sys.argv[2]=='TF-IDF'):
        for q in queries:
            tf_idf(q)
            # break
    if(sys.argv[2]=='Okapi-BM25'):
        for q in queries:
            BM25(q)
            # break
    if(sys.argv[2]=='Dirichlet'):
        for q in queries:
            dirichlet(q)
            # break


def evaluation():
    sheets=1
    
    for query in range(10):
        print("Presision for Query", sheets)
        dataframe1 = pd.read_excel('qrels.xlsx', "Q"+str(sheets)+" Docs")
        # sheets+=1
        docIds=dataframe1["Doc Id"]
        totalDocs=len(docIds)
        docRelevancy=dataframe1["Doc Relevancy"]
        irrelevantDocs=dataframe1["Irrelevant Doc"][0]+dataframe1["Marginally relevant Doc"][0]
        relevantDocs=dataframe1["Fairly relevant Doc"][0]+dataframe1["Highly relevant Doc"][0]
        score=open("TFIDF/Q"+str(sheets)+".txt", 'r', encoding="utf-8").readlines()
        MAP=0
        R=0
        P5=0
        P10=0
        P20=0
        P30=0
        for i in range(totalDocs):
            index=-1
            for j in range(totalDocs):
                if docIds[j]==int(score[i].split(' ')[0].split('.')[0]):
                    index=j
                    if docRelevancy[index]==4 or docRelevancy[index]==3:
                        R+=1
                        MAP+=(R/(i+1))
            if i==4:
                P5=R/5
            elif i==9:
                P10=R/10
            elif i==19:
                P20=R/20
            elif i==29:
                P30=R/30
        MAP/=relevantDocs
        print("P@5 of TFIDF: ", P5)
        print("P@10 of TFIDF: ", P10)
        print("P@20 of TFIDF: ", P20)
        print("P@30 of TFIDF: ", P30)
        print("MAP of TFIDF: ",MAP)
        score=open("BM25/Q"+str(sheets)+".txt", 'r', encoding="utf-8").readlines()
        MAP=0
        R=0
        P5=0
        P10=0
        P20=0
        P30=0
        for i in range(totalDocs):
            index=-1
            for j in range(totalDocs):
                if docIds[j]==int(score[i].split(' ')[0].split('.')[0]):
                    index=j
                    if docRelevancy[index]==4 or docRelevancy[index]==3:
                        R+=1
                        MAP+=(R/(i+1))
            if i==4:
                P5=R/5
            elif i==9:
                P10=R/10
            elif i==19:
                P20=R/20
            elif i==29:
                P30=R/30
        MAP/=relevantDocs
        print("P@5 of BM25: ", P5)
        print("P@10 of BM25: ", P10)
        print("P@20 of BM25: ", P20)
        print("P@30 of BM25: ", P30)
        print("MAP of BM25: ",MAP)
        score=open("Dirichlet/Q"+str(sheets)+".txt", 'r', encoding="utf-8").readlines()
        MAP=0
        R=0
        P5=0
        P10=0
        P20=0
        P30=0
        for i in range(totalDocs):
            index=-1
            for j in range(totalDocs):
                if docIds[j]==int(score[i].split(' ')[0].split('.')[0]):
                    index=j
                    if docRelevancy[index]==4 or docRelevancy[index]==3:
                        R+=1
                        MAP+=(R/(i+1))
            if i==4:
                P5=R/5
            elif i==9:
                P10=R/10
            elif i==19:
                P20=R/20
            elif i==29:
                P30=R/30
        MAP/=relevantDocs
        print("P@5 of Dirichlet: ", P5)
        print("P@10 of Dirichlet: ", P10)
        print("P@20 of Dirichlet: ", P20)
        print("P@30 of Dirichlet: ", P30)
        print("MAP of Dirichlet: ",MAP)
        sheets+=1
    return

evaluation()