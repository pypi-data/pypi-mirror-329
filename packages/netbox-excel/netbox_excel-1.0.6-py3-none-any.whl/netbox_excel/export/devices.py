from dcim.models import Device, DeviceType, DeviceBay

def get_device():
    devices = Device.objects.all()
    devices = devices.order_by('rack', '-position')
    return devices

def get_device_type_parent():
    device_type = DeviceType.objects.filter(subdevice_role='parent')
    return device_type

def get_devices_child(parentid):
    # get list bay
    result = [] 
    device = get_device_by_id(parentid)
    device_bays = DeviceBay.objects.filter(device=device).order_by('-name')
    for item_bay in device_bays:
        device_child = Device.objects.get(id = item_bay.installed_device_id)
        result.append(device_child)
    return result

def get_device_by_id(id):
    device = Device.objects.get(id=id)
    return device

# def get_device_bay(parent):
#     device_child = DeviceBay.objects.filter(parent_device = parent)
#     return device_child