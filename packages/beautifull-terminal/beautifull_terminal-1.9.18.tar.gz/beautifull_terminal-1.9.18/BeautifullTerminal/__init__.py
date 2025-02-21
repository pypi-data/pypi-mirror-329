import importlib
if __name__ == "__main__":
    from terminal import BeautifullTerminal
else:
    from BeautifullTerminal.terminal import BeautifullTerminal

BeautifullTerminal()

try:
    importlib.import_module('requests')
    importlib.import_module('pkg_resources')
    
    import requests
    import pkg_resources

    importlib.import_module('BeautifullTerminal')
    installed_version = pkg_resources.get_distribution('beautifull-terminal').version

    response = requests.get(f'https://pypi.org/pypi/beautifull-terminal/json')
    response.raise_for_status()
    data = response.json()
    latest_version = data['info']['version']

    if latest_version:
        if installed_version == latest_version:
            print(f"beautifull-terminal {latest_version} is up to date!", color="green")
        else:
            print("Beautifull-terminal {installed_version} is not up to date. There is a newer version {latest_version}. To update, run 'pip install --upgrade beautiful-terminal'.", color="yellow")
except:
    pass