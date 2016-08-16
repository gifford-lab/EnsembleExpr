FROM haoyangz/deepsea-predict-docker
MAINTAINER Haoyang Zeng  <haoyangz@mit.edu>

RUN apt-get install -y vim default-jre
RUN pip install scikit-learn

RUN echo "r <- getOption('repos'); r['CRAN'] <- 'http://cran.us.r-project.org'; options(repos = r);" > ~/.Rprofile
RUN Rscript -e "install.packages('snow')"

RUN mkdir /script
COPY . /script/
RUN wget http://gerv.csail.mit.edu/hg19.in -q -O /script/data/hg19.in
WORKDIR /script/
