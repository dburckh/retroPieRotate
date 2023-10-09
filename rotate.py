import sys
import os

ES_SETTINGS_PATH = '/opt/retropie/configs/all/emulationstation/es_settings.cfg'
RETRO_CONFIG_PATH = '/opt/retropie/configs/all/retroarch.cfg'
# https://github.com/batocera-linux/batocera-emulationstation/blob/master/es-app/src/main.cpp
ES_SCREEN_ROTATE_PREFIX = '<int name="ScreenRotate" '
ES_SCREEN_WIDTH_PREFIX = '<int name="ScreenWidth" '
ES_SCREEN_HEIGHT_PREFIX = '<int name="ScreenHeight" '
VALUE_PREFIX = 'value="'
VALUE_POSTFIX = '" />\n'
VIDEO_ROTATION = 'video_rotation'
ASPECT_RATIO_INDEX = 'aspect_ratio_index'
ASPECT_RATIO_INDEX_0 = ASPECT_RATIO_INDEX + ' = "0"\n'

ROTATIONS = ['0', '1', '2', '3']


def read_lines(path):
    with open(path, "r") as file:
        return file.readlines()


def write_lines(path, lines):
    with open(path, "w") as file:
        file.writelines(lines)


def update_lines(lines, replace_dict):
    """
    Update the lines passed on the dictionary
    If a given line startswith() the key of the dict it will be updated to the value of the dict entry
    dict entries with values of None will be removed
    :param lines: a List of lines
    :param replace_dict: a dictionary of replacement values
    :return true if the lines were updated
    """
    i = 0
    end = len(lines)
    updated = False
    while i < end:
        line = lines[i]
        for key in replace_dict.keys():
            if line.startswith(key):
                value = replace_dict[key]
                if value is None:
                    # Counteract the index increase because we deleted an i
                    lines.pop(i)
                    end -= 1
                    i -= 1
                    updated = True
                else:
                    if lines[i] != value:
                        lines[i] = value
                        updated = True
                del replace_dict[key]
                break
        i += 1

    # Add anything we didn't update
    for value in replace_dict.values():
        if value is not None:
            lines.append(value)
            updated = True
    return updated


def usage():
    print('Usage ', sys.argv[0], ' [0|1|2|3]')
    sys.exit(-1)


def rotate(rotation):
    try:
        ROTATIONS.index(rotation)
    except ValueError:
        return -1

    es_settings_lines = read_lines(ES_SETTINGS_PATH)
    if rotation == '0':
        es_dict = {
            ES_SCREEN_ROTATE_PREFIX: None,
            ES_SCREEN_WIDTH_PREFIX: None,
            ES_SCREEN_HEIGHT_PREFIX: None
        }
    else:
        # Read the resolution from the frame buffer. Format: "<width>,<height>"
        with open('/sys/class/graphics/fb0/virtual_size', "r") as file:
            resolution = file.readline().strip('\n')
        width, height = resolution.split(',')
        es_dict = {
            # Retropie's 90/270 rotations are the opposite of ES's
            ES_SCREEN_ROTATE_PREFIX: ES_SCREEN_ROTATE_PREFIX + VALUE_PREFIX + str(4 - int(rotation)) + VALUE_POSTFIX,
            # Transpose the width and height because we are rotated
            ES_SCREEN_WIDTH_PREFIX: ES_SCREEN_WIDTH_PREFIX + VALUE_PREFIX + height + VALUE_POSTFIX,
            ES_SCREEN_HEIGHT_PREFIX: ES_SCREEN_HEIGHT_PREFIX + VALUE_PREFIX + width + VALUE_POSTFIX
        }

    if not update_lines(es_settings_lines, es_dict):
        print("No updates")
        return 0

    write_lines(ES_SETTINGS_PATH, es_settings_lines)

    retro_config_lines = read_lines(RETRO_CONFIG_PATH)

    retro_dict = {
        VIDEO_ROTATION: VIDEO_ROTATION + ' = "' + rotation + '"\n',
        ASPECT_RATIO_INDEX: None if rotation == '0' or rotation == '2' else ASPECT_RATIO_INDEX_0
    }
    update_lines(retro_config_lines, retro_dict)
    write_lines(RETRO_CONFIG_PATH, retro_config_lines)

    # touching this file causes emulationstation to restart on exit
    open('/tmp/es-restart', 'a').close()

    os.system('kill $(pidof emulationstation)')
    return 0


if __name__ == '__main__':
    if len(sys.argv) != 2 or rotate(sys.argv[1]) < 0:
        usage()
