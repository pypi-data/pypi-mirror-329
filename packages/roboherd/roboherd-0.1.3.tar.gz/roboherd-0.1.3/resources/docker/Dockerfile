FROM helgekr/bovine:0.5.18-python3.13

ARG tag
RUN pip install roboherd==#{tag}

RUN mkdir /app
WORKDIR /app

CMD ["/bin/sh"]
