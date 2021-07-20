FROM ubuntu:latest

RUN apt upgrade
RUN apt update -y

RUN apt install git -y
RUN apt install curl -y

RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | RUN gpg --dearmor -o /usr/share/keyrings/githubcli-archive-keyring.gpg
RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null

RUN apt update
RUN apt install gh
