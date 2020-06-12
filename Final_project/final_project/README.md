# SSAFY 최종 프로젝트

## Trello를 이용한 일정관리

Url : `https://trello.com/b/VvNEXFFk/ssafy-최종-프로젝트`



## git을 이용한 공동 작업공간

> git branch 사용
>
> 한광욱 : brchA
> 이예림 : brchB



### branch 명령어

```bash
#브랜치 생성
$git branch { 브랜치명 }

#브랜치 이동
$git checkout {브랜치명}

#브랜치 확인
$git branch

[참고사이트]
https://victorydntmd.tistory.com/91
```



### git 하루 루틴

> ##### 아침
>
> 각자 브랜치에서 전 날 올린 master file pull하기

```bash
$git checkout brchB
$git pull origin master
```

> ##### 틈틈이
>
> 각자 브랜치에서 작업 후 

```bash
$git add.
$git commit -m '메세지'
$git push origin brchB
```

> ##### 자기 전
>
> master로 이동 후 각자 브랜치에서 작업한 것 pull, push하기

```bash
$git checkout master
$git pull origin brchB
$git push origin master

#pull했을 때 충돌오류 발생 => 충돌 해결 후 push
```



## 파일 구조

```

```



## 명세서

### 1단계 : 필수구현

* JSON파일 받아오기
* The Movie Data Base 의 api 사용
* index.html
  * JSON image받아오기



## 가상환경 생성

```
1. .gitignore 파일생성 // project 바깥쪽에

2. gitignore.io 사이트

   > venv, django, python

3. python -m venv venv

4. source venv/Scripts/activate

5. pip list로 확인

6. pip freeze => 필요한 다운로드 파일 확인

7. pip freeze > requirements.txt  //다운 받을 파일들 requirements.txt에 저장

8. pip install -r requirements.txt // requirements.txt에 저장된 파일들 다운받기

9. deactivate //가상환경 종료 
```





## API를 통해 받은 데이터 파일 생성

1. The Movie Data Base 에 가입하여 API_KEY 생성
2. 원하는 데이터를 담은 JSON 파일을 생성할 Python Code 작성
3. 파이썬 코드 실행하면 JSON파일 생성됨

```python
# 영화 장르 추출
import requests

import json
# import pandas as pd
# from io import StringIO


# API 지정

apikey = "91f3048e6d4f7b2729a87dcfbbef1b04"



# 정보를 알고 싶은 영화 리스트 만들기

movie_list = range(1, 1000)



# API 지정

api = "https://api.themoviedb.org/3/movie/{movies}?api_key={key}"



# string.format_map() 매핑용 클래스 만들기

class Default(dict):

    def __missing__(self, key):

        return key



# 각 영화의 정보 추출하기
data = {}
genres = []
x = 0
vis = [0]*99999999
for name in movie_list:
    # API의 URL 구성하기

    url = api.format_map(Default(movies=name, key=apikey))

        # print(url)  # 데이터 확인

    # API에 요청을 보내 데이터 추출하기

    r = requests.get(url)  # json 형태의 데이터가 나온다.

        # print(type(r))  # <class 'requests.models.Response'>

    # 결과를 JSON 형식으로 변환하기
    a = json.loads(r.text)
    if 'status_code' in a:
        continue
    else:
        b = a['genres']
        z = {}
        y = {}
        x = {}

        for i in range(len(b)):
            if vis[b[i]['id']] == 0:
                vis[b[i]['id']] = 1
                z["fields"] = {"name" : b[i]['name']}
                y["pk"] = (b[i]['id'])
                x["model"] = "movies.Genre"
                mid = dict(y, **z)
                total = dict(x, **mid)
                genres.append(total)    

            
            # print(x)
            # print(y)
            # data[x] = y
       
    # print('')
# print('')
# print(genres)
 
        
with open('TMDVGenredata.json', 'w', encoding="utf-8") as f:
    json.dump(genres, f, ensure_ascii=False, indent="\t")
```



```python
# 영화 데이터 JSON 만들기
import requests

import json
# import pandas as pd
# from io import StringIO


# API 지정

apikey = "91f3048e6d4f7b2729a87dcfbbef1b04"



# 정보를 알고 싶은 영화 리스트 만들기

movie_list = range(1, 10000)



# API 지정

api = "https://api.themoviedb.org/3/movie/{movies}?api_key={key}"



# string.format_map() 매핑용 클래스 만들기

class Default(dict):

    def __missing__(self, key):

        return key



# 각 영화의 정보 추출하기
data = []
x = 0
for name in movie_list:
    # API의 URL 구성하기

    url = api.format_map(Default(movies=name, key=apikey))

        # print(url)  # 데이터 확인

    # API에 요청을 보내 데이터 추출하기

    r = requests.get(url)  # json 형태의 데이터가 나온다.

        # print(type(r))  # <class 'requests.models.Response'>

    # 결과를 JSON 형식으로 변환하기
    a = json.loads(r.text)
    # print(type(a))
    # print(a)
    
    b = {}
    try:
        if 'status_code' in a:
            continue
        else :
            a['genres'] = [a['genres'][0]["id"]] 
            del a['belongs_to_collection']
            del a['budget']
            del a['imdb_id']
            del a['homepage']
            del a['id']
            del a['production_companies']
            del a['production_countries']
            del a['revenue']
            del a['runtime']
            del a['spoken_languages']
            del a['tagline']
            del a['video']
            del a['status']
            b['fields'] = a
            jd= {"model" : "movies.Movie", "pk": x }
            c = dict(jd, **b)
            data.append(c)
            x += 1
    except:
        continue

        

with open('TMDBdata.json', 'w', encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent="\t")
```



## 데이터 파일 DB에 load하기

```
#model.py에 data 모델 정의하기
$python manage.py loaddata {파일명.json}
 *주의 : json파일 1.models.py class내 fields 입력순서 맞추기, 
 			     2.model, pk, fields설정 필수
                     {
                        model: 'app명.class명',
                        pk: <int형>,
                        fields: {
                            ...
                        }

                     }

#데이터 보는법

1. pip install django-extensions //설치
2. settings.py에 INSTALLED_APPS에 'django_extensions'정의
3. shell로 들어가서 확인 

$python manage.py shell
>>>from app이름.models import 모델명
>>>모델명.objects.all()
```







---

## 스케줄링

#### 6월 11일  | 목

- [x] accounts 구현하기
- [x] JSON데이터 받아오기

#### 6월 12일   | 금

- [ ] movie쪽 만들기
- [ ] 알고리즘 만들기(국가별 해결)
- [ ] 그 전까지한거 체크

#### 6월 13일  |  토

- [ ] bootstrap으로 꾸미기
- [ ] 추가 사항 넣기(검색창) - 되면
- [ ] UCC 어떤식으로 만들지 구상하기

#### 6월 14일   |  일

- [ ] bootstrap으로 꾸미기
- [ ] UCC 만들기



---

