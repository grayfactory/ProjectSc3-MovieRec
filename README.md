# ProjectSc3-MovieRec

# PROJECT 주말N명화
본격, UserBase 영화 큐레이션 시스템
## 기획의도
넷플릭스, 디즈니, 애플TV, 유튜브 등등 볼거리는 넘처나는데 막상 볼 영화를 잘 고르지 못하는 당신을 위한 솔루션  
500편 이상을 본 검증된 User pool을 기반으로 당신의 취향과 유사한 User가 추천하는 **'볼만한'** 영화 큐레이션

## DB 구성
### The Movie Len
- 평점데이터셋: [GroupLens Movie data set](https://grouplens.org/datasets/movielens/) 
  - 53,889개 영화에 대한 유저 283,228명의 27,753,444개 평점 데이터
- 모든 평점 데이터를 사용하지 않고, 500개 이상의 영화에 평점을 남김 유저만 사용하였으며, 최소 930명 이상의 유저가 평점을 남긴 영화만 사용
  - 2590개 영화, 10,221명의 유저, 6,649,687개의 평점 데이터 사용
### Naver, YouTube API
- 한글 title, 국내 개봉 poster img를 얻기 위해 naver 영화 API사용
- YouTube 영화 trailer 영상 link를 위해 YouTube API사용


## DB schema
![schema](https://user-images.githubusercontent.com/74405346/112937095-031d3380-9162-11eb-805c-75ad417bdc40.png)

## Structure
![](https://user-images.githubusercontent.com/74405346/113112674-68495580-9244-11eb-8aad-5bf2fca738b5.png | width=100)
