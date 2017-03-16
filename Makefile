
MKVENV = devtools/mkvenv

LOCFILES = $(addsuffix .lock, $(basename $(wildcard test/*.open)))

.PHONY: all
all: requirements.lock $(LOCFILES)


requirements.lock: requirements.open
	touch $@
	pip install -r $@
	pip install -r $^
	pip freeze >$@


test/%.lock: test/%.open $(MKVENV)
	$(MKVENV) $(basename $(notdir $<)) $(basename $<)
