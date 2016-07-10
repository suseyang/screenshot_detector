#!/usr/bin/en sh
if [ $# -ne 2 ]; then
    echo "Usage: \"./create_lmdb.sh path_to_save_lmdb image_dir\"";
    exit
fi

MY=$1
#IMG_DIR=/home/ydx/caffe/data/re/
IMG_DIR=$2

echo "Create train lmdb..."
rm -rf $MY/img_train_lmdb
build/tools/convert_imageset --shuffle \
    --resize_height=256 --resize_width=256 \
    $IMG_DIR $MY/train.txt $MY/img_train_lmdb

echo "Create test lmdb..."
rm -rf $MY/img_test_lmdb
build/tools/convert_imageset --shuffle \
    --resize_height=256 --resize_width=256 \
    $IMG_DIR $MY/test.txt $MY/img_test_lmdb

echo "All Done..."
