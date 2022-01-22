#!/bin/bash

rsync -rvulP --exclude '.DS_Store' --ignore-errors --size-only --log-file=copy.log --cache "/Volumes/External Drive/Documents/" "/Volumes/iboysoft_ntfs_disk3s2_/Documents/"
