FROM python

RUN  python -m pip install tinytuya pyyaml
COPY *.py .
COPY config.yaml .
