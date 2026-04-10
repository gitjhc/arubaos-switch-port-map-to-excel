from workflows.create_port_map.create_port_map_excel import PortMapToExcel
from workflows.create_port_map.create_port_map import PortMapCreator
from data.ip_list import ip_list


def main():
    with PortMapCreator() as port_map_creator:
        port_map_creator.set_account()
        for ip in ip_list():
            port_map_creator.set_ip(ip)
            port_map_creator.login()

            vlan_map = port_map_creator.get_vlans()
            port_map = port_map_creator.get_ports()
            vsf_map = port_map_creator.get_vsf_links()
            route_map = port_map_creator.get_routes()

            with PortMapToExcel(file_path=f'./port_map({ip}).xlsx') as excel_creator:
                excel_creator.run(vlan_map=vlan_map, port_map=port_map, vsf_map=vsf_map, route_map=route_map)

if __name__ == "__main__":
    main()
    