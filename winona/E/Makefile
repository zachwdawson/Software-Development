PYTHON = python3

.PHONY : setup

.DEFAULT_GOAL = setup

setup:
	@echo "Installing Requirements..."
	pip3 install --user -r Other/requirements.txt
	dos2unix xtcp
	chmod +x xtcp

