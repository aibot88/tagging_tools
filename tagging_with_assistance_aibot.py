import pickle
import numpy as np
import sys
import os
import tkinter as tk
import json
import pandas as pd


class Dataset:
    """
    Store the information of a dataset.
    """
    def __init__(self, data, s_label, label, pkg_names, time, source, family):
        #label:0/1 (0->mal 1->nor)
        self.SegmentsList = data #class 'numpy.ndarray' API Sequence
        self.SegmentsLabels = s_label #class 'numpy.ndarray' API Sequence Labels
        self.apkLabel = label #class 'numpy.float64' APP Label 
        self.pkgNames = pkg_names #class 'str' APP unique id
        self.pkgTime = time #class 'str' APP time xxxx(year)
        self.pkgSources = source #class 'str' APP source
        self.family = family #class 'str' APP family. Valid only when apkLabel == 0 


action_level = {0: -1, 1: 0, 2: 2, 3: 0, 4: 0, 5: 3, 6: 0, 7: 3, 8: 3, 9: 0, 10: 0, 11: 0, 12: 2, 13: 0, 14: 3, 15: 0, 16: 3, 17: 0, 18: 0, 19: 1, 20: 0, 21: 3, 22: 0, 23: 0, 24: 0, 25: 0, 26: 0, 27: 0, 28: 0, 29: 0, 30: 2, 31: 0, 32: 2, 33: 2, 34: 1, 35: 3, 36: 0, 37: 0, 38: 0, 39: 0, 40: 0, 41: 0, 42: 0, 43: 0, 44: 1, 45: 2, 46: 2, 47: 3, 48: 3, 49: 3, 50: 0, 51: 2, 52: 1, 53: 1, 54: 0, 55: 0, 56: 0, 57: 0, 58: 0, 59: 0, 60: 0, 61: 0, 62: 0, 63: 0, 64: 0, 65: 2, 66: 1, 67: 3, 68: 0, 69: 0, 70: 0, 71: 0, 72: 3, 73: 0, 74: 0, 75: 3, 76: 0, 77: 3, 78: 0, 79: 0, 80: 0, 81: 1, 82: 0, 83: 2, 84: 2, 85: 0, 86: 2, 87: 2, 88: 0, 89: 3, 90: 2, 91: 3, 92: 3, 93: 3, 94: 0, 95: 0, 96: 3, 97: 0, 98: 0, 99: 0, 100: 1, 101: 0, 102: 0, 103: 0, 104: 0, 105: 0, 106: 2, 107: 2, 108: 1, 109: 1, 110: 2, 111: 3, 112: 0, 113: 3, 114: 3, 115: 3, 116: 3, 117: 3, 118: 0, 119: 1, 120: 0, 121: 0, 122: 0, 123: 0, 124: 0, 125: 3, 126: 3, 127: 3, 128: 3, 129: 3, 130: 0, 131: 3, 132: 3, 133: 3, 134: 3, 135: 3, 136: 0, 137: 0, 138: 3, 139: 3, 140: 3, 141: 3, 142: 3, 143: 0, 144: 2, 145: 0, 146: 0, 147: 0, 148: 0, 149: 2, 150: 2, 151: 0, 152: 3, 153: 3, 154: 1, 155: 0, 156: 2, 157: 1, 158: -1, 159: 2, 160: 0, 161: 2, 162: 0, 163: 2, 164: 1, 165: 0, 166: 0, 167: 2, 168: 2, 169: -1}
action_level_category=['normal','less_sensitive','sensitive','more_sensitive']
#标注index
index2load = open("./index", 'r')
id = int(index2load.read())
print('index: '+str(id))

index2load.close()
#compactid与action的dict dict[compactid]=action

compactid2ac_dict_file = open('./compactid2action.json','r')

compactid2ac_dict=json.load(compactid2ac_dict_file)

compactid2ac_dict_file.close()

#待标注数据

file2load = open('APISeqDB.pk','rb')
datasets = pickle.load(file2load)


data_dict = {
    'SegmentsList': [dataset.SegmentsList for dataset in datasets],
    'SegmentsLabels': [dataset.SegmentsLabels for dataset in datasets],
    'apkLabel': [dataset.apkLabel for dataset in datasets],
    'pkgNames': [dataset.pkgNames for dataset in datasets],
    'pkgTime': [dataset.pkgTime for dataset in datasets],
    'pkgSources': [dataset.pkgSources for dataset in datasets],
    'family': [dataset.family for dataset in datasets]
}
df = pd.DataFrame(data_dict)
cnt = 0
# l_data,l_label = pickle.load(file2load)
app_data, app_label, app_pkg = df['SegmentsList'].to_list(), df['SegmentsLabels'].to_list(), df['pkgNames']

l_data, l_label, l_pkg = [],[],[]
for index, seqs in enumerate(app_data):
    pkg_name = app_pkg[index]
    labels = app_label[index]
    for j, seq in enumerate(seqs):
        l_data.append(seq)
        l_label.append(labels[j])
        l_pkg.append(pkg_name)



# l_data= pickle.load(file2load)
# l_label = [-1]*len(l_data)

print('data_len: {0}; label_len: {1}'.format(len(l_data),len(l_label)))

sum1=0
sum2=0
sum3=0
#for i in range(len(l_label)):
#    if l_label[i]==1:
#        sum1+=1
#    elif l_label[i]==0:
#        sum2+=1
#    else:
#        sum3+=1
print('normal_num: {0}; mal_num: {1}; other_num: {2}'.format(sum1,sum2,sum3))

file2load.close()

def next_():
    action_list.delete(1.0,'end')
    global id
    if id<len(l_data)-1:
        id+=1
    sen_cnt=0
    less_sen_cnt=0
    more_sen_cnt=0
    more_sen_dict={}
    sen_dict={}
    less_sen_dict={}
    for i in l_data[id]:
        if action_level[i] in [0,1,2,3]:
            action_list.insert("end",compactid2ac_dict[str(i)]+'\n',action_level_category[action_level[i]])
        else:
            action_list.insert("end",compactid2ac_dict[str(i)]+'\n')
        
        if action_level[i] == 1:
            less_sen_cnt+=1
            less_sen_dict[i]=1
        if action_level[i] == 2:
            sen_cnt+=1
            sen_dict[i]=1
        if action_level[i] == 3:
            more_sen_cnt+=1
            more_sen_dict[i]=1        
    less_sensitive.set('次敏感: {0}个，{1}次'.format(len(less_sen_dict),less_sen_cnt))
    sensitive.set('  敏感: {0}个，{1}次'.format(len(sen_dict),sen_cnt)) 
    more_sensitive.set('  高危: {0}个，{1}次'.format(len(more_sen_dict),more_sen_cnt))     

    #if l_label[id]==1:
    #    st.set("Label:正常")
    #    #next_()
    #elif l_label[id]==0:
    #    st.set("Label:恶意")
    #    #next_()
    #else:
    st.set(str(l_label[id]))

def back_():
    action_list.delete(1.0,'end')
    global id
    if id>0:
        id-=1
    sen_cnt=0
    less_sen_cnt=0
    more_sen_cnt=0
    more_sen_dict={}
    sen_dict={}
    less_sen_dict={}
    for i in l_data[id]:
        if action_level[i] in [0,1,2,3]:
            action_list.insert("end",compactid2ac_dict[str(i)]+'\n',action_level_category[action_level[i]])
        else:
            action_list.insert("end",compactid2ac_dict[str(i)]+'\n')

        if action_level[i] == 1:
            less_sen_cnt+=1
            less_sen_dict[i]=1
        if action_level[i] == 2:
            sen_cnt+=1
            sen_dict[i]=1
        if action_level[i] == 3:
            more_sen_cnt+=1
            more_sen_dict[i]=1 
    less_sensitive.set('次敏感: {0}个，{1}次'.format(len(less_sen_dict),less_sen_cnt))
    sensitive.set('  敏感: {0}个，{1}次'.format(len(sen_dict),sen_cnt))
    more_sensitive.set('  高危: {0}个，{1}次'.format(len(more_sen_dict),more_sen_cnt))   
    #if l_label[id]==1:
    #    st.set("Label:正常")
    #elif l_label[id]==0:
    #    st.set("Label:恶意")
    #else:
    st.set(str(l_label[id]))

def is_one():
    global l_data,l_label,cnt
    cnt+=1
    l_label[id]=1
    next_()

def is_two():
    global l_data,l_label,cnt
    cnt+=1
    l_label[id]=2
    next_()

def is_thr():
    global l_data,l_label,cnt
    cnt+=1
    l_label[id]=3
    next_()

def is_fou():
    global l_data,l_label,cnt
    cnt+=1
    l_label[id]=4
    next_()

def is_fiv():
    global l_data,l_label,cnt
    cnt+=1
    l_label[id]=5
    next_()

def is_six():
    global l_data,l_label,cnt
    cnt+=1
    l_label[id]=6
    next_()


def save():
    global l_data,l_label,id,l_pkg
    file2load = open('./muti_label_data.pk','wb')
    data_dict = {
    'SegmentsList': l_data,
    'SegmentsLabels': l_label,
    'apkLabel': None,
    'pkgNames': l_pkg,
    'pkgTime': None,
    'pkgSources': None,
    'family': None
    }
    temp_df = pd.DataFrame(data_dict)
    # l_label=np.array(l_label)
    # all_data=[l_data,l_label]
    pickle.dump(temp_df,file2load)
    file2load.close()
    index2load = open("./index", 'w')
    index2load.write(str(id))
    index2load.close()

def p_out():
    print(get_act_seg(l_data[id]))
    print(id,cnt)

root = tk.Tk() 
width = 550
height = 800 
root.geometry(f'{width}x{height}')
# action_list = tk.Listbox(root,width=40,height=30)
action_list = tk.Text(root,width=40,height=30)
action_list.tag_config('normal',background='lightgreen')
action_list.tag_config('less_sensitive',background='yellow')
action_list.tag_config('sensitive',background='orange')
action_list.tag_config('more_sensitive',background='red')
less_sensitive=tk.StringVar()
less_sensitive.set('次敏感: {0}个，{1}次'.format('test','test'))
sensitive=tk.StringVar()
sensitive.set('  敏感: {0}个，{1}次'.format('test','test'))
more_sensitive=tk.StringVar()
more_sensitive.set('  高危: {0}个，{1}次'.format('test','test'))
st = tk.StringVar()
st.set("Label:待定")
lb = tk.Label(root,textvariable=st)
lb2 = tk.Label(root,textvariable=less_sensitive)
lb3 = tk.Label(root,textvariable=sensitive)
lb4 = tk.Label(root,textvariable=more_sensitive)
one = tk.Button(root,width=10,text="sms",command=is_one)
two = tk.Button(root,width=10,text="info",command=is_two)
thr = tk.Button(root,width=10,text="rog",command=is_thr)
fou = tk.Button(root,width=10,text="re",command=is_fou)
fiv = tk.Button(root,width=10,text="phone",command=is_fiv)
six = tk.Button(root,width=10,text="sys",command=is_six)
next = tk.Button(root,width=10,text="next",command=next_)
back = tk.Button(root,width=10,text="back",command=back_)
ss = tk.Button(root,width=10,text="保存",command=save)
pp = tk.Button(root,width=10,text="输出",command=p_out)
sen_cnt=0
less_sen_cnt=0
more_sen_cnt=0
more_sen_dict={}
sen_dict={}
less_sen_dict={}
for i in l_data[id]:
    if i!=0:
        if action_level[i] in [0,1,2,3]:
            action_list.insert("end",compactid2ac_dict[str(i)]+'\n',action_level_category[action_level[i]])
        else:
            action_list.insert("end",compactid2ac_dict[str(i)]+'\n')

        if action_level[i] == 1:
            less_sen_cnt+=1
            less_sen_dict[i]=1
        if action_level[i] == 2:
            sen_cnt+=1
            sen_dict[i]=1
        if action_level[i] == 3:
            more_sen_cnt+=1
            more_sen_dict[i]=1 
less_sensitive.set('次敏感: {0}个，{1}次'.format(len(less_sen_dict),less_sen_cnt))
sensitive.set('  敏感: {0}个，{1}次'.format(len(sen_dict),sen_cnt))
more_sensitive.set('  高危: {0}个，{1}次'.format(len(more_sen_dict),more_sen_cnt))   
#if l_label[id]==1:
    #st.set("Label:正常")
#elif l_label[id]==0:
st.set(str(l_label[id]))


def get_act_seg(seg):
    seg=seg.tolist()
    print(seg)
    result = ""
    for i in range(len(seg)):
        if(seg[i]!=0):
            result+='\n'+compactid2ac_dict[str(seg[i])]
    return result
'''
while(1):
    print(get_act_seg(l_data[index]))
    n = input()
    if n=='1':
        if(index>=len(l_label)):
            l_label.append(0)
        else:
            l_label[index]=0
        index+=1
    elif n=='2':
        if(index>=len(l_label)):
            l_label.append(1)
        else:
            l_label[index]=1
        index+=1
    else:
        file2load = open('./0.01.pk','wb')
        l_label=np.array(l_label)
        all_data=[l_data,l_label]
        pickle.dump(all_data,file2load)
        file2load.close()
        index2load = open("./index", 'w')
        index2load.write(str(index))
        index2load.close()
        break
'''


action_list.pack(side=tk.LEFT,fill=tk.Y)
lb2.place(x=350,y=100)
lb3.place(x=350,y=120)
lb4.place(x=350,y=140)
lb.place(x=400,y=200)
one.place(x=400,y=250)
two.place(x=400,y=300)
thr.place(x=400,y=350)
fou.place(x=400,y=400)
fiv.place(x=400,y=450)
six.place(x=400,y=500)
next.place(x=400,y=550)
back.place(x=400,y=600)
ss.place(x=400,y=700)
pp.place(x=400,y=650)
root.mainloop()