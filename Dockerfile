FROM ubuntu:21.10
ARG BUILD_CONCURRENCY
RUN apt-get update && apt-get install -y locales  && rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8
RUN ln -fs /usr/share/zoneinfo/America/Chicago /etc/localtime
RUN apt-get update && apt-get install -y tzdata  python3  python3-pip python3-dev python-is-python3
RUN dpkg-reconfigure --frontend noninteractive tzdata
RUN mkdir -p /src  && mkdir -p /opt
RUN apt-get update && \
    apt-get install -y --no-install-recommends wget ca-certificates tzdata\
    libboost-program-options-dev build-essential libboost-regex-dev libboost-date-time-dev libboost-chrono-dev\
    libboost-filesystem-dev autoconf libboost-iostreams-dev libboost-thread-dev expat liblua5.2-0 libtbb2 git\
    libboost-dev  libzmq5-dev swig cmake automake libtool tmux
WORKDIR /

RUN wget https://github.com/GMLC-TDC/HELICS/releases/download/v2.8.0/Helics-v2.8.0-source.tar.gz
RUN mkdir helics
WORKDIR helics
RUN tar -xzvf ../Helics-v2.8.0-source.tar.gz 
#2.8 does not work
RUN mkdir build
WORKDIR /helics/build
RUN cmake -DBUILD_PYTHON_INTERFACE=ON -DCMAKE_CXX_FLAGS="-fPIC -std=c++14" ..
RUN  NPROC=${BUILD_CONCURRENCY:-$(grep -c ^processor /proc/cpuinfo 2>/dev/null || 1)} && make -j${NPROC} install
RUN wget http://apache.mirrors.pair.com//xerces/c/3/sources/xerces-c-3.2.3.tar.gz
RUN tar -xzf xerces-c-3.2.3.tar.gz
WORKDIR xerces-c-3.2.3
RUN ./configure CFLAGS="-Wno-error" CPPFLAGS="-Wno-error"
RUN NPROC=${BUILD_CONCURRENCY:-$(grep -c ^processor /proc/cpuinfo 2>/dev/null || 1)} && make -j${NPROC} install
RUN pip install pytz traci dask[dataframe] pandas numpy textx openpyxl

WORKDIR /
RUN git clone https://github.com/gridlab-d/gridlab-d.git gridlab-d
WORKDIR gridlab-d
RUN git checkout 725bec8d7fd57134607559199b795acc1722d494
RUN autoreconf -fi
RUN ./configure --with-helics --with-xerces --enable-silent-rules "CFLAGS=-g -O0 -w" "CXXFLAGS=-g -O0 -w -std=c++14" "LDFLAGS=-g -O0 -w"
RUN NPROC=${BUILD_CONCURRENCY:-$(grep -c ^processor /proc/cpuinfo 2>/dev/null || 1)} && make -j${NPROC} install
WORKDIR /

RUN rm -rf gridlab-d helics xerces-c-3.2.3

# Install latest sumo package.
RUN echo "deb https://ppa.launchpadcontent.net/sumo/stable/ubuntu impish main" >> /etc/apt/sources.list
RUN echo "deb-src https://ppa.launchpadcontent.net/sumo/stable/ubuntu impish main " >> /etc/apt/sources.list
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 4B339D18DD12CA62CA0E400F87637B2A34012D7A
RUN apt-get update && apt-get -qq install sumo sumo-tools sumo-doc vim
 
RUN touch start-session.sh
RUN echo "tmux new-session -s \"gridlab\" -d" >start-session.sh
RUN echo "tmux split-window -h" >>start-session.sh
RUN echo "tmux split-window -v" >>start-session.sh
RUN echo "tmux -2 attach-session -d" >>start-session.sh
RUN chmod +x start-session.sh

ENV PYTHONPATH "${PYTHONPATH}:/usr/local/python"
ENV SUMO_HOME '/usr/share/sumo/'
RUN git clone https://github.com/adubey14/HELICS-Tutorial.git gridlab-tutorial
ENV HOME "/"
COPY . transit-gym
WORKDIR /transit-gym/src
RUN pip install .
RUN apt-get update && apt-get -qq install unzip

WORKDIR /transit-gym/examples/HelloWorld/network
RUN unzip Chattanooga_SUMO_Network.net.zip

WORKDIR /