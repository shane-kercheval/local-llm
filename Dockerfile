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
WORKDIR /llms/models/
RUN wget https://huggingface.co/eachadea/ggml-vicuna-13b-1.1/resolve/main/ggml-vic13b-q5_1.bin
# getting this for alpaca model; author for vicuna updated to latest version but couldn't find
# latest version of alpaca; re-add at later time
# error loading model: this format is no longer supported (see https://github.com/ggerganov/llama.cpp/pull/1305)
# llama_init_from_file: failed to load model
# RUN wget https://huggingface.co/Sosaka/Alpaca-native-4bit-ggml/resolve/main/ggml-alpaca-7b-q4.bin

# install python packages
WORKDIR /code
ENV PYTHONPATH "${PYTHONPATH}:/code:/code/source"
RUN python -m pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN rm requirements.txt
WORKDIR /code

# RUN pip install git+https://github.com/huggingface/transformers

RUN apt-get update -y && apt-get install zsh -y
RUN PATH="$PATH:/usr/bin/zsh"


# ### Used for selenium
# RUN apt-get update && apt-get install -y \
#     apt-transport-https \
#     ca-certificates \
#     curl \
#     gnupg \
#     --no-install-recommends \
#     && curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
#     && echo "deb https://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
#     && apt-get update && apt-get install -y \
#     google-chrome-stable \
#     --no-install-recommends
# RUN wget https://chromedriver.storage.googleapis.com/108.0.5359.71/chromedriver_linux64.zip && \
#     unzip chromedriver_linux64.zip && \
#     rm chromedriver_linux64.zip && \
#     chmod +x chromedriver && \
#     mv chromedriver /usr/local/bin/
# RUN apt install -y gconf-service libasound2 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils wget


CMD '/bin/zsh'
