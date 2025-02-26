from medroom.dna.processors.utils.functions import clean_text

class processCall:

    def __init__(self,
                 filename: str,
                 column_text: str,
                 sheet_name: str):

        self.filename = filename
        self.column_text = column_text
        self.sheet_name = sheet_name

        super().__init__()
    
    
    @classmethod
    def call_processor(self,
                        filename: str,
                        column_text: str,
                        sheet_name: str):
        
        df = filename
        
        return df