import os
import subprocess

import logging
from string import join

log = logging.getLogger(__name__)

out_dir = os.path.join('static', 'images', 'generated')
target_size = 96    # Width/height of target gym icon in pixels


def get_gym_icon(team, level, raidlevel, pkm):
    init_image_dir()
    level = int(level)

    subject_lines = []
    badge_lines = []
    white_transparent = "\"rgba(255, 255, 255, 0.7)\""
    black_transparent = "\"rgba(0, 0, 0, 0.7)\""
    if pkm:
        out_filename = os.path.join(out_dir, "{}_{}_{}.png".format(team, level, pkm))
        subject_lines = draw_subject(os.path.join('static', 'icons', '{}.png'.format(pkm)), float(2) / 3)
        badge_lines.extend(draw_badge(75, 20, 15, white_transparent, "black", raidlevel))
        if level > 0:
            badge_lines.extend(draw_badge(75, 76, 15, black_transparent, "white", level))
    elif raidlevel:
        raidlevel = int(raidlevel)
        egg_name = "legendary" if raidlevel == 5 else ("rare" if raidlevel > 2 else "normal")
        out_filename = os.path.join(out_dir, "{}_{}_{}.png".format(team, level, egg_name))
        subject_lines = draw_subject(os.path.join('static', 'images', 'raid', 'egg_{}.png'.format(egg_name)), 0.5)
        badge_lines.extend(draw_badge(75, 20, 15, white_transparent, "black", raidlevel))
        if level > 0:
            badge_lines.extend(draw_badge(75, 76, 15, black_transparent, "white", level))
    elif level > 0:
        out_filename = os.path.join(out_dir, '{}_{}.png'.format(team, level))
        badge_lines.extend(draw_badge(75, 76, 15, black_transparent, "white", level))
    else:
        return os.path.join('static', 'images', 'gym', '{}.png'.format(team))

    if not os.path.isfile(out_filename):
        gym_image = os.path.join('static', 'images', 'gym', '{}.png'.format(team))
        font = os.path.join('static', 'Arial Black.ttf')
        cmd = 'convert {} {} -gravity center -font "{}" -pointsize 25 {} {}'.format(gym_image, join(subject_lines),
                                                                                    font, join(badge_lines),
                                                                                    out_filename)
        subprocess.call(cmd, shell=True)
    return out_filename


def draw_subject(image, scale):
    scaled_size = int(target_size * scale)
    lines = []
    lines.append(
        "-gravity north \( {} -resize {}x{} \( +clone -background black -shadow 80x3+5+5 \) +swap -background none -layers merge +repage \) -geometry +0+0 -composite".format(
            image, scaled_size, scaled_size))
    return lines


def draw_badge(x, y, r, fcol, tcol, text):
    lines = []
    lines.append('-fill {} -draw "circle {},{} {},{}"'.format(fcol, x, y, x+r, y))
    lines.append('-fill {} -draw \'text {},{} "{}"\''.format(tcol, x-48, y-49, text))
    return lines


def init_image_dir():
    if not os.path.isdir(out_dir):
        try:
            os.makedirs(out_dir)
        except OSError as exc:
            if not os.path.isdir(out_dir):
                raise
