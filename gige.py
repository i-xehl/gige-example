from harvesters.core import Harvester
from harvesters.core import DeviceInfo, NodeMap
from genicam.gentl import TimeoutException
import cv2

h = Harvester()

h.add_file("mvGenTLProducer.cti")

h.update()

print(h.device_info_list)
ia = h.create()
ia.remote_device.node_map.PixelFormat.value = 'RGB8Packed'
ia.remote_device.node_map.ExposureTimeRaw.value = 50771
ia.remote_device.node_map.GainRaw.value = 320
ia.remote_device.node_map.BlackLevelRaw.value = 0
ia.remote_device.node_map.AcquisitionMode.value = "Continuous"

print(DeviceInfo.search_keys)

ia.start()

while True:
    try:
        buffer = ia.try_fetch(timeout= 40)
        print(buffer)
        if buffer == None:
            continue
        img = buffer.payload.components[0].data
        img = img.reshape(buffer.payload.components[0].height, buffer.payload.components[0].width, 3)
        img_copy = img.copy()
        img_copy = cv2.cvtColor(img_copy, cv2.COLOR_BGR2RGB)
        cv2.imshow("win", img_copy)
        cv2.waitKey(1)
        buffer.queue()
    except TimeoutException as e:
        print(e)

