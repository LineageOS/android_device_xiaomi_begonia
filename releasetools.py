# Copyright (C) 2009 The Android Open Source Project
# Copyright (C) 2019 The Mokee Open Source Project
# Copyright (C) 2019-2020 The LineageOS Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import common


def FullOTA_InstallEnd(info):
    OTA_InstallEnd(info, False)
    Firmware_Images(info, False)


def IncrementalOTA_InstallEnd(info):
    OTA_InstallEnd(info, True)
    Firmware_Images(info, True)


def AddImage(info, basename, dest, incremental, firmware):
    name = basename
    if incremental:
        input_zip = info.source_zip
    else:
        input_zip = info.input_zip
    if firmware:
        data = input_zip.read("RADIO/" + basename)
    else:
        data = input_zip.read("IMAGES/" + basename)
    common.ZipWriteStr(info.output_zip, name, data)
    info.script.Print("Patching {} image unconditionally...".format(dest.split('/')[-1]))
    info.script.AppendExtra('package_extract_file("%s", "%s");' % (name, dest))


def OTA_InstallEnd(info, incremental):
    AddImage(info, "vbmeta.img", "/dev/block/by-name/vbmeta", incremental, False)
    AddImage(info, "dtbo.img", "/dev/block/by-name/dtbo", incremental, False)

def Firmware_Images(info, incremental):
    """
    Adds the firmware files from $(INTERNAL_OTA_PACKAGE_TARGET) into the $(LINEAGE_TARGET_PACKAGE).
    """
    partition_list = ["lk1", "lk2", "sda", "sdb", "audio_dsp", "cam_vpu1", "cam_vpu2", "cam_vpu3", "gz1", "gz2", "md1img", "oem_misc1", "scp1", "scp2", "spmfw", "sspm_1", "sspm_2", "tee1", "tee2",]
    for partition in partition_list:
        AddImage(info, "{}.img".format(partition), "/dev/block/by-name/{}".format(partition), incremental, True)
