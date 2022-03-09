# 1. Base image
FROM python:3.8.3-slim-buster

# Define Labels
LABEL name="which solana nft to mint." \
      description="Furnish insights about next solana nft project and sort them according to the hype (based on their number of twitter followers." \
      version="0.1" \
      url="https://gitlab.tech.orange/newmanagedservices/images/python-mongo-extract" \
      maintainer="thibaut.allain29@gmail.com"

# Define environnment variables
ENV TINI_VERSION="v0.19.0"
ENV WORKDIR=/data
ENV PYTHONUSER=python

# Define arguments we can pass to the docker build
ARG TOP
ARG PERIOD
ENV TOP=${TOP:-10}
ENV PERIOD=${PERIOD:-5}

ARG GIT_HASH
ENV GIT_HASH=${GIT_HASH:-dev}

# Create dedicated Working Directory
RUN mkdir $WORKDIR && \
    chmod 755 $WORKDIR

# Add Working Directory    
WORKDIR $WORKDIR

# Get Source files and install prerequisites
COPY src/* .
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini

# Install dependencies 
RUN pip install -U \
    pip \
    setuptools \
    wheel

RUN pip install -r requirements.txt

# Create Python default user
RUN useradd -m -r $PYTHONUSER && \
    chown user $WORKDIR

COPY . /src

# Install dependencies
RUN pip install -r requirements.txt

USER $PYTHONUSER

# Execute python script
ENTRYPOINT ["/tini", "--"]

CMD [ "sh", "c", "python run.py --top=${TOP} --period=${PERIOD}" ]
