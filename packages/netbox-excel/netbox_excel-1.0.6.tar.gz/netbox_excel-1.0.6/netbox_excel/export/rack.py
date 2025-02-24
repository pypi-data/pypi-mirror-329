from dcim.models import Rack

def get_rack_have_device():
    racks = Rack.objects.all()
    racks = racks.order_by('name')
    return racks