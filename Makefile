PAGES = $(shell seq 1 128)
pages: $(foreach page, $(PAGES), raw/html/$(page)-oldal.html)
raw/html/%-oldal.html: 
	wget -O $@ "http://onkormanyzat.gyor.hu/cikklista/uvegzseb.html/$(notdir $(basename $@))"
	touch $@
pages: pagelist.txt
	aria2c -x5 -d raw/html -i $<
	touch $@ 
pagelist.txt: raw/html/*-oldal.html
	echo "" > $@
	for file in raw/html/*-oldal.html; do \
		grep "article_preliminary" $$file | grep -orh 'cikk/.*szerz.*\.html' | awk '{print "http://onkormanyzat.gyor.hu/"$$0}' >> $@ ; \
	done
