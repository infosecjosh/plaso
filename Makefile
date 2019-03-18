
.PHONY: build test-plugin test-formatter test

PLASOSETUP=/home/forensics/working/plaso/setup.py
LOG2TIMELINE=/usr/local/bin/log2timeline.py
PSORT=/usr/local/bin/psort.py
TESTDB=./test_data/mailstore.jpinkman2018@gmail.com.db
PLASOFILE=/home/forensics/testplaso.plaso
TESTJSON=/home/forensics/plaso.json
CSV=/home/forensics/plaso.csv

build: 
	sudo $(PLASOSETUP) install

test-plugin: 
	if [ -e $(PLASOFILE) ]; then rm $(PLASOFILE); fi
	$(LOG2TIMELINE) --parsers sqlite $(PLASOFILE) $(TESTDB)

test-formatter: 
	if [ -e $(TESTJSON) ]; then rm $(TESTJSON); fi
	if [ -e $(CSV) ]; then rm $(CSV); fi
	$(PSORT) -d -o l2tcsv -w $(CSV) $(PLASOFILE) 
	
test: test-plugin test-formatter

