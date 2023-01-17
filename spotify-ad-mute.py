"""
Title: spotify-ad-mute
Description: This is a program to mute spotify whenever an ad appears.
Author: Marco A. Barreto - marcoagbarreto
Version: 13-Jan-2023
"""

try:
    import os
    import sys
    from pyautogui import locateCenterOnScreen as pyautogui_locateCenterOnScreen, click as pyautogui_click
    import time
    from pick import pick
    from threading import Thread as threading_Thread
except ImportError as details:
    print("-E- Couldn't import module, try pip install 'module'")
    raise details


# function needed for auto-py-to-exe to find relative path when one-file is used.
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def append_ads(folder_ad='ads'):
    ads = []
    for image in os.listdir(folder_ad):
        if image.endswith(".png") or image.endswith(".jpg") or image.endswith(".jpeg"):
            ads.append(folder_ad + '/' + image)
    return ads


image_volume = resource_path('volume/volume.png')
image_mute = resource_path('volume/mute.png')
image_ad = append_ads(resource_path('ads'))


class MuteAd(threading_Thread):
    def __init__(self):
        super(MuteAd, self).__init__()
        self.program_running = True
        self.running = False

    def run(self):
        while self.program_running:
            while self.running:
                xy_ad = check_for_ad(image_ad)
                if xy_ad is not None:
                    xy_volume = locate_image(image_volume)
                    if xy_volume is not None:
                        pyautogui_click(x=xy_volume[0], y=xy_volume[1], clicks=1, button='left')
                    time.sleep(0.5)
                else:
                    xy_mute = locate_image(image_mute)
                    if xy_mute is not None:
                        pyautogui_click(x=xy_mute[0], y=xy_mute[1], clicks=1, button='left')
                    time.sleep(0.5)


def locate_image(image):
    return pyautogui_locateCenterOnScreen(image, grayscale=True, confidence=0.9)


def check_for_ad(ads):
    for ad in ads:
        xy_ad = locate_image(ad)
        if xy_ad is not None:
            return xy_ad


def show_menu(mute_ad):
    title = f'spotify-ad-mute: (({mute_ad.running}))'
    options = ['Run', 'Stop']
    option, index = pick(options, title)

    if index == 0:
        mute_ad.running = True
    else:
        mute_ad.running = False


def main():
    # Set terminal size to optimal size
    os.system('mode con cols=30 lines=7')

    # Start program
    mute_ad = MuteAd()
    mute_ad.start()

    while True:
        # show menu
        show_menu(mute_ad)


if __name__ == "__main__":
    main()
