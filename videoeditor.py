import json
from moviepy.editor import *
import sys, random, threading, string, os
import shutil
from mutagen.easymp4 import EasyMP4Tags
import mutagen
import glob
import subprocess

videos = []
background = []
letters = string.ascii_lowercase

def spoofKeys(media_file):
    global letters

    actualKeys = '', *sorted(EasyMP4Tags.Set.keys())
    for v in range(1, len(actualKeys)):
        
        try:
            tag = ''.join(random.choice(letters) for i in range(9))
            media_file[actualKeys[v]] = tag
        except:
            tag = str(random.randint(0, 4))
            media_file[actualKeys[v]] = tag
    
    return media_file

def changeMetaData(mfile):
    with open(mfile, 'r+b') as file:
        media_file = mutagen.File(file, easy=True)
        media_file = spoofKeys(media_file)
        media_file.save(file)

def randomDuration(videoD, audioD):
    rndInt = random.uniform(videoD, audioD - videoD)

    if random.randint(0, 1) == 0:
        return [rndInt - videoD, rndInt]
    else:
        return [rndInt, rndInt + videoD]

def unique(config_data):
    global letters, videos, background

    try:
        videoName = ''.join(random.choice(letters) for i in range(15))
        videopath = random.choice(videos)

        brightness = random.uniform(float(config_data['brightness_min']), float(config_data['brightness_max']))
        generatedSpeed = random.uniform(float(config_data['speed_min']), float(config_data['speed_max']))
        contrast = random.uniform(float(config_data['contrast_min']), float(config_data['contrast_max']))
        gamma = random.uniform(float(config_data['gamma_min']), float(config_data['gamma_max']))
        songVolume = random.uniform(float(config_data['audio_volume_min']), float(config_data['audio_volume_max']))

        clip = VideoFileClip(f"{config_data['folderInput']}\\" + videopath)

        clip = clip.speedx(generatedSpeed)

        NOISE = f"{config_data['folderBackground']}\\{random.choice(background)}"
        audioclip = AudioFileClip(NOISE).fx(afx.volumex, songVolume)
        video_duration = (clip.duration)
        audio_duration = (audioclip.duration)

        rndDuration = randomDuration(int(video_duration), int(audio_duration))

        print(f"Song: {NOISE}\nVolume: {round(songVolume, 3)}\nDuration: from {round(rndDuration[0], 3)} seconds to {round(rndDuration[1], 3)} seconds\nVideo Brightness: {brightness}\nVideo speed: {generatedSpeed}\nVideo Contrast {contrast}\nVideo Gamma: {gamma}")

        audioclip = audioclip.subclip(rndDuration[0], rndDuration[1])
        new_audioclip = CompositeAudioClip([clip.audio, audioclip])
        clip.audio = new_audioclip

        clip = clip.fx(vfx.colorx, brightness).fx(vfx.lum_contrast, contrast, contrast, contrast).fx(vfx.gamma_corr, gamma)
        print("Video is rendering..")
        final_clip = concatenate_videoclips([clip])
        final_clip.write_videofile(f"{config_data['folderTemp']}\\{videoName}.mp4", codec='libx264', preset='ultrafast', logger=None)

        changeMetaData(f"{config_data['folderTemp']}\\{videoName}.mp4")

        shutil.move(f"{config_data['folderTemp']}\\{videoName}.mp4", f"{config_data['folderOutput']}\\{videoName}.mp4")
        print("Done")
    except Exception as e:
        print(str(e))
        try:
            os.remove(f"{config_data['folderTemp']}\\{videoName}.mp4")
        except:
            pass

def removeAll(folder_path):
    file_list = os.listdir(folder_path)
    
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        try:
            os.remove(file_path)
        except Exception as e:
            pass
   
def main():
    global videos, background
    configfile = input("Enter name of config file: (Press Enter if config.json) ")
    if configfile == "": configfile = "config.json"
    with open(configfile, 'r') as file:
        config_data = json.load(file)
            
        required_parameters = ['videos', 'folderInput', 'folderOutput', 'folderBackground', 'folderTemp', 'brightness_min', 'brightness_max', 'speed_min', 'speed_max', 'contrast_min', 'contrast_max', 'gamma_min', 'gamma_max', 'audio_volume_min', 'audio_volume_max']
        if all(param in config_data for param in required_parameters):
            print("Configuration is valid.")
        else:
            print("Invalid configuration. Please make sure all required parameters are present.")

    tempFiles = os.getcwd()
    for item in tempFiles:
        if item.endswith(".mp3"):
            os.remove(os.path.join(dir_name, item))

    videos = os.listdir(config_data["folderInput"])
    background = os.listdir(config_data["folderBackground"])
    removeAll(config_data["folderTemp"])

    for x in range(0, int(config_data["videos"])):
        print(f"{str(x)}/{config_data['videos']}")
        unique(config_data)

if __name__ == "__main__":
    main()