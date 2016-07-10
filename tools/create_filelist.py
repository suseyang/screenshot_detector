#coding:utf8
import os
from os import listdir
from os.path import isfile, join
import sys
import shutil

img_exts = ['jpg', 'jpeg', 'png']
train_num = 4000
test_num = 1000

def is_img(fn):
    if fn.split('.')[-1] in img_exts:
        return True
    return False

def prefix_filename(path, prefix):
    for f in get_files(path):
        if f[:2] != prefix:
            os.rename(join(path, f), join(path, prefix+f))
        else:
            continue

def get_files(path):
    files = [f for f in listdir(path) if (isfile(join(path, f)) and is_img(f))]
    return files

def make_dir_if_necessary(path):
    dtrain = join(path, 'train')
    dtest = join(path, 'test')
    if not os.path.exists(dtrain):
        os.makedirs(dtrain)
    if not os.path.exists(dtest):
        os.makedirs(dtest)

def count_files_number(path):
    ssn = get_files(join(path, 'screenshot'))
    nsn = get_files(join(path, 'notscreenshot'))
    if len(ssn) < 5000 or len(nsn) < 5000:
        print 'files less than 5000, screenshot = ', len(ssn), ' not screenshot = ', len(nsn)
        print 'program exit now without executing'
        sys.exit()

def gen_file_list(path, prefix):
    global train_num
    global test_num
    val = ''
    image_path = ''
    if prefix == 'ss':
        img_path = join(path, 'screenshot')
        val = ' 1\n'
    elif prefix == 'ns':
        img_path = join(path, 'notscreenshot')
        val = ' 0\n'
    else:
        print 'prefix wrong, ', prefix
        sys.exit()

    print img_path, ' get files: ', get_files(img_path)
    #if len(files) < 5000:
    #    print image_path, ' only has ', len(files), ' files'
        #sys.exit()

    prefix_filename(img_path, prefix)
    files = get_files(img_path)

    with open('train.txt', 'ab') as train_label:
        with open('test.txt', 'ab') as test_label:
            for img in files:
                if train_num > 0:
                    train_label.write(img + val)
                    shutil.move(os.path.join(img_path, img), os.path.join(path, 'train', img))
                    train_num -= 1
                elif test_num > 0:
                    test_label.write(img + val)
                    shutil.move(os.path.join(img_path, img), os.path.join(path, 'test', img))
                    test_num -= 1
                else:
                    break
    if train_num > 0 or test_num > 0:
        print 'need more files...'
        print prefix, ' required: train = ', train_num, ' test = ', test_num
    train_num = 4000
    test_num = 1000

def main():
    path = sys.argv[1]
    count_files_number(path)
    make_dir_if_necessary(path)

    gen_file_list(path, 'ss')
    gen_file_list(path, 'ns')

if __name__ == '__main__':
    print 'sys.argv = ', sys.argv
    if len(sys.argv) != 2:
        print 'Usage: python create_filelist.py path'
        sys.exit()
    main()
