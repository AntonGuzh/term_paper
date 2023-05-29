FROM python
COPY . /project
WORKDIR /project

SHELL ["/bin/bash", "-c"]
RUN apt-get update && \
    apt install texlive-latex-extra -y && \
    apt install texlive-lang-cyrillic -y && \
    apt install texlive-lang-greek -y
SHELL ["/bin/sh", "-c"]
RUN pip3 install -r requirements.txt

CMD ["python", "./bot.py"]