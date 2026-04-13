import xlsxwriter
import urllib3
from aruba_rest.tools.colors import get_color

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class PortMapToExcel():

    def __init__(self, file_path='./port_map.xlsx'):
        self.file_path = file_path
        self.vlan_map = None
        self.port_map = None
        self.vsf_map = None
        self.route_map = None

        self.port_map_sheet = None

        self.current_row = 0
        self.vlan_color_match = {}

    def __enter__(self):
        self.start_excel()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.workbook is not None:
            self.end_excel(self.workbook)

    def start_excel(self):
        print('Creating Excel file to : ', self.file_path)
        self.workbook = xlsxwriter.Workbook(self.file_path)
        self.port_map_sheet = self.workbook.add_worksheet('PORT_MAP')
        return

    def end_excel(self, workbook):
        print(f'Excel file saved to: {self.file_path}')
        workbook.close()

    def _excel_format(self, bold: bool = False, color: str | None = None) -> object:
        format = self.workbook.add_format({
            "bold": bold,
            "align": 'center',
            "valign": 'vcenter',
            "border": 1,
        })
        if color:
            format.set_bg_color(color)
        return format

    def vlan_map_excel(self, vlan_map: list):
        worksheet = self.port_map_sheet

        # header
        worksheet.write(self.current_row, 0,  'VLAN MAP',
                        self._excel_format(bold=True, color='#D9EAD3'))
        self.current_row += 1

        worksheet.write(self.current_row, 0, 'VLAN ID',
                        self._excel_format(bold=True, color='#D9EAD3'))
        worksheet.write(self.current_row, 1, 'Name',
                        self._excel_format(bold=True, color='#D9EAD3'))
        self.current_row += 1

        # values
        for idx, vlan_item in enumerate(vlan_map):
            worksheet.write(self.current_row, 0, vlan_item.get(
                'vlan_id', ''), self._excel_format(color=get_color(idx)))
            worksheet.write(self.current_row, 1, vlan_item.get(
                'name', ''), self._excel_format(color=get_color(idx)))
            self.vlan_color_match[vlan_item.get('vlan_id', '')] = {
                'color': get_color(idx), 'vlan_name': vlan_item.get('name', '')}
            self.current_row += 1

        self.current_row += 2

    def vsf_map_excel(self, vsf_map):
        worksheet = self.port_map_sheet

        # header
        worksheet.write(self.current_row, 0, 'VSF MAP',
                        self._excel_format(bold=True, color='#D9EAD3'))
        self.current_row += 1

        worksheet.write(self.current_row, 0, '#',
                        self._excel_format(bold=True, color='#D9EAD3'))
        worksheet.write(self.current_row, 1, 'Model',
                        self._excel_format(bold=True, color='#D9EAD3'))
        worksheet.write(self.current_row, 2, 'ROM Version',
                        self._excel_format(bold=True, color='#D9EAD3'))
        worksheet.write(self.current_row, 3, 'Serial Number',
                        self._excel_format(bold=True, color='#D9EAD3'))
        worksheet.write(self.current_row, 4, 'CPU Utilization',
                        self._excel_format(bold=True, color='#D9EAD3'))
        worksheet.write(self.current_row, 5, 'Total Memory',
                        self._excel_format(bold=True, color='#D9EAD3'))
        worksheet.write(self.current_row, 6, 'Free Memory',
                        self._excel_format(bold=True, color='#D9EAD3'))
        worksheet.write(self.current_row, 7, 'Up Time',
                        self._excel_format(bold=True, color='#D9EAD3'))
        self.current_row += 1

        # values
        for vsf_item in vsf_map:
            worksheet.write(self.current_row, 0, vsf_item.get(
                'member_id', ''), self._excel_format())
            worksheet.write(self.current_row, 1, vsf_item.get(
                'model', ''), self._excel_format())
            worksheet.write(self.current_row, 2, vsf_item.get(
                'rom_version', ''), self._excel_format())
            worksheet.write(self.current_row, 3, vsf_item.get(
                'serial_num', ''), self._excel_format())
            worksheet.write(self.current_row, 4, vsf_item.get(
                'cpu_util', ''), self._excel_format())
            worksheet.write(self.current_row, 5, vsf_item.get(
                'total_mem', ''), self._excel_format())
            worksheet.write(self.current_row, 6, vsf_item.get(
                'free_mem', ''), self._excel_format())
            up_time = f"{vsf_item.get('up_time', {}).get('days', '')} days {vsf_item.get('up_time', {}).get('hours', '')} hours {vsf_item.get('up_time', {}).get('minutes', '')} minutes"
            worksheet.write(self.current_row, 7, up_time, self._excel_format())
            self.current_row += 1
        self.current_row += 2

    def route_map_excel(self, route_map):
        worksheet = self.port_map_sheet

        # header
        worksheet.write(self.current_row, 0, 'ROUTE MAP',
                        self._excel_format(bold=True, color='#D9EAD3'))
        self.current_row += 1

        worksheet.write(self.current_row, 0, 'Gateway',
                        self._excel_format(bold=True, color='#D9EAD3'))
        worksheet.write(self.current_row, 1, 'Mask',
                        self._excel_format(bold=True, color='#D9EAD3'))
        self.current_row += 1

        # values
        for route_item in route_map:
            worksheet.write(self.current_row, 0, route_item.get(
                'gateway', ''), self._excel_format())
            worksheet.write(self.current_row, 1, route_item.get(
                'mask', ''), self._excel_format())
            self.current_row += 1

        self.current_row += 2

    def port_map_excel(self, port_map, header_type='is_enabled'):
        '''
        header_type: str = 'is_enabled' or 'is_port_up'
        '''

        worksheet = self.port_map_sheet

        if not self.vlan_color_match:
            print(
                'VLAN color match is not set. Please run vlan_map_excel first to set the color match for VLANs.')

        # header
        worksheet.write(self.current_row, 0, 'PORT MAP',
                        self._excel_format(bold=True, color='#D9EAD3'))
        self.current_row += 1

        # values
        col_num = 0
        for idx, port_item in enumerate(port_map):
            if port_item['id'].split('/')[0] != port_map[idx-1]['id'].split('/')[0]:
                if idx != 0:
                    self.current_row += 3
                    col_num = 0

            if port_item.get(header_type, False):
                worksheet.write(self.current_row, col_num,
                                port_item.get('id', ''), self._excel_format(color='#D9EAD3'))
            else:
                worksheet.write(self.current_row, col_num,
                                port_item.get('id', ''), self._excel_format())

            color = self.vlan_color_match.get(port_item.get('vlan_id', ''), {})
            worksheet.write(
                self.current_row+1,
                col_num,
                color.get('vlan_name', None),
                self._excel_format(color=color.get('color'))
            )
            worksheet.write(
                self.current_row+2,
                col_num, port_item.get('name', ''),
                self._excel_format(color=color.get('color'))
            )
            col_num += 1
        self.current_row += 5
