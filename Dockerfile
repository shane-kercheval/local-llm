FROM python:3.10

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y nano

# install lamma.cpp
# WORKDIR /
# RUN git clone https://github.com/ggerganov/llama.cpp
# WORKDIR /llama.cpp
# RUN make

# download vicuna model
WORKDIR /code/models/
RUN wget https://huggingface.co/eachadea/ggml-vicuna-13b-1.1/resolve/main/ggml-vicuna-13b-1.1-q4_0.bin
RUN wget https://huggingface.co/Sosaka/Alpaca-native-4bit-ggml/resolve/main/ggml-alpaca-7b-q4.bin




# install python packages
WORKDIR /code
ENV PYTHONPATH "${PYTHONPATH}:/code"
RUN python -m pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN rm requirements.txt
WORKDIR /code

RUN apt-get update -y && apt-get install zsh -y
RUN PATH="$PATH:/usr/bin/zsh"

CMD '/bin/zsh'
