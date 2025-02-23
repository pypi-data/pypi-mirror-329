# if __name__ == "__main__":
#     from gguf_comfy import downloader

import json, requests, urllib.request
from tqdm import tqdm
def read_json_file(file_path):
    response = urllib.request.urlopen(file_path)
    data = json.loads(response.read())
    return data
def download_7z_file(url, output_filename):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        total_size = int(response.headers.get('content-length', 0))
        with open(output_filename, 'wb') as file, tqdm(desc=
            f'Downloading {output_filename}', total=total_size, unit='B',
            unit_scale=True, unit_divisor=1024) as progress_bar:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
                progress_bar.update(len(chunk))
        print(f'Downloaded {output_filename} to the current directory.')
    else:
        print('Failed to download the file. Seems encountering a connection problem.')
if __name__ == '__main__':
    print('Please select:\n1. download gguf pack\n2. download comfy pack')
    choice = input('Enter your choice (1 to 2): ')
    if choice == '1': # gguf pack option
        version = ('https://raw.githubusercontent.com/calcuis/gguf-pack/main/version.json')
        ver = read_json_file(version)
        url = (f"https://github.com/calcuis/gguf-pack/releases/download/{ver[0]['version']}/GGUF_windows_portable.7z")
        output_filename = 'gguf.7z'
        download_7z_file(url, output_filename)
    elif choice == '2': # gguf comfy option
        from gguf_comfy import downloader
    else:
        print('Not a valid number.')