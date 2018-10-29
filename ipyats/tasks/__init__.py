from genie.abstract import Lookup # noqa
from genie.libs import ops, conf # noqa
from genie.utils.diff import Diff # noqa

def compare_stuff(obj1, obj2):
    diff = Diff(obj1, obj2)
    diff.findDiff()
    print(diff)


def get_interface_info(dev):
    """
    returns parsed and normalized interface counters
    """
    if not dev.is_connected():
        dev.connect()
    abstract = Lookup.from_device(dev)
    # Find the Interface Parsers for this device
    # 1) Directory must exists in genie.libs.ops.<feature>
    # 2) Then abstraction will kick in to find the right one
    # 3) The directory syntax is <feature>.<feature.<Feature>
    #    Where the class is capitalized but the directory/files arent.
    intf = abstract.ops.interface.interface.Interface(dev)
    intf.learn()
    return intf.info


def get_routing_table(dev):
    """
    returns a parsed and normalized routing table
    """
    if not dev.is_connected():
        dev.connect()
    abstract = Lookup.from_device(dev)
    # The directory syntax is <feature>.<feature.<Feature>
    routing = abstract.ops.routing.routing.Routing(dev)
    routing.learn()
    return routing.info


def configure_l3_interface(dev, name, ip, mask, remove=False, apply=True):
    """
    creates an l3 interface `name` on `dev` with ip `ip` and mask `mask`

    booleans can also be passed

    configure_l3_interface(... apply=True) (default)
    configure_l3_interface(... remove=True)

    """
    from genie.conf.base import Interface
    if not dev.is_connected():
        dev.connect()
    if name not in dev.interfaces:
        interface = Interface(device=dev, name=name)
    else:
        interface = dev.interfaces[intf]
    # this is a bug....shouldn't have to do this...
    # Add some configuration
    interface.switchport_enable = False
    interface.ipv4 = ip
    interface.ipv4.netmask = mask

    if apply and not remove:
        print("\n")
        print("******************************************************")
        print("Configuring interface {} on {}  ".format(dev.name, interface.name))
        print("******************************************************")
        interface.build_config(apply=apply)
    if remove:
        print("\n")
        print("******************************************************")
        print("Removing interface {} on {}  ".format(dev.name, interface.name))
        print("******************************************************")
        interface.build_unconfig(apply=apply)
    return interface


def learn(feature, dev):
    if not dev.is_connected():
        dev.connect()
    abstract = Lookup.from_device(dev)
    # Find the Interface Parsers for this device
    # 1) Directory must exists in genie.libs.ops.<feature>
    # 2) Then abstraction will kick in to find the right one
    # 3) The directory syntax is <feature>.<feature.<Feature>
    #    Where the class is capitalized but the directory/files arent.
    # e.g interface.interface.Interface

    class_name = '.'.join(['abstract.ops',
                           feature.lower(),
                           feature.lower(),
                           feature.title()])

    try:
        feature_details = eval(class_name)(dev)
    except LookupError:
        raise NotImplementedError("Feature is not implemented for this OS")

    feature_details.learn()
    if hasattr(feature_details, 'info'):
        return feature_details.info
    else:
        return feature_details


def get_platform_info(dev):
    return learn('platform', dev)


def get_bgp_info(dev):
    return learn('bgp', dev)


def get_ospf_info(dev):
    return learn('ospf', dev)


def get_hsrp_info(dev):
    return learn('hsrp', dev)


def get_igmp_info(dev):
    return learn('igmp', dev)


def get_stp_info(dev):
    return learn('stp', dev)

def get_vlan_info(dev):
    return learn('vlan', dev)

def get_vrf_info(dev):
    return learn('vrf', dev)



# TODO: Check with team
# def get_vxlan_info(dev):
#     return learn('vxlan', dev)


def get_multicast_info(dev):
    return learn('mcast', dev)
