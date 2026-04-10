import urllib3
from aruba_rest.src import ip_static_route, loginOS, ports, vlan
from aruba_rest.src import vsf
from aruba_rest.tools.base_url import base_url
from aruba_rest.tools.mask_text import enterPasswd, enterId
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class PortMapCreator():
    def __init__(self):
        self.baseurl = None
        self.__id = None
        self.__passwd = None
        self.cookie_header = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('--logout--')
        self.logout()

    def set_ip(self, ip: str):
        self.baseurl = base_url(ip)

    def set_account(self):
        self.__id = enterId()
        self.__passwd = enterPasswd()

    def login(self):
        self.cookie_header = loginOS.login_os(
            self.baseurl, self.__id, self.__passwd)

    def logout(self):
        loginOS.logout(self.baseurl, self.cookie_header)

    def get_vlans(self) -> list:
        vlans = vlan.get_vlan(self.baseurl, self.cookie_header)
        if not isinstance(vlans, dict):
            return []

        vlan_list = []
        for vlan_item in vlans.get('vlan_element', []):
            if not isinstance(vlan_item, dict):
                continue
            vlan_list.append({
                'vlan_id': vlan_item.get('vlan_id', ''),
                'name': vlan_item.get('name', ''),
                'status': vlan_item.get('status', ''),
                'type': vlan_item.get('type', ''),
                'is_voice_enabled': vlan_item.get('is_voice_enabled', ''),
                'is_jumbo_enabled': vlan_item.get('is_jumbo_enabled', ''),
                'is_dsnoop_enabled': vlan_item.get('is_dsnoop_enabled', ''),
                'is_dhcp_server_enabled': vlan_item.get('is_dhcp_server_enabled', ''),
                'is_management_vlan': vlan_item.get('is_management_vlan', ''),
            })

        return vlan_list

    def get_ports(self) -> list:
        port_names = ports.get_all_ports_with_name(
            self.baseurl, self.cookie_header)
        port_vlans = ports.get_all_ports_with_vlan(
            self.baseurl, self.cookie_header)

        if not isinstance(port_names, dict) or not isinstance(port_vlans, dict):
            return []

        port_name_items = port_names.get('port_element', [])
        port_vlan_items = port_vlans.get('vlan_port_element', [])

        vlan_map = {
            item.get('port_id'): item.get('vlan_id')
            for item in port_vlan_items
            if item.get('port_mode') == 'POM_UNTAGGED'
        }

        port_list = []
        for port_item in port_name_items:
            if not isinstance(port_item, dict):
                continue

            p_id = port_item.get('id', '')

            port_list.append({
                'id': p_id,
                'name': port_item.get('name', ''),
                'vlan_id': vlan_map.get(p_id, ''),
                'is_enabled': port_item.get('is_port_enabled', ''),
                'is_port_up': port_item.get('is_port_up', ''),
            })
        return port_list

    def get_vsf_links(self) -> list:
        vsf_links = vsf.get_system_info(self.baseurl, self.cookie_header)
        if not isinstance(vsf_links, dict):
            return []

        vsf_list = []
        for item in vsf_links.get('vsf_member_system_info_element', []):
            if not isinstance(item, dict):
                continue
            vsf_list.append({
                'member_id': item.get('member_id', ''),
                'model': item.get('model', ''),
                'rom_version': item.get('rom_version', ''),
                'serial_num': item.get('serial_num', ''),
                'cpu_util': item.get('cpu_util', ''),
                'total_mem': item.get('total_mem', ''),
                'free_mem': item.get('free_mem', ''),
                'up_time': item.get('up_time', {}),
            })
        return vsf_list

    def get_routes(self) -> list:
        route = ip_static_route.get_ip_route(self.baseurl, self.cookie_header)
        if route is None or not hasattr(route, 'json'):
            return []

        route_payload = route.json()
        route_list = []

        for route_item in route_payload.get('ip_route_element', []):
            if not isinstance(route_item, dict):
                continue

            destination = route_item.get('destination', {})
            mask = route_item.get('mask', {})
            gateway = route_item.get('gateway', {})

            route_list.append({
                'id': route_item.get('id', ''),
                'destination': destination.get('octets', '') if isinstance(destination, dict) else destination,
                'mask': mask.get('octets', '') if isinstance(mask, dict) else mask,
                'ip_route_mode': route_item.get('ip_route_mode', ''),
                'gateway': gateway.get('octets', '') if isinstance(gateway, dict) else gateway,
                'metric': route_item.get('metric', ''),
                'distance': route_item.get('distance', ''),
                'name': route_item.get('name', ''),
            })

        return route_list
