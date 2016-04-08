all : Contest.py ContestUI.py
	@continue

ContestUI.py : ContestUI.ui
	pyuic5 ContestUi.ui > ContestUI.py

test: 
	python Contest.py
