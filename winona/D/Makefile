PYTHON = python3

.PHONY : setup clean all

.DEFAULT_GOAL = all

setup:
	@echo "Installing Requirements..."
	pip3 install --user -r Other/requirements.txt
	dos2unix xgui
	chmod +x xgui

clean:
	rm -rf dist
	rm -f xgui.spec
	rm -rf build

all: | clean setup

