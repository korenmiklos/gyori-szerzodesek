PAGES = $(shell seq 1 128)
DOCUMENTS = $(shell echo raw/doc/*)
WORD = $(shell echo raw/doc/*.doc?)

all_documents: $(foreach document, $(DOCUMENTS), output/$(notdir $(document)).txt)
csv: $(foreach document, $(WORD), output/$(basename $(notdir $(document))).csv)
docx: $(foreach document, $(WORD), temp/docx/$(basename $(notdir $(document))).docx)
pages: $(foreach page, $(PAGES), raw/html/$(page)-oldal.html)
raw/html/%-oldal.html: 
	wget -O $@ "http://onkormanyzat.gyor.hu/cikklista/uvegzseb.html/$(notdir $(basename $@))"
	touch $@
documents: documents.txt
	aria2c -x5 -j5 -d raw/doc -i $<
	touch $@ 
pages: pagelist.txt
	aria2c -x5 -d raw/html -i $<
	touch $@ 
pagelist.txt: raw/html/*-oldal.html
	echo "" > $@
	for file in raw/html/*-oldal.html; do \
		grep "article_preliminary" $$file | grep -orh 'cikk/.*szerz.*\.html' | awk '{print "http://onkormanyzat.gyor.hu/"$$0}' >> $@ ; \
	done
documents.txt: raw/html/*szerz*.html
	rm $@ || true
	touch $@
	for file in raw/html/*szerz*.html; do \
		tail -n +550 $$file | head -n +233 | grep "getAttachement" | grep -ohE '\"http.*?\"' | sed 's/"//g' >> $@ || true ; \
		tail -n +550 $$file | head -n +233 | grep "data/files" | grep -ohE '\"http.*?\"' | sed 's/"//g' >> $@ || true ; \
	done
temp/docx/%.docx: raw/doc/%.doc
	 soffice --convert-to docx --outdir temp/docx $< 
temp/docx/%.docx: raw/doc/%.docx
	 cp $< $@ 
output/%.txt: raw/doc/%
	if [ '$(suffix $<)' = '.doc' ] ; then \
		antiword -m 8859-2.txt $< | iconv -f iso-8859-2 -t utf-8 > $@; \
	else \
		pdftotext $< | iconv -f iso-8859-2 -t utf-8 > $@; \
	fi	
output/all.csv: raw/doc/*.doc* extract_table.py
	python extract_table.py > $@
