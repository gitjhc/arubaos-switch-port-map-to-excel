from workflows.create_port_map.create_port_map_excel import PortMapToExcel
from workflows.create_port_map.create_port_map import PortMapCreator

def main():
    with PortMapCreator(ip='172.31.20.13') as port_map_creator:
        vlan_map = port_map_creator.get_vlans()
        port_map = port_map_creator.get_ports()
        vsf_map = port_map_creator.get_vsf_links()
        route_map = port_map_creator.get_routes()

        with PortMapToExcel(file_path='./port_map.xlsx') as excel_creator:
            excel_creator.vlan_map_excel(vlan_map=vlan_map)
            excel_creator.port_map_excel(port_map=port_map)
            excel_creator.vsf_map_excel(vsf_map=vsf_map)
            excel_creator.route_map_excel(route_map=route_map)

if __name__ == "__main__":
    main()