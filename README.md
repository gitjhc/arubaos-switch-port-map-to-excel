# arubaos-switch-python

This project uses the ArubaOS Switch API v4 to collect switch data and generate Excel reports.

## Simple Usage

1. Install the package in editable mode:

   ```bash
   pip install -e .
   ```

2. Add target switch IP addresses in `data/ip_list.py`.

3. Run the script:

   ```bash
   python run.py
   ```

4. If you want to change VLAN colors in the Excel output, register them in `tools/colors.py`.

## Output

This script generates separate Excel sheets for:

* PORT_MAP


## Source

Original GitHub repository: https://github.com/aruba/arubaos-switch-api-python

Original work by Aruba.
