## Emergency AI
### Folder 
`Module` : main.py를 실행할 때 필요한 파일

`weights` : 모델 학습시킨 가중치 폴더가 들어있음 

<br>

### Python file

`Crawling.py` : 이미지를 크롤링하기 위한 코드 

`Crawling.py` : Custom Yolov5 model을 사용하여 `경추 7`번과 `귀` 부분을 detection 하는 코드

`main.py` : main.py 

<br>

### Folder Tree

```commandline
├── Crawling.py
├── Image_detect.py
├── Module
│   ├── Draw
│   │   ├── XYvalue.py
│   │   ├── __pycache__
│   │   │   ├── XYvalue.cpython-38.pyc
│   │   │   └── draw.cpython-38.pyc
│   │   └── draw.py
│   └── Frame
│       ├── __pycache__
│       │   └── setting.cpython-38.pyc
│       └── setting.py
├── README.md
├── __pycache__
├── main.py
└── weights
    ├── README.md
    ├── TEST_IMG.png
    └── Version_1.pt
```
