FROM python:3.7

RUN  pip3 install --upgrade pip setuptools wheel &&\
     pip3 install numpy scipy &&\
     pip3 install networkx &&\
     pip3 install openpyxl &&\
     pip3 install pandas &&\
     pip3 install shapely &&\
     pip3 install pyproj &&\
     pip3 install uesgraphs &&\
     pip3 install -e git+https://github.com/RWTH-EBC/richardsonpy.git#egg=richardsonpy &&\
     pip3 install pytest-cov &&\
     pip3 install coveralls &&\
     pip3 install flake8


RUN pip install sphinx numpydoc

COPY . /pycity_base

RUN pip install -e ./pycity_base

WORKDIR /pycity_base/doc
CMD ./docu.sh
