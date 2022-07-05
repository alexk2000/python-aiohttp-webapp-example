from webapp import main
import sys
import yaml

CONFIG_FILE = 'config.yml'

if __name__ == '__main__':

    try:
        with open(CONFIG_FILE, 'r') as ymlfile:
            config = yaml.load(ymlfile)
    except Exception as e:
        print("Wrong configuration file:\n", e)
        sys.exit(1)

    sys.exit(main(config=config))
