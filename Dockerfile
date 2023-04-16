FROM python:3.10

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y nano

RUN apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# install lamma.cpp
# WORKDIR /
# RUN git clone https://github.com/ggerganov/llama.cpp
# WORKDIR /llama.cpp
# RUN make

# download models
WORKDIR /code/models/
RUN wget https://huggingface.co/eachadea/ggml-vicuna-13b-1.1/resolve/main/ggml-vicuna-13b-1.1-q4_0.bin
RUN wget https://huggingface.co/Sosaka/Alpaca-native-4bit-ggml/resolve/main/ggml-alpaca-7b-q4.bin


# install python packages
WORKDIR /code
ENV PYTHONPATH "${PYTHONPATH}:/code:/code/source"
RUN python -m pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN rm requirements.txt
WORKDIR /code

RUN apt-get update -y && apt-get install zsh -y
RUN PATH="$PATH:/usr/bin/zsh"

CMD '/bin/zsh'
