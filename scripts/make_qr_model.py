#!/usr/bin/env python3
import os
import sys

import qrcode


def words():
    ''' Return list of words for which to make QR code Gazebo models. '''
    if len(sys.argv) < 2:
        print('Usage: ./make_qr_model.py word1 [word2 ...]')
        sys.exit(1)
    return sys.argv[1:]


def make_qr_code(word):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    )
    qr.add_data(word)
    qr.make(fit=True)
    img = qr.make_image()
    path = 'qr_{}/{}.png'.format(word, word)
    img.save(path)


def make_qr_mesh(word):
    # modify the collada data file to take the texture from the newly generated
    # QR code image
    with open('model_template/qr.dae') as f:
        data = f.read()
    data = data.replace('{file}', word + '.png')
    path = 'qr_{}/{}.dae'.format(word, word)
    with open(path, 'w') as f:
        f.write(data)


def make_gazebo_config(word):
    # write SDF file
    with open('model_template/model.sdf') as f:
        data = f.read()
    data = data.replace('{name}', word)
    path = 'qr_{}/model.sdf'.format(word)
    with open(path, 'w') as f:
        f.write(data)

    # write config file
    with open('model_template/model.config') as f:
        data = f.read()
    data = data.replace('{name}', word)
    path = 'qr_{}/model.config'.format(word)
    with open(path, 'w') as f:
        f.write(data)


def main():
    for word in words():
        os.mkdir('qr_' + word)
        make_qr_code(word)
        make_qr_mesh(word)
        make_gazebo_config(word)


if __name__ == '__main__':
    main()
