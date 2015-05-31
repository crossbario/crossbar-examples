# When on Windows and starting GNU make from Git bash,
# we need to set this:
ifdef COMSPEC
   SHELL=C:/Windows/System32/cmd.exe
endif

all: uninstall install

install:
	exit | sqlplus -L -S ${CROSSBAR_ORACLE} @install.sql

uninstall:
	exit | sqlplus -L -S ${CROSSBAR_ORACLE} @uninstall.sql

download:
	curl http://downloads.dbpedia.org/3.8/en/persondata_en.ttl.bz2 -O persondata_en.ttl.bz2
	bzip2 -d persondata_en.ttl.bz2

preprocess:
	python persondata.py persondata_en.ttl persondata_en.csv

load:
	sqlldr ${CROSSBAR_ORACLE} control=persondata.ctl data=persondata_en.csv

insert:
	exit | sqlplus -L -S ${CROSSBAR_ORACLE} @persondata.sql
