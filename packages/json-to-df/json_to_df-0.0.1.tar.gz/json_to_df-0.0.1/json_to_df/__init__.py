from .json_to_df import json_to_dataframe_conversion_pipeline
import json
import os

def convert(obj, destination=".", save_excel=True):
    """
    Complete execution pipeline
    This function performs the following steps
    1. Parse and compiles the nested JSON object
    2. Convert the flattened JSON to detect non-listed elements and creates a seperate dataframe out of it
    3. Generate managable dictionary for the rest of the elements
    4. Convert the above dictionary to managable tables (dataframes)
    5. Group the dataframes and update the table references
    6. Write the tables as excel file

    Args:
        json_data (dict): Raw JSON object
        destination (str, optional): Folder where the excel file has to be saved. Defaults to ".".
        save_excel (bool, optional): True: To save the output as excel. False: To return dictionary of dataframes. Defaults to True.

    Returns:
        Condition if save_excel=True
            str: Excel file path
        Condition if save_excel=False
            dict[DataFrame]: Dictionary of dataframes
    """
    # Check if obj is filepath or a string then, read the json content
    json_obj = None
    if isinstance(obj, str):
        if os.path.exists(obj):
            try:
                if obj.endswith(".json"):
                    with open(obj, "r") as jf:
                        json_obj = json.load(jf)
                else:
                    raise Exception("Not a JSON file")
            except BaseException as e:
                raise Exception(f"Exception occured while reading the json file\n{str(e)}")
        else:
            raise Exception("Invalid path provided, kindly check the file reference")
    elif isinstance(obj, dict):
        json_obj = obj
    return json_to_dataframe_conversion_pipeline(
        json_data=json_obj,
        destination=destination,
        save_excel=save_excel
    )
    