FROM mcr.microsoft.com/vscode/devcontainers/python:3.13

#
# Update the OS and maybe install packages
#
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get upgrade -y

# install git and git-lfs
RUN apt-get install -y sudo git git-lfs

# remove temporary files
RUN apt-get autoremove -y
RUN apt-get clean -y
RUN rm -rf /var/lib/apt/lists/*

# Install the project dependencies
RUN mkdir -p /usr/src/agentsagi
COPY ./requirements.txt /usr/src/agentsagi/
WORKDIR /usr/src/agentsagi
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /usr/src
RUN rm -rf /usr/src/agentsagi

# Set the default command to bash
CMD ["/bin/bash"]