FROM python:3.7.2
LABEL maintainer="Anish"

ENV TZ=Africa/Johannesburg

RUN pip install --upgrade pip

# The `WORKDIR` directive will create the directory if it doesn't exist
WORKDIR /usr/local/tal/business_seconds

ENV LIBRDKAFKA_VERSION 0.9.1
RUN curl -Lk -o /root/librdkafka-${LIBRDKAFKA_VERSION}.tar.gz https://github.com/edenhill/librdkafka/archive/${LIBRDKAFKA_VERSION}.tar.gz && \
    tar -xzf /root/librdkafka-${LIBRDKAFKA_VERSION}.tar.gz -C /root && \
    cd /root/librdkafka-${LIBRDKAFKA_VERSION} && \
    ./configure && make && make install && make clean && ./configure --clean && \
    ldconfig

# As `WORKDIR` was set, the `COPY` destination can be relative
COPY . .

# We can chain the `RUN` directives into a single command
# to use only a single layer
RUN pip install --extra-index-url https://admin:GIXsa5sDvejKfy9IGnhD@pypi.takealot.com/pypi -e .
