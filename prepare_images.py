'''
Script para separar las imágenes en carpetas train y val.
'''

# Librerías a utilizar.
import json
import argparse
import os
import shutil
import sys

def image_cp(args):
    with open(args.data_path,'r') as f:
        data = json.load(f)
        imgs_idxs = set()
        not_in_images = []
        for question in data.values():
            imgs_idxs.add(int(question['imageId']))

        if not os.path.isdir(args.new_img_dir):
            os.mkdir(args.new_img_dir)

        for img_idx in imgs_idxs:
            old_img_path = f"{args.old_img_dir}/{img_idx}.jpg"
            new_img_path = f"{args.new_img_dir}/{img_idx}.jpg"
            try:
                shutil.copyfile(old_img_path,new_img_path)
            except Exception as e:
                print(e)
                not_in_images.append(str(img_idx))
                
        with open(args.missing_img_log,'w+') as f:
            f.write('\n'.join(not_in_images))
            #os.rename(old_img_path,new_img_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--old_img_dir', required=True)
    parser.add_argument('--new_img_dir', required=True)
    parser.add_argument('--data_path', required=True)
    parser.add_argument('--missing_img_log', required=True)
    
    args = parser.parse_args()
    image_cp(args)
