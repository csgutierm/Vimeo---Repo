import subprocess
import requests
import shutil
import os
import re

dirs_to_cr = [
    'bin', 'Downloads/Finished/Vimeo', 'Downloads/Temp'
]

for directory_path in dirs_to_cr:
    os.makedirs(directory_path, exist_ok=True)

temp_dir = 'Downloads/Temp'
if os.path.exists(temp_dir):
    shutil.rmtree(temp_dir)

yt_dl = '.\\bin\\yt-dlp.exe'
ffm = '.\\bin\\ffmpeg.exe'

print('''
v2 playlist.json link
''')

link = input('Link: ')

try:
    bef_v2 = re.findall(r'(https:.*exp.*hmac.*)/v2/playlist', link)[0].strip()
except IndexError:
    print(' [ERROR] this is not a v2 playlist.json link!')
    ex_it = input('\nEnter to close..')
    exit()    

video_title = input('\nVideo title here: ')

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}

resp = requests.get(link, headers=headers).json()

video_data = [
    {
        'id': re.match(r'(.*?)-', video['id']).group(1),
        'width': video['width'],
        'height': video['height'],
        'video_res': f"{video['width']}x{video['height']}",
        'video_link': f"{bef_v2}/parcel/video/{re.match(r'(.*?)-', video['id']).group(1)}.mp4"
    }
    for video in resp['video']
]

audio_data = [
    {
        'id': re.match(r'(.*?)-', audio['id']).group(1),
        'codecs': audio['codecs'],
        'bitrate': audio['bitrate'],
        'audio_details': f"{audio['codecs']}, {audio['bitrate']}",
        'audio_link': f"{bef_v2}/parcel/audio/{re.match(r'(.*?)-', audio['id']).group(1)}.mp4"
    }
    for audio in resp['audio']
]

video_data.sort(key=lambda x: (x['width'], x['height']), reverse=True)
audio_data.sort(key=lambda x: x['bitrate'], reverse=True)

sel_vid_name = video_data[0]['video_res']
selected_video_link = video_data[0]['video_link']
sel_aud_name = audio_data[0]['audio_details']
selected_audio_link = audio_data[0]['audio_link']
print(f"\nbest video: {sel_vid_name}")
print(f"best audio: {sel_aud_name}\n")
    
subprocess.run([yt_dl, '-N', '16', '--no-warning', '--no-check-certificate', '-o', f'{temp_dir}\\{sel_vid_name}.mp4', selected_video_link])
print()
subprocess.run([yt_dl, '-N', '16', '--no-warning', '--no-check-certificate', '-o', f'{temp_dir}\\{sel_aud_name}.aac', selected_audio_link])

if sel_vid_name and sel_aud_name:
    output_x = f'Downloads\\Finished\\Vimeo\\{video_title}_{sel_vid_name}.mp4'
    print('\n [INFO] ffmpeg process started...\n')
    subprocess.run([ffm, '-v', 'quiet', '-stats', '-y', '-i', f'{temp_dir}\\{sel_vid_name}.mp4', '-i', f'{temp_dir}\\{sel_aud_name}.aac', '-c', 'copy', output_x])
else:
    print("\n [ERROR] Need video and audio picked..")

print(f'\n [INFO] File moved here:\n {output_x}')
print('\n [INFO] Deleting unnecessary files..')

temp_dir = 'Downloads/Temp'
if os.path.exists(temp_dir):
    shutil.rmtree(temp_dir)

print(' [INFO] All done.')
ex_it = input('\nEnter to close..')
exit()