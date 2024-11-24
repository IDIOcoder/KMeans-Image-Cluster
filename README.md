# KMeans-Image-Cluster

![sample_image](sample_image)

## 설명
이 프로그램은 학교 과제의 일환으로 Sklearn 라이브러리의 KMeans 모듈을 활용하여 제작된 이미지 클러스터링 도구입니다.
기본적으로 RGB 공간에서 클러스터링을 수행할 수 있으며, 거리 가중치를 고려하여 RGBxy의 5차원 공간에서도 클러스터링을 실행할 수 있도록 설계되었습니다.
사용자 친화적인 인터페이스를 제공하기 위해 CustomTkinter를 사용해 GUI를 구현하였습니다.

## 설치
### 1. 환경 설정
- python 3.12 (해당 버전에서 제작되었습니다)
- pip
### 2. 라이브러리 설치
우선, 가상환경을 설정하고 사용하는 것을 강력히 추천합니다.
run.py 실행시 필요한 라이브러리를 자동으로 설치하도록 코드를 작성하긴 하였으나, 올바르게 동작하지 않을 수 있습니다.
그럴 경우 아래의 명령어를 통해 필요한 라이브러리를 다운로드 하세요.
```
pip install -r requirements.txt
```

## 사용법
1. Select Image를 통해 이미지를 불러옵니다.
2. Cluster에 설정할 클러스터의 수를 입력하세요 (K>0)
3. 차원을 선택합니다 (RGB / RGB+XY)
4. RUN을 눌러 실행합니다.
   
- RGB+XY의 경우 거리 가중치를 입력해야합니다.
- RGB+XY기반 클러스터링시 PCA스위치를 on/off 하여 PCA기반 3차원 그래프/RGB기반 3차원 그래프 를 확인하실 수 있습니다. (실행 후에도 가능)
- Visualize를 on/off하여 그래프를 확인하실 수 있습니다.
- Save를 통해 클러스터링된 이미지 / 그래프를 다운하실 수 있습니다. 
