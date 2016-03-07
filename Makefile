.PHONY:
install:
	xargs -a apt-requirements.txt sudo apt-get -y install
