PYTHON = python3

.PHONY : setup

.DEFAULT_GOAL = setup

setup:
	@echo "Installing Requirements..."
	pip3 install --user -r ../Fish/Common/requirements.txt
	dos2unix ../Fish/Common/main.py
	chmod +x ../Fish/Common/main.py

