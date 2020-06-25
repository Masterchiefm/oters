#!/bin/bash
file=$1

rm -rf extract
rm -rf extract/DEBIAN
rm -rf build

mkdir extract
mkdir extract/DEBIAN
mkdir build

echo $file
dpkg -X $file extract/
dpkg -e $file extract/DEBIAN/ 
echo 请修改文件
read a
dpkg-deb -b extract/ build/

echo 打包完成
