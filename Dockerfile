FROM haoyangz/deepsea-predict-docker
MAINTAINER Haoyang Zeng  <haoyangz@mit.edu>

RUN apt-get update;apt-get install -y vim default-jre lzop
RUN pip install scikit-learn

RUN echo "r <- getOption('repos'); r['CRAN'] <- 'http://cran.us.r-project.org'; options(repos = r);" > ~/.Rprofile
RUN Rscript -e "install.packages('snow')"

RUN mkdir /script
COPY . /script/
RUN cd /script/data; wget http://gerv.csail.mit.edu/hg19.in.lzo -q; lzop -d hg19.in.lzo
WORKDIR /script/
