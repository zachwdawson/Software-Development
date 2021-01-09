PYTHON = python3

.PHONY : setup clean all

.DEFAULT_GOAL = all

setup:
	@echo "Installing Requirements..."
	pip3 install --user -r requirements.txt
	dos2unix ../xjson
	chmod +x ../xjson

clean:
	rm -rf dist
	rm -f xjson.spec
	rm -rf build

all: | clean setup

