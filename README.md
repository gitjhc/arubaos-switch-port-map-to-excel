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

* VLAN
* PORT
* VSF
* ROUTE

## How to run this code

There are different workflows covered in this repo under the `workflows/` directory. Before starting, ensure the switch REST API is enabled:

```bash
switch# rest-interface
```

In order to run these scripts, please complete the steps below:

1. Install virtual env. Make sure Python 3 is installed on the system.

   ```bash
   python3 -m venv switchenv
   ```

2. Activate the virtual env.

   ```bash
   source switchenv/bin/activate
   ```

3. Install all packages required from the requirements file.

   ```bash
   pip install -r /arubaos-switch-api-python/requirements.txt
   ```

4. Open the project `arubaos-switch-api-python` from an editor such as PyCharm.

5. Set the project interpreter to the new virtual env created in step 1.

6. Go to the corresponding data YAML file for each workflow and provide the correct switch IP and credentials.

7. Run the workflows from `arubaos-switch-api-python/workflows`, for example `base_provision.py`.


## Source

Original GitHub repository: https://github.com/aruba/arubaos-switch-api-python

Original work by Aruba.
