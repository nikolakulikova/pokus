FROM python
#FROM
#VOLUME ["[2222/222]"]
#ADD --chmod=655  /somedir/
#COPY hom?.txt /mydir/
#COPY  /mydir/
RUN --network=default ls
RUN --network=noe ls
RUN --security=default ls
RUN --security=insecure ls
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
  --mount=type=cache,target=/var/lib/apt,sharing=locked \
  ls
RUN /bin/bash -c "echo hello"
RUN ["/bin/bash", "-c", "echo hello"]
#RUN ['echo hello']
#RUN 'echo hello'
#RUN "echo hello"
#CMD ["ls"]
#CMD ['ls']
#CMD echo 'This is a test.'
#LABEL "com.example.vendor"="ACME Incorporated"
#LABEL "com.example.vendor"=""
#LABEL "com.example.vendor"=
#LABEL ="ACME Incorporated"
#LABEL "com.example.vendor""ACME Incorporated"
#EXPOSE 80/udp
#EXPOSE 80
#EXPOSE /udp
#EXPOSE udp
#EXPOSE 80udp
#ENV MY_NAME="John Doe"
#ENV MY_NAME=
#ENV ="John Doe"
#ENV "John Doe"
#ENV MY_NAME
#ADD hom* /mydir
#ADD  /mydir/
#ADD --chown=10:11 files* /somedir/
#ADD --chown=1 files* /somedir/
#ADD --chown=myuser:mygroup --chmod=655 files* /somedir/
#ADD --chown=myuser:mygroup --chmod=655  /somedir/
#ADD --chown= --chmod=655  /somedir/
#ADD --chown= --chmod  /somedir/
#ADD --chownmyuser:mygroup --chmod=655 files* /somedir/
#ADD --chown=myuser:mygroup --chmod655 files* /somedir/
#ENTRYPOINT ["ls"]
#ENTRYPOINT ["ls"]
#ENTRYPOINT ['ls']
#ENTRYPOINT 'ls'
#VOLUME /myvol
#VOLUME "/myvol"
#VOLUME
#USER patrick
#USER "patrick"
#USER patrick:aaa
#USER patrick:
#WORKDIR /a
#WORKDIR "/a"
#ARG buildno
#ARG buildno=
#ARG buildno=aaa
#ONBUILD ADD . /app/src
#ONBUILD ADD  /app/src
#ONBUILD ADD  "/app/src" .
#SHELL ["ls"]
#SHELL ["ls"
#SHELL "ls"]
#SHELL "ls"
#
#HEALTHCHECK --interval=5m --timeout=3s \
#  CMD curl -f http://localhost/ || exit 1
#HEALTHCHECK --interval=5m --timeout=3s \
#   curl -f http://localhost/ || exit 1
#HEALTHCHECK curl -f http://localhost/
#HEALTHCHECK NONE CMD curl -f http://localhost/
#HEALTHCHECK NONE
#
#ADD --link aaa aa
#ADD --link aaa
#COPY --link aaa
#COPY --parents aaa aa
#COPY --parent aaa aa
#COPY -parent aaa aa
#COPY -aa aaa aa
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
  --mount=type=cache,target=/var/lib/apt,sharing=locked \
  apt update && apt-get --no-install-recommends install -y gcc \

RUN 'ls'