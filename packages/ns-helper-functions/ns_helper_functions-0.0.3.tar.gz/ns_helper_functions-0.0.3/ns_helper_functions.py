def create_menu():

    ReturnDict = {}

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--inventory_source",
        "-i",
        help="Source of the inventory. Valid options are nautobot, excel or nornir",
        # default="nautobot",
        type=str,
        choices=["excel", "nornir", "nautobot"],
        required=False,
    )

    parser.add_argument(
        "--nautobot_url", help="Nautobot url, for example http://localhost:8080", type=str, required=False
    )
    parser.add_argument(
        "--nautobot_token", help="Nautobot token", type=str, required=False)
    
    parser.add_argument(
        "--nautobot_filter_parameters_string", "-q", help="Nautobot query filter (in json format)", type=str, required=False)
    
    parser.add_argument(
        "--vault_url", help="Hashicorp vault url, for example http://localhost:8200", type=str, required=False
    )

    parser.add_argument(
        "--vault_token", help="Nautobot token", type=str, required=False
    )

    parser.add_argument(
        "--mode",
        help="Valid choices are dry_run, apply",
        type=str,
        choices=["dry_run", "apply"],
        required=False,
    )

    args = parser.parse_args()

    if not args.inventory_source:
        args.inventory_source = get_inventory_source()
    ReturnDict.update({"inventory_source": args.inventory_source})

    if args.inventory_source == "nautobot":
        if not args.nautobot_url:
            if os.environ.get('nautobot_url'):
                args.nautobot_url = os.environ.get('nautobot_url')
            else:
                args.nautobot_url = get_nautobot_url()
        ReturnDict.update({"nautobot_url": args.nautobot_url})

        if not args.nautobot_token:
            if os.environ.get('nautobot_token'):
                args.nautobot_token = os.environ.get('nautobot_token')
            else:
                args.nautobot_token = get_nautobot_token()
        ReturnDict.update({"nautobot_token": args.nautobot_token})

        if not args.nautobot_filter_parameters_string:
            if os.environ.get('nautobot_filter_parameters_string'):
                nautobot_filter_parameters_string = os.environ.get('nautobot_filter_parameters_string')
                nautobot_filter_parameters = json.loads(args.nautobot_filter_parameters_string)
            else:
                nautobot_filter_parameters= get_nautobot_query_filter_string()
            ReturnDict.update({"nautobot_filter_parameters": nautobot_filter_parameters})
        # nautobot_filter_parameters = {"location" : "Olympos"}
        ReturnDict.update({"nautobot_filter_parameters": nautobot_filter_parameters})
                
        if not args.vault_url:
            if os.environ.get('vault_url'):
                args.vault_url = os.environ.get('vault_url')
            else:
                args.vault_url = get_vault_url()
        ReturnDict.update({"vault_url": args.vault_url})

        if not args.vault_token:
            if os.environ.get('vault_token'):
                args.vault_token = os.environ.get('vault_token')
            else:
                args.vault_token = get_vault_token()
        ReturnDict.update({"vault_token": args.vault_token})

        if not args.mode:
            args.mode= get_dry_run()
            ReturnDict.update({"mode": args.mode})


    return ReturnDict


def frame(text, style_character='*'):
    line_len = []
    for line in text.split('\r\n'):
        line_len.append(len(line))
    max_len = max(line_len)
    frame_line = style_character * (max_len + 4)
    print(frame_line)
    for line in text.split('\r\n'):
        print(style_character+line.center(max_len+2)+style_character)
    print(frame_line)


def create_default_files_and_directories(files = [".env"], directories = ["_OUTPUT", "parameters"]):

    import os

    for directory in directories:
        if not os.path.exists(directory):
            os.mkdir(directory)

    for file in files:
        if not os.path.isfile(file):
            open(file, 'a').close()

    return None



def get_col_widths(dataframe):
    # First we find the maximum length of the index column   
    idx_max = max([len(str(s)) for s in dataframe.index.values] + [len(str(dataframe.index.name))])
    # Then, we concatenate this to the max of the lengths of column name and its values for each column, left to right
    ColumnLengthList = [idx_max] + [max([len(str(s)) for s in dataframe[col].values] + [len(col)]) for col in dataframe.columns]
    for index,length in enumerate(ColumnLengthList):
        if length < 12:
            ColumnLengthList[index] = 12
        
    return ColumnLengthList#[idx_max] + [max([len(str(s)) for s in dataframe[col].values] + [len(col)]) for col in dataframe.columns]


# Function used to break a list into a list of lists with a given number of elements
def chunks(l, n):
    # For item i in a range that is a length of l,
    for i in range(0, len(l), n):
        # Create an index range for l of n items:
        yield l[i:i+n]
        

def create_key_parameter_menu(folder,extension):
    
    import os

    KEYS = [f for f in os.listdir(folder) if f.endswith(extension)]
    KEYS.sort()     
    print ("The following Excel files were detected in your parameters file.\n")
    i=0
    for KEY in (KEYS):
        i=i+1
        print  ("["+str(i)+"]:",(KEY))
    while True:
        KEY = input("\r\nPlease input the number of the file you would like to use: ")

        if str(KEY).isdigit():
            KEY = int(KEY)
        if (KEY  in set(range(1,len(KEYS)+1))):
            break
        else:
            print ("Your entry is not valid. Please try again.\r\n")
            continue
    

    workbookname = KEYS[KEY-1]
    return workbookname


def get_workbook(default_folder):

    import openpyxl 
    import os

    forbiden_chars = ["<", ">", ":", "\"", "\\", "|", '?', "*"]
    extension = 'xlsx'
    #while True:
    while True:
        workbookfolder_raw = input(f"\nPlease enter the name of the excel workbook folder, press . to use the current folder or press enter to use the default {default_folder} folder: ")
        if workbookfolder_raw.strip() =="":
            workbookfolder=default_folder
            break
        elif (any(i in workbookfolder_raw.strip() for i in forbiden_chars)):
            print ("\r\nThe folder name contains forbiden characters")
            continue
        elif not os.path.exists(workbookfolder_raw.strip()):
            print ("\r\nThe folder you provided does not exist")
            continue
        else:
            workbookfolder=workbookfolder_raw.strip()
            break

    if workbookfolder == ".":
        print ("\r\nYou have chosen the current folder as your workbook folder.")
    else:
        print ("\r\nYou have chosen the" , workbookfolder , "folder as your workbook folder.")
    #
    print()

    workbookname = create_key_parameter_menu(workbookfolder,extension)
    
    workbookpath=workbookfolder+"/"+workbookname
    workbook = openpyxl.load_workbook(workbookpath, data_only=True)

    return workbook, workbookname, workbookfolder


def get_device_worksheet(workbook):
    
    worksheets=[]
    print ("\r\nYour workbook contains the following worksheets:\r\n")
    
    for worksheet in workbook.worksheets:
        worksheets.append(worksheet.title)
    i=0
    for worksheet in (worksheets):
        i=i+1
        print  ("["+str(i)+"]:",(worksheet))
    
    while True:
    
        deviceworksheet_number = input(f"\r\nPlease input the number of the device worksheet: ")
    
        if str(deviceworksheet_number).isdigit():
            deviceworksheet_number = int(deviceworksheet_number)
        if (deviceworksheet_number not in set(range(1,len(worksheets)+1))) or (not str(deviceworksheet_number).isdigit()):
            print ("Your entry is not valid. Please try again.\r\n")
            continue
        deviceworksheet_name=worksheets[int(deviceworksheet_number)-1]
        if deviceworksheet_name not in workbook.sheetnames:
            print ("The provided excel workbook does not include a worksheet named:" , deviceworksheet_name)
            continue
        else:
            break
            
    # return workbook[deviceworksheet_name]
    return deviceworksheet_name


def get_hostname(task):
    task.host.open_connection("netmiko", None)
    conn = task.host.connections["netmiko"].connection
    hostname = conn.find_prompt()
    return hostname


def get_hostname_ftd(task):
    task.host.open_connection("netmiko", None)
    conn = task.host.connections["netmiko"].connection
    conn.send_command("system support diagnostic-cli", expect_string="#", read_timeout=15, auto_find_prompt=False)
    hostname = conn.find_prompt()
    return hostname


def get_hostname_asa(task):
    task.host.open_connection("netmiko", None)
    conn = task.host.connections["netmiko"].connection
    #conn.enable()
    #import ipdb; ipdb.set_trace()
    #conn.send_command("system support diagnostic-cli", expect_string=None, auto_find_prompt=False)
    hostname = conn.find_prompt()
    return hostname

def get_credentials():

    from getpass import getpass

    username = input(
        "\r\nPlease enter your Username or press enter to use excel Username: ")
    password = getpass(
        "\r\nPlease enter your password or press enter to use excel password: ")
    DICT = dict()

    return username, password


def get_nr_from_excel_or_NB_choice():

    from rich.console import Console
    console = Console()

    nr_from_excel_or_NB_choice = 0
    while nr_from_excel_or_NB_choice != 1 or nr_from_excel_or_NB_choice != 2:
        console.print(
            "\r\n[1] Get inventory data from Excel\r\n[2] Get inventory data from Nautobot \r\n")
        nr_from_excel_or_NB_choice = input(
            "Please input 1 to get inventory data from Excel or 2 to get inventory data from Nautobot: ")
        if nr_from_excel_or_NB_choice == "1":
            console.print("\nYou have chosen to get inventory data from Excel")
            break
        elif nr_from_excel_or_NB_choice == "2":
            console.print("\nYou have chosen to get inventory data from Nautobot")
            break
        else:
            console.print("\nNot a Valid Choice. Try again")

    return nr_from_excel_or_NB_choice


def get_credentials_from_NB_or_stdin():

    from rich.console import Console
    console = Console()

    credentials_from_NB_or_stdin = 0
    while credentials_from_NB_or_stdin not in [1,2]:
        console.print(
            "\r\n[1] Get credentials from from Nautobot\r\n[2] Get credentials from stdin \r\n")
        credentials_from_NB_or_stdin = input(
            "Please input 1 to get credentials from Nautobot or 2 to get credentials from stdin: ")
        if credentials_from_NB_or_stdin == "1":
            console.print("\nYou have chosen to get credentials from Nautobot")
            break
        elif credentials_from_NB_or_stdin == "2":
            console.print("\nYou have chosen to get credentials from stdin")
            break
        else:
            console.print("\nNot a Valid Choice. Try again")

    return credentials_from_NB_or_stdin


def get_nautobot_data():

    import os
    from getpass import getpass
    from rich.console import Console

    console = Console()

    if "nautobot_url" in os.environ:
        console.print(f"nautobot_url found in environment variables.")
        nautobot_url = os.environ.get('nautobot_url')
    else:
        nautobot_url = input(f"Please input the nautobot URL, for example http://localhost:8080: ")

    if "nautobot_token" in os.environ:
        console.print(f"nautobot_token found in environment variables.")
        nautobot_token = os.environ.get('nautobot_token')
    else:
        nautobot_token = getpass(f"Please input your Nautobot authentication token: ")


    if "nautobot_query_filter" in os.environ:
        console.print(f"nautobot_query_filter found in environment variables.")
        nautobot_query_filter = os.environ.get('nautobot_query_filter')
    else:
        nautobot_query_filter = input(f"Please input your Nautobot query filter, or leave blank: ")

    nautobot_data = {
        "nautobot_url" : nautobot_url,
        "nautobot_token" : nautobot_token,
        "nautobot_query_filter" : nautobot_query_filter
    }

    return nautobot_data


def init_nautobot(url,token):

    import pynautobot 

    nautobot = pynautobot.api(
        url=url,
        token=token,
    )

    return nautobot


def get_hc_secrets_group_parameters_dict(nr,nautobot):
    secrets_group_name_set = set()
    for host in nr.inventory.dict()['hosts']:
        if nr.inventory.dict()['hosts'][host]['data']['pynautobot_dictionary']['secrets_group']:
            secrets_group_name_set.add(nr.inventory.dict()['hosts'][host]['data']['pynautobot_dictionary']['secrets_group']['name'])

    hc_secrets_group_parameters_dict = {}
    for secrets_group_name in secrets_group_name_set:
        secrets_group_credentials_list = nautobot.extras.secrets_groups.get(
            secrets_group_name
        ).secrets
        for secret_group in secrets_group_credentials_list:
            secret_provider = secret_group.secret.provider
            secret_name = secret_group.secret.name
            secret_type = secret_group.secret_type
            # console.print(f"{secret_provider} {secret_type} {secret_name}")
            if secret_provider == "hashicorp-vault":
                hc_secret_group_parameters = secret_group["secret"]["parameters"]
                if not secrets_group_name in hc_secrets_group_parameters_dict:
                    hc_secrets_group_parameters_dict.update(
                        {
                            secrets_group_name: {
                                secret_type: {
                                    "secret_parameters": hc_secret_group_parameters,
                                    "secret_name": secret_name,
                                }
                            }
                        }
                    )
                else:
                    hc_secrets_group_parameters_dict[secrets_group_name].update(
                        {
                            secret_type: {
                                "secret_parameters": hc_secret_group_parameters,
                                "secret_name": secret_name,
                            }
                        }
                    )
    return hc_secrets_group_parameters_dict


def get_credentials_from_HCKV(HCKV_TOKEN,HCKV_URL,hc_secrets_group_parameters_dict):

    import requests

    HCKV_headers = {
        "X-Vault-Token": HCKV_TOKEN
    }

    secret_group_name_credentials_dict = {}
    for secret_group_name,secret_group_credential_type_dict in hc_secrets_group_parameters_dict.items():
        for secret_group_credential_type,secret_group_credential_type_parameters in secret_group_credential_type_dict.items():
            path = secret_group_credential_type_parameters['secret_parameters']['path']
            mount_point = secret_group_credential_type_parameters['secret_parameters']['mount_point']
            path = secret_group_credential_type_parameters['secret_parameters']['path']
            response = requests.get(f'{HCKV_URL}/v1/{mount_point}/data/{path}', headers=HCKV_headers).json()
            # console.print (secret_group_credential_type)
            if secret_group_name not in secret_group_name_credentials_dict:
                # console.print (f"secret_group_name {secret_group_name} not in dict. Adding {secret_group_credential_type} with value {secret_group_credential_type_value}")
                secret_group_credential_type_value = response['data']['data'][secret_group_credential_type]
                secret_group_name_credentials_dict.update({secret_group_name : {secret_group_credential_type : secret_group_credential_type_value}})
            else:
                # console.print (f"secret_group_name {secret_group_name} is in dict. Adding {secret_group_credential_type} with value {secret_group_credential_type_value}")
                secret_group_credential_type_value = response['data']['data'][secret_group_credential_type]
                secret_group_name_credentials_dict[secret_group_name].update({secret_group_credential_type : secret_group_credential_type_value})


    return secret_group_name_credentials_dict


def get_HCKV_data():

    import os
    from getpass import getpass
    from rich.console import Console

    console = Console()

    env_vars = ['vault_url', 'vault_token']
    if all(e in os.environ for e in env_vars):
        console.print(f"Vault environment variables found, getting vault url and token.")
        HCKV_URL = os.environ.get('vault_url')
        HCKV_TOKEN = os.environ.get('vault_token')
    else:
        # Need to perform data validation
        while True:
            HCKV_URL = input(f"Please input the Hashicorp Key vault URL, for example http://localhost:8200: ")
            HCKV_TOKEN = getpass(f"Please input your Hashicorp Key vault authentication token: ")
            break

    HCKV_data = {
        "HCKV_URL" : HCKV_URL,
        "HCKV_TOKEN" : HCKV_TOKEN,
    }


    return HCKV_data


def get_nr_from_NB():

    from nornir import InitNornir
    import json

    nautobot_data = get_nautobot_data()
    nautobot_url = nautobot_data['nautobot_url']
    nautobot_token = nautobot_data['nautobot_token']
    filter_parameters_string = nautobot_data['nautobot_query_filter']
    filter_parameters = json.loads(filter_parameters_string)
    query_filter_list = []
    for filter_key, filter_value in filter_parameters.items():
        # print (f"{filter_key}")
        # print (f"{filter_value}")
        query_filter_list.append(f"{filter_key} : \"{filter_value}\"")
    query_filter = ", ".join(query_filter_list)
    # filter_key = list(filter_parameters.keys())[0]
    # filter_value = list(filter_parameters.values())[0]
    # query_filter = f"{filter_key} : \"{filter_value}\""

    nautobot = init_nautobot(nautobot_url,nautobot_token)
    nr = InitNornir(
        runner={
            "plugin": "threaded",
            "options": {
                "num_workers": 50,
            },
        },
        inventory={
            "plugin": "NautobotInventory",
            "options": {
                "nautobot_url": nautobot_url,
                "nautobot_token": nautobot_token.split(" ")[-1],
                "filter_parameters": filter_parameters,
                # "ssl_verify": False,
            },
        },
    )

    credentials_from_NB_or_stdin = get_credentials_from_NB_or_stdin()
    
    if credentials_from_NB_or_stdin == "1":
        HCKV_data = get_HCKV_data()
        HCKV_URL = HCKV_data["HCKV_URL"]
        HCKV_TOKEN = HCKV_data["HCKV_TOKEN"]


        hc_secrets_group_parameters_dict = get_hc_secrets_group_parameters_dict(nr,nautobot)
        secret_group_name_credentials_dict = get_credentials_from_HCKV(HCKV_TOKEN,HCKV_URL,hc_secrets_group_parameters_dict)


        for host in nr.inventory.dict()['hosts']:
            if nr.inventory.dict()['hosts'][host]['data']['pynautobot_dictionary']['secrets_group']:
                secrets_group_name = nr.inventory.dict()['hosts'][host]['data']['pynautobot_dictionary']['secrets_group']['name']
                nr.inventory.hosts[host].username = secret_group_name_credentials_dict[secrets_group_name]['username']
                nr.inventory.hosts[host].password = secret_group_name_credentials_dict[secrets_group_name]['password']


    elif credentials_from_NB_or_stdin == "2":
        username, password = get_credentials()

        for host in nr.inventory.dict()['hosts']:
            nr.inventory.hosts[host].username = username
            nr.inventory.hosts[host].password = password

    return nautobot, nr



def get_nr_from_excel():

    from nornir import InitNornir
    import os

    if not os.path.exists("parameters"):
        os.mkdir("parameters")

    default_folder = "parameters"
    workbook, workbookname, workbookfolder = get_workbook(default_folder)
    deviceworksheet = get_device_worksheet(workbook)
    workbookpath = (f"{workbookfolder}/{workbookname}")

    nr = InitNornir(
    logging={"enabled": False},
    runner={
        "plugin": "threaded",
        "options": {
            "num_workers": 50
        }
    },
    inventory={
        "plugin": "ExcelInventory",
        "options":
        {
            "excel_file": workbookpath,
            "excel_sheet": deviceworksheet

        }
    })

    username, password = get_credentials()


    for host in nr.inventory.dict()['hosts']:
        if username:
            nr.inventory.hosts[host].username = username
        if password:
            nr.inventory.hosts[host].password = password

    return nr, workbook, workbookname, workbookfolder, deviceworksheet, workbookpath
