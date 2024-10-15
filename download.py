import requests
import os

ASEPRITE_REPOSITORY = 'aseprite/aseprite'
SKIA_REPOSITORY = 'aseprite/skia'
SKIA_RELEASE_FILE_NAME = 'Skia-Windows-Release-x64.zip'
VERSION_FILE = 'version.txt'

def get_latest_tag_aseprite():
	response = requests.get(f'https://api.github.com/repos/{ASEPRITE_REPOSITORY}/releases/latest')
	response_json = response.json()
	return response_json['tag_name']

def get_current_version():
	if os.path.exists(VERSION_FILE):
		with open(VERSION_FILE, 'r') as f:
			return f.read().strip()
	return None

def save_aseprite_tag(tag):
	with open(VERSION_FILE, 'w') as f:
		f.write(tag)

def clone_aseprite(tag):
	clone_url = f'https://github.com/{ASEPRITE_REPOSITORY}.git'
	git_cmd = f'git clone -b {tag} {clone_url} src/aseprite --depth 1'
	os.system(git_cmd)
	os.system('cd src/aseprite && git submodule update --init --recursive')

def get_latest_tag_skia():
	response = requests.get(f'https://api.github.com/repos/{SKIA_REPOSITORY}/releases/latest')
	response_json = response.json()
	return response_json['tag_name']

def download_skia_for_windows(tag):
	download_url = f'https://github.com/{SKIA_REPOSITORY}/releases/download/{tag}/{SKIA_RELEASE_FILE_NAME}'

	file_response = requests.get(download_url)
	file_response.raise_for_status()
	
	with open(f'src/{SKIA_RELEASE_FILE_NAME}', 'wb') as f:
		f.write(file_response.content)
	
	os.system(f'7z x src/{SKIA_RELEASE_FILE_NAME} -osrc/skia')

if __name__ == '__main__':
	aseprite_tag = get_latest_tag_aseprite()
	current_version = get_current_version()

	if aseprite_tag != current_version:
		clone_aseprite(aseprite_tag)
		save_aseprite_tag(aseprite_tag)

		skia_tag = get_latest_tag_skia()
		download_skia_for_windows(skia_tag)
	else:
		print("Already at the latest version.")
