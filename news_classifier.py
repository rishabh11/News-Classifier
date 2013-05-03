#!/usr/bin/python

import nltk,os,sys,re,csv
from os import listdir
from os.path import join
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer

class news_classifier():
    
    features=[]
    list=[]

    def tokenize(self,text):
        terms = re.findall(r'\w+', text) 
        terms = [term for term in terms if not term.isdigit()] 
        return terms
    
    def frequency(self,text):
        sent=self.tokenize(text)
        ans={}
        for i in sent:
            if i not in stopwords.words():
                las=LancasterStemmer()
                temp=las.stem(i)
                if temp not in ans:
                    ans[temp]=1
                else:
                    ans[temp]+=1
        sorted(ans, key=ans.get, reverse=True)
        ans2={}
        for i in ans.keys()[0:10]:
            ans2[i]=ans[i]
        return ans2
    
    def rating(self,text):
        dic=self.frequency(text)
        for i in dic.keys():
            if dic[i]>10:
                dic[i]="High"
            elif dic[i]<=10 and dic[i]>5:
                dic[i]="Med"
            else:
                dic[i]="Low"
        return dic
    
    def write(self):
        f = open("data.csv", "wb")
        csv_file = csv.writer(f, delimiter=",")
        row=list(self.features)
        row.insert(0," ")
        row.append(" ")
        csv_file.writerow(row)
        for i in self.list:
            row=[i[0]]
            count=0
            for j in self.features:
                if j in i[1].keys():
                    row.append(i[1][j])
                else:
                    row.append(0)
                count+=1
            row.append(i[2])
            csv_file.writerow(row)
        f.close()
        
    def main(self):
        dataset_path=os.path.dirname(os.path.realpath(__file__))
        for dirname in os.listdir(dataset_path):
            label = dirname
            classpath = join(dataset_path, dirname)
            for dirpath, dirnames, filenames in os.walk(classpath):
                for filename in filenames:
                    filepath = join(dirpath, filename)
                    f=open(filepath,"r")
                    freq=self.frequency(f.read())
                    for i in freq.keys():
                        if i not in self.features:
                            self.features.append(i)
                    self.list.append((filepath,freq,label))
                    f.close()
        self.write()

    def main2(self):
        f=open(sys.argv[2])
        total_words=len(self.features)
        num_words={}
        #print total_words
        for i in self.list:
            temp=0
            for j in i[1]:
                temp+=i[1][j]
            if i[2] not in num_words:
                num_words[i[2]]=temp
            else:
                num_words[i[2]]+=temp
        #print num_words
        words=self.frequency(f.read())
        f.close()
        prob={}
        for i in num_words.keys():
            prob[i]=1.0
        for i in words.keys():
            for k in num_words.keys():
                count=0
                for j in self.list:
                    if j[2]==k and i in j[1].keys():
                        count+=j[1][i]
                post=(count+1.0)/(total_words+num_words[k])
                #print i,k,post,count
                prob[k]*=(post**words[i])
        print prob
        max=-1.0
        classified=""
        #sorted(prob, key=prob.get, reverse=True)
        for i in prob:
            if prob[i]>max:
                max=prob[i]
                classified=i
        print classified

if __name__=='__main__':                       
    k=news_classifier()
    if(sys.argv[1]=="1"):
        k.main()
        k.main2()
    else:
        if(sys.argv[1]=="2"):
            k.main2()