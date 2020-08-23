#DOCKER FILE - SEGMENTATION ENTRY

FROM python:3.8-slim-buster

WORKDIR /var/pyvinci

RUN apt-get update -y

RUN apt-get -y install nano git build-essential libglib2.0-0 libsm6 libxext6 libxrender-dev

RUN pip install torch==1.6.0+cpu torchvision==0.7.0+cpu -f https://download.pytorch.org/whl/torch_stable.html

RUN pip install cython

RUN pip install pyyaml==5.1 

RUN pip install pycocotools 

RUN pip install opencv-python 

RUN pip install -U 'git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI'

RUN python -m pip install detectron2 -f https://dl.fbaipublicfiles.com/detectron2/wheels/cpu/index.html

RUN pip install sqlalchemy

RUN pip install psycopg2-binary

COPY . .

CMD ["python3", "worker-segmentation.py"]

