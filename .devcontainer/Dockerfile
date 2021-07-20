FROM ubuntu:latest as Base

# GH Repo installation
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | RUN gpg --dearmor -o /usr/share/keyrings/githubcli-archive-keyring.gpg
RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
RUN apt update
RUN apt upgrade -y

FROM Base as Dependency-Installs
RUN apt install git -y
RUN apt install gh -y
# Python 3.9.6 dependencies
RUN apt install build-essential gdb lcov libbz2-dev libffi-dev libgdbm-dev liblzma-dev libncurses5-dev libreadline6-dev libsqlite3-dev libssl-dev lzma lzma-dev tk-dev uuid-dev zlib1g-dev -y
