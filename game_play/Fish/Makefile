PYTHON = python3

.PHONY : setup

.DEFAULT_GOAL = setup

setup:
	@echo "Installing Requirements..."
	pip3 install --user -r Common/requirements.txt
	dos2unix Common/main.py
	chmod +x Common/main.py

