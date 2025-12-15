all: \
  interrupt_resume.json

%.json: %.py
	python $< >& $@

clean:
	@rm -f *~ *.json
