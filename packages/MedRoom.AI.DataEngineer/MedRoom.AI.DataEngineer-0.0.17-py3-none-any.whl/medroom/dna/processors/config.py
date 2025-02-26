import yaml
import os
import logging
from dotenv import load_dotenv

PATH = f'opt/data_engineer/datalake/'

class Config:

    def __init__(self):
        super().__init__()

        logging.info('Setting up lakes file')

        self.PATH

    @staticmethod
    def parse_recipe():
        with open(PATH + 'commands.yml') as f:
            read_data = yaml.safe_load(f)
        return read_data
    

    @staticmethod
    def parse_recipe_stop():
        with open(PATH + 'stopWords.yml') as f:
            read_data = yaml.safe_load(f)
        return read_data
    
    @staticmethod
    def path_root(self):
        return PATH