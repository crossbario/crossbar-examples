default:
	@echo "targets: requirements run"

requirements:
	# tested on Ubuntu 18.04.1 LTS + CPython 3.7.2 (from source)
	# https://kivy.org/doc/stable/installation/installation-linux.html#dependencies-with-sdl2

	# Install necessary system packages
	sudo apt-get install -y \
		build-essential \
		ffmpeg \
		libsdl2-dev \
		libsdl2-image-dev \
		libsdl2-mixer-dev \
		libsdl2-ttf-dev \
		libportmidi-dev \
		libswscale-dev \
		libavformat-dev \
		libavcodec-dev \
		zlib1g-dev \
		xclip

	# Install gstreamer for audio, video (optional)
	sudo apt-get install -y \
		libgstreamer1.0 \
		gstreamer1.0-plugins-base \
		gstreamer1.0-plugins-good

	#sudo apt install -y libegl1-mesa-dev
	pip install -r requirements.txt

run:
	crossbarfx edge start

run_exe_standalone:
	~/crossbarfx-linux-amd64-20190120-1765597 edge start

run_exe_managed:
	CROSSBAR_FABRIC_URL="ws://localhost:9000/ws" ~/crossbarfx-linux-amd64-20190120-1765597 edge start
