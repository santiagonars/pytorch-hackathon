#!/usr/bin/env bash
mkdir coco
cd coco/

wget http://images.cocodataset.org/zips/train2017.zip
wget http://images.cocodataset.org/zips/val2017.zip
wget http://images.cocodataset.org/zips/test2017.zip

unzip train2017.zip
unzip val2017.zip
unzip test2017.zip

rm train2017.zip
rm val2017.zip

mkdir images
mv train2017 images/
mv val2017 images/

wget http://images.cocodataset.org/annotations/annotations_trainval2017.zip
unzip annotations_trainval2017.zip

wget http://images.cocodataset.org/annotations/stuff_annotations_trainval2017.zip
unzip stuff_annotations_trainval2017.zip

rm annotations_trainval2017.zip
rm stuff_annotations_trainval2017.zip
