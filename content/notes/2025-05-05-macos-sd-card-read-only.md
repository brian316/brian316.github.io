+++
title = "macOS SD Card Read Only Issues"
+++

[tl;dr](#solution)

## Problem

I bought a cheap amazon basics micro sd card and inserted it with the adapter into my macbook M1. Thinking things would go smoothly (somehow they never do) I only had read access to the card. I tried everything from disk utilities First Aid, formatting to exFAT and MS-DOS (FAT), and dangerously typing commands from the interwebs into my terminal... cough, of course I have common sense enough to know what they are doing. Nothing worked. It was simply stuck on readonly mode. I had given up hope and started my amazon return thinking I had a defective device maybe even a fake sd card, but then I used a known working sd card and same issue! I had to dig deeper to find my solution.


## System Check

Insert your sd card and check the volume info
```bash
diskutil info /Volumes/YOUR_CARD_NAME
```

look for this line. If present you have the issue!
```shell
Volume Read-Only:          Yes (read-only mount flag set)
```

<!-- [script](/scripts/sdcard_fix.sh?view=true) -->

Use macbooks `Disk Utility` to erase/format your sd card to the desired format and take note of that format. For me I needed to use `msdos` format so it can be read my 3d printer find (Creality Ender-3 v2 Neo).

## Solution

Now for the hack! We are going to manually mount the disk as a read/write volume.

```bash
# get volume device name
diskutil info /Volumes/SDCARD |grep /dev
```

if using `exfat` then replace `msdos` with `exfat`
```bash
sudo umount /Volumes/SDCARD
sudo mkdir -p /Volumes/SDCARD
sudo mount -t msdos -o rw /dev/disk6s1 /Volumes/SDCARD
```

## Conclusion

Like I said this is a hack so everytime you insert your sdcard you'll have to run the set of commands. Not ideal, but we are programmers or maybe just script kiddies so just create a script to run whenever you need it. Hopefully I figure out the issue in the future and I update this soon. 

~ Maybe it's my machine!