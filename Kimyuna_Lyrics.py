import requests
from bs4 import BeautifulSoup
from konlpy.tag import Kkma
kkma=Kkma()

#Jaurim
#   Album   Title   Nouns
#   <str>   <str>   <str list>
Jaurim=[]
Naver_Index=[[20771, 9], #1
             [24115, 8], #2
             [24124, 2],
             [2189629, 11], #3
             [2185078, 1],
             [15405515, 1], #4
             [15405526, 8],
             [16087287, 1] #연
             ]


def AlbumCrawling(first_page, num):
    page=0
    for i in range(num):
        url='https://music.naver.com/lyric/index.nhn?trackId={}'.format(first_page+i)
        source_code=requests.get(url)
        text=source_code.text

        Jaurim_temp=[]

        # 0열 Album
        a1=text.find("""class="album">""")
        a2=text.find("<", a1)
        Jaurim_temp.append(text[(a1+14):a2])

        # 1열 Title
        b1=text.find('''se;" title="''')
        b2=text.find('"', b1+12)
        Jaurim_temp.append(text[(b1+12):b2])
        
        # 2열 Nouns
        c1=text.find("show_lyrics")
        c2=text.find("</div>", c1)
        Jaurim_temp.append(kkma.nouns(text[(c1+13):c2]))

        Jaurim.append(Jaurim_temp.copy())

def Find_Songs(word):
    for i in range(len(Jaurim)):
        for j in Jaurim[i][2]:
            if(j==word):
                print(Jaurim[i][1])
            if(Jaurim[i][1]=="garbage"):
                continue
        

#웹 크롤링
for i in range(len(Naver_Index)):
    AlbumCrawling(Naver_Index[i][0], Naver_Index[i][1])
    print("Crawling {} of {} Done..".format((i+1), len(Naver_Index)))

print("----------------------------------------------")

#가비지 값 제거
garbage=["네이버", "청소년보호법"]
for i in range(len(Jaurim)):
    for j in Jaurim[i][2]:
        if(j in garbage):
            Jaurim[i][1]="garbage"

#단어 갯수 카운트
Word_Dict={}
for i in range(len(Jaurim)):
    for j in Jaurim[i][2]:
        if(Jaurim[i][1]=="garbage"):
            continue
        try:
            Word_Dict[j]+=1
        except KeyError:
            Word_Dict[j]=1

print("----------------------------------------------")

#출력
for i in Word_Dict:
    if(Word_Dict[i]>5):
        print(i, "-", Word_Dict[i])
