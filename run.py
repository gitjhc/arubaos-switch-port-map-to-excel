import aruba_rest.workflows.create_port_map.create_port_map as create_port_map
from aruba_rest.workflows.create_port_map.create_port_map_excel import PortMapToExcel
from ip_list import ip_list as SetIP



ip_list = SetIP()


def main():
    with create_port_map.PortMapCreator() as port_map_creator:
        port_map_creator.set_account()
        for ip in ip_list:
            port_map_creator.set_ip(ip)
            port_map_creator.login()

            vlan_map = port_map_creator.get_vlans()
            port_map = port_map_creator.get_ports()
            vsf_map = port_map_creator.get_vsf_links()
            route_map = port_map_creator.get_routes()

            with PortMapToExcel(file_path=f'./port_map({ip}).xlsx') as excel_creator:
                excel_creator.vlan_map_excel(vlan_map=vlan_map)
                excel_creator.port_map_excel(port_map=port_map, header_type='is_port_up') # header_type: 'is_enabled' or 'is_port_up'
                excel_creator.vsf_map_excel(vsf_map=vsf_map)
                excel_creator.route_map_excel(route_map=route_map)


if __name__ == "__main__":
    main()
