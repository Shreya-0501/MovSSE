import string
import re
import pprint
import stanza
from collections import Counter
import json


file = open("bttf.txt", encoding="utf-8")                                   #script file
fileSub = open("bttfSc.txt", encoding="utf-8")                               #subtitle file


Content = file.read()                                           #full script file
contentSub = fileSub.read()                                     #full subtitle file

Scriptpart = Content.split("CUT TO:")                              #stores cut to - cut to
listSub = contentSub.split("\n\n")                              #splits the subtitle file paragraph to  paragraph (dialogue no., timestamp, dialogue)


listSubLower = []                                               #has the content in lowercase
ScriptpartLow = []

for i in listSub:                                               #converting everything in listSub to lowercase and appending it to a new list
    x = i.lower()
    listSubLower.append(x)

for i in Scriptpart:                                               #converting everything in CoList2 to lowercase and appending it to a new list
    x = i.lower()
    ScriptpartLow.append(x)


Scriptedit1 = []

for i in ScriptpartLow:                                            #making short forms of have to full forms
    x = i.replace("'ve", " have")
    x = x.replace("...", " ")
    x = x.replace("--", " ")
    x = x.replace("\n\n"," ")
    x = x.replace("\n"," ")

    Scriptedit1.append(x)


Subedit1 = []

for i in listSubLower:                                          #making short forms of have to full forms
    x = i.replace("'ve", " have")
    Subedit1.append(x)

punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''                       #punctuation

Scriptedit2 = []                                                    #has lowercase content without '\n' chars


for i in Scriptedit1:                                           #removing all the '\n' chars and appending it to a new list
    
    x = i

    for ele in punc:
        x = x.replace(ele, "")

    Scriptedit2.append(x)

#print(Scriptedit2)

dict = {0: {"dialogueNo" : "0", "scene" : 0, "timeStamp" : "00:00:00", "dialogue" : " ", "change" : False}}

def dictMaker(s, idx, subDialogue):                      #makes a dictionary
    dict[subDialogue[0]] = {}
    dict[subDialogue[0]]["dialogueNo"] = subDialogue[0]
    dict[subDialogue[0]]["scene"] = idx
    dict[subDialogue[0]]["timestamp"] = subDialogue[1]

    str1 = ""                                           #empty string
    # traverse in the string
    for ele in subDialogue[s]:                          #converting a list to a string
        str1 += ele

    dict[subDialogue[0]]["dialogue"] = str1             #stores dialogue(string)
    dict[subDialogue[0]]["change"] = False              #stores where the cut-to num changes


before = 0
flag = 0
notfoundc = 0                                       #stores the number of dialogues that aren't found
foundc = 0                                         #stores the number of dialogues found in script file from the subtitle file

for j in Subedit1:                            #has paragraphs of subtitles   --> we are splitting every paragraph into:
    subDialogue = j.split("\n")                   #{"1486", "02:49:52,390 --> 02:49:55,225'", "I'm not gonna be coming back,to this place."}

    if len(subDialogue) < 2:                      # then dialogue doesn't exist
        continue                                  #then continue
    x = subDialogue[2]                            #else first dialogue starts from 2

    flag = 0                                            #indicates whether dialogue is found or not

    for ele in x:                                       #removing punc in dialogues(index -1)
        if ele in punc:
            x = x.replace(ele, "")

    for idx, i in enumerate(Scriptedit2):                            #idx is iterator(scene number), i has cuto no in cut to - cut to (in paragraphs)
        if ((idx<=before+2) and (idx>before-1)):                 #to ensure the dialogue is in the present index or in the ones after this
            if(i.find(x) != -1):                                 #if we find the dialogue
                #print(subDialogue[0],x , idx)                   #print the dialogue no., dialogue and the cut-to index
                s = slice(2, len(subDialogue))                   #contains full dialogue
                dictMaker(s, idx, subDialogue)                   #passing sliced dialogue, scene index, and subDialogue list
                flag = 1
                foundc +=1
                #print(foundc)                                    #prints the number of dialogues found
                before = idx
                break

            else:
                if (flag == 0) :
                    fcount = 0                                         #found count
                    sentence = x.split(" ")                            #dialogue -> word by word  , x-->dialogue
                    totcount = len(sentence)                           #size of the dialogue
                    for word in sentence:                              #for every word in dialogue
                        if (Scriptedit2[before].find(word) != -1):         #searching word in Scriptedit2()
                            fcount += 1

                    percentage = fcount/totcount

                    if(percentage >= 0.65):
                        #print(subDialogue[0], x , before)
                        s = slice(2, len(subDialogue))                          #slices the dialogue from the subDialogue list
                        dictMaker(s, idx, subDialogue)
                        foundc += 1
                        flag = 1
                        before = idx
                        break
                    else:
                        # print(subDialogue[0],x , before,percentage)
                        s = slice(2, len(subDialogue))                          #slices the dialogue from the subDialogue list
                        dictMaker(s, before, subDialogue)

        
    if flag == 0:                                               #not found dialogues
        notfoundc += 1
        #print(subDialogue[0],x , idx)
        #print(notfoundc)                                         #prints the number of dialogues not found

cutonum = 0

for dictNum, info in dict.items():                              #dictNum -> high level key  #initial index number of dictionary -->initial high level key
    for key in info:                                            #info -> the inner dict's key  (dialogueNo, change)
        if cutonum != info["scene"]:                           #if the number changes
            dict[dictNum]["change"] = True                      #True --> when scene num changes
    cutonum = info["scene"]                                    #initially initialised to the scene num

print("Number of dialogues found :-", foundc)
print("Number of dialogues not found :-", notfoundc)


#pprint.pprint(dict, sort_dicts = False)

# for id,data in dict.items():

#     #print(dict[x]['change'])

#     for key in data:
#         if(key=="change"):
#             if(data[key] == True):
#                 print(id ,data["scene"], data[key])


# for id, data in dict.items():
#     for key in data:
#         if(key == "timestamp"):
#             #print(data[key])
#             times = data[key].split("-->")
#             print(times[0])


final = {0: {"dialogueNo" : "0", "scene" : 0, "start" : "00:00:00" , "end" : "00:00:00", "dialogue" : " "}}

for id, data in dict.items():
    if id ==0 or id == 1:
        continue
    final[id] ={}
    for key in data:

        if(key == "timestamp"):
            times = data[key].split(" --> ")
            
            final[id]["start"] = times[0]
            final[id]["end"] = times[1]
        elif(key == "change"):
            continue
        else:
            final[id][key] = data[key]

pprint.pprint(final, sort_dicts = False)


script = {0: {"scene no" : 0, "data" :" " , "GPE" :[] ,"PERSON":[],"WOA":[],"ORG":[],"TIME":[],"MONEY":[]}}



nlp = stanza.Pipeline('en')                    #for stanza


for idx, para in enumerate(Scriptedit1):
    doc = nlp(para)

    script[idx]={}
    script[idx]["scene no"] = idx
    script[idx]["data"] = para

    geo = []
    persons = []
    workoa = []
    org = []
    time = []
    money = []

    for ent in doc.ents:
        
        #print(ent.type, ent.text)

        if ent.type == "GPE":
            #print(ent.text)
            if ent.text not in geo:
                geo.append(ent.text)
                #print(ent.text)
        elif ent.type == "PERSON":
            #print(ent.text)
            if ent.text not in persons:
                persons.append(ent.text)
                #print(ent.text)
        elif ent.type == "WORK OF ART":
            #print(ent.text)
            if ent.text not in workoa:
                workoa.append(ent.text)
                #print(ent.text)
        elif ent.type == "ORG":
            #print(ent.text)
            if ent.text not in org:
                org.append(ent.text)
                #print(ent.text)
        elif ent.type == "TIME":
            #print(ent.text)
            if ent.text not in time:
                time.append(ent.text)
                #print(ent.text)
        elif ent.type == "MONEY":
            #print(ent.text)
            if ent.text not in money:
                money.append(ent.text)
                #print(ent.text)
        
    script[idx]["GPE"]= geo
    script[idx]["PERSON"] = persons
    script[idx]["WOA"] = workoa
    script[idx]["ORG"]= org
    script[idx]["TIME"] = time
    script[idx]["MONEY"] = money
    #print(geo,persons,workoa,org,time,money)


pprint.pprint(script, sort_dicts = False)

with open("bfftdailogues.json", "w") as outfile:
    json.dump(final, outfile)

with open("bfftscene.json","w") as outfile:
    json.dump(script,outfile)




