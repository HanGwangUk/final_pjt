# SSAFY 최종 프로젝트

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



## API를 통해 받은 데이터 파일 생성

1. The Movie Data Base 에 가입하여 API_KEY 생성
2. 원하는 데이터를 담은 JSON 파일을 생성할 Python Code 작성

```python
import requests # Python에서 requests를 실행하기 위해서
import json

# API 지정
apikey = "Your_API"

# 정보를 알고 싶은 영화 리스트 만들기
movie_list = range(1, 1000)



# API 지정
api = "https://api.themoviedb.org/3/movie/{movies}?api_key={key}"

# string.format_map() 매핑용 클래스 만들기

class Default(dict):
    def __missing__(self, key):
        return key

# 각 영화의 정보 추출하기
data = []

for name in movie_list:
    
    # API의 URL 구성하기
    url = api.format_map(Default(movies=name, key=apikey))

    # API에 요청을 보내 데이터 추출하기
    r = requests.get(url)  # json 형태의 데이터가 나온다.

    # 결과를 JSON 형식으로 변환하기
    jd = json.loads(r.text)
    
    # 받아올 수 없는 데이터에는 status_code가 출력되어서 없는 것들만 data에 넣기
    if 'status_code' in jd:
        continue
    else:
        data.append(jd)

# json 데이터를 json 파일로 생성하기
with open('TMDVdata.json', 'w', encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent="\t")

```









---

## 스케줄링

#### 6월 11일  | 목

- [x] accounts 구현하기
- [x] JSON데이터 받아오기

#### 6월 12일   | 금

- [ ] movie쪽 만들기
- [ ] 알고리즘 만들기
- [ ] 그 전까지한거 체크

#### 6월 13일  |  토

- [ ] bootstrap으로 꾸미기
- [ ] 추가 사항 넣기(검색창) - 되면
- [ ] UCC 어떤식으로 만들지 구상하기

#### 6월 14일   |  일

- [ ] bootstrap으로 꾸미기
- [ ] UCC 만들기



