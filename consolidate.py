import pprint
import json

i = 1
celebs=[]
while(i<10):
    
    # Files where the AWS face recog results are stored are run and consolidted to make a json file.
    file1 = open(r"C:\Users\chand\chandra\movsse\facrecog\salt_results\celebs_"+str(i)+".txt",'r')

    part = []

    ans = file1.readlines()
    l = len(ans)
    # print(l)

    j = 0

    while(j<l):

        x = ans[j+1].split(",")
        if(len(x)>1):
            y = x[1].split("'")
            part.append(str(ans[j].strip())+"  " +str(y[1]))
        else:
            y = x[0].split("'")
            part.append(str(ans[j].strip())+"  " +str(y[1]))

        j = j+2

    celebs.append(part)
    i = i+1


# A dictionary is used to mark the start and end of a scene and celebrities stored in it.
dict = {0: {"start" : '', "end" : '' , "Celebrities" : []}}

def dictMaker(start, cel, end,i):                      #makes a dictionary
    dict[i] = {}
    dict[i]["start"] = start
    dict[i]["end"] = end
    dict[i]["Celebrities"] = cel

i = 1
times = ['00:00:00', '00:10:08', '00:20:02', '00:32:13', '00:42:04', '00:54:31', '01:06:46', '01:17:20' , '01:29:23' , '01:37:05' ]

while(i<10):

    stime = times[i-1].split(":")
    start_seconds = (int(stime[0])*60*60)+(int(stime[1])*60)+(int(stime[2]))

    etime = times[i].split(":")
    end_seconds = (int(etime[0])*60*60)+(int(etime[1])*60)+(int(etime[2]))
    dictMaker(start_seconds,celebs[i-1],end_seconds,i)
    
    i = i+1

del dict[0]
# pprint.pprint(dict)
pprint.PrettyPrinter(sort_dicts=False).pprint(dict)
    
json_object = json.dumps(dict) 
# print(json_object)

with open("faces.json", "w") as outfile:
    outfile.write(json_object)


file1.close()