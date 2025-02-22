import copy
import pandas as pd
import random
import os

def generate_random_filename(n=20):
    """
    Generates a random alphanumeric filename with n characters

    Args:
        n (int, optional): Number of characters. Defaults to 20.

    Returns:
        str: Filename
    """    
    alpha = "abcdefghijklmnopqrstuvwxyz"
    alpha += alpha.upper()
    filename = ""
    for _ in range(n):
        filename += alpha[random.randint(0, len(alpha)-1)]
    return filename



def compile_json(obj, top_level_key="", depth=0):
    """
    Recursive function to compile the nested JSON object into a more managable dictionary
    It essentially traverses through the JSON tree and flattens it out.
    
    Args:
        obj (dict): Nested dictionary input
        top_level_key (str, optional): Parent key which gets updated at every level. Defaults to "".
        depth (int, optional): Keeps a track of the depth of the JSON tree. Defaults to 0.

    Returns:
        dict: Flattened dictionary
    """    
    final_dict = {}
    if isinstance(obj, list):
        for n, elem in enumerate(obj):
            if top_level_key != "":
                new_key = f"{top_level_key}__listElem:{n}"
            else:
                new_key = "listElem:"+str(n)
            tmp_dict = compile_json(elem, top_level_key=new_key, depth=depth+1)
            final_dict ={**final_dict, **tmp_dict}
    elif isinstance(obj, dict):
        for key, val in obj.items():
            new_key = f"{top_level_key}__{key}" if top_level_key != "" else key
            tmp_dict = compile_json(val, top_level_key=new_key, depth=depth+1)
            final_dict = {**final_dict, **tmp_dict}
    else:
        if top_level_key not in final_dict.keys():
            final_dict[top_level_key] = ""
        final_dict[top_level_key] = obj
    return final_dict



def get_non_listelem_table(copy_dict):
    """
    It groups all the non-list items together and builds a seperate JSON.

    Args:
        copy_dict (dict): Dictionary obtained after JSON compilation and flattening

    Returns:
        tuple (json, list): Returns the non-list dictionary and keys to be removed from the existing dictionary
    """    
    # Generate the metadata (Note: Metadata is just a name to represent non listElem elements)
    metadata = {}
    meta_removals = []

    for x in copy_dict.keys():
        if "listElem:" not in x:
            metadata[x] = copy_dict[x]
            meta_removals.append(x)
    return metadata, meta_removals


def generate_managable_dict(result):
    """
    Convert the flatten parsed JSON into a managable dictionary by groupping string items which are within lists.
    Here, the Non-list elements also seperated out

    Args:
        result (dict): Parsed flattened JSON

    Returns:
       tuple (json, json): Returns  and non_listed_json
    """    
    final_dict = compile_json(result)

    copy_dict = copy.deepcopy(final_dict)

    for _ in range(10):
        # Split the list element groups
        group1 = {}
        for x in copy_dict.keys():
            tmp = x.split("__")
            if "listElem:" in tmp[-1]:
                tmp = tmp[::-1]
                i = 1
                t_key = "__".join(tmp[i:][::-1])
                if t_key not in group1:
                    group1[t_key] = []
                group1[t_key].append(x)

        # Group all the last list elements into one string
        group2 = {}
        for grp in group1.keys():
            tkeys = group1[grp]
            strtmp = []
            for k in tkeys:
                strtmp.append(copy_dict[k])
            group2[grp] = ', '.join(strtmp)

        # Remove merged groups
        removals = [y for x in group1.values() for y in x]

        copy_dict_1 = {}
        for k in copy_dict:
            if k not in removals:
                copy_dict_1[k] = copy_dict[k]

        for k in group2:
            if k in copy_dict_1.keys():
                copy_dict_1[k] = ' | '.join((copy_dict_1[k], group2[k]))
            else:
                copy_dict_1[k] = group2[k]

        if copy_dict == copy_dict_1:
            break
        copy_dict = copy.deepcopy(copy_dict_1)
    
    metadata, meta_removals = get_non_listelem_table(copy_dict)

    copy_dict_1 = {k: copy_dict[k] for k in copy_dict.keys() if k not in meta_removals}

    copy_dict = copy.deepcopy(copy_dict_1)
    return copy_dict, metadata


def generate_managable_tables(copy_dict):
    """
    Convert the flatten parsed JSON into multiple tables by groupping the flattened keys

    Args:
        copy_dict (dict): Parsed and compiled JSON which contains only the listed items

    Returns:
        tables (json): All the derived tables
    """
    tables = {}

    # Break the listElem elements into individual tables (multi-level elements)
    for k in copy_dict.keys():
        ksplit = k.split("__")
        lindex = []
        for n, ky in enumerate(ksplit):
            if "listElem:" in ky:
                lindex.append(n)

        tmp = []
        for n, ln in enumerate(lindex):
            tmp.append(('__'.join(ksplit[0:ln]), ksplit[ln], '__'.join(ksplit[ln+1:]), k))

        for n, dt in enumerate(tmp):
            if dt[0] not in tables.keys():
                tables[dt[0]] = {}
            if dt[1] not in tables[dt[0]].keys():
                tables[dt[0]][dt[1]] = {}
            if 'listElem' not in dt[2]:
                tables[dt[0]][dt[1]][dt[2]] = copy_dict[dt[3]]
            else:
                tx = dt[2].split("__")
                partial_tx = []
                for tx1 in tx:
                    if "listElem:" not in tx1:
                        partial_tx.append(tx1)
                    else:
                        break
                ptx = '__'.join(partial_tx)
                tables[dt[0]][dt[1]][ptx] = f"[## Refer:{dt[0] + '__' + dt[1]+'__'+ptx} ##]"

    return tables


def reorganize_table_references(final_combined_table_dict):
    """
    Re-organizing the table references after the tables have been groupped together.
    References needs to be updated because some tables after groupping will merge.

    Args:
        final_combined_table_dict (dict): Merged tables (dataframes)

    Returns:
        dict: Dictionary of data frames (Returns same structure as input but with updated values within each dataframe)
    """    
    # Re-organize the references based on the grouped table references
    tb_references = {}
    for table_name, fctable in final_combined_table_dict.items():
        tmp = list(set(fctable['table_ref'].to_list()))
        for ref in tmp:
            stmp = fctable[fctable['table_ref']==ref]
            indx_refs = ', '.join([str(x) for x in stmp.index.tolist()])
            tb_references[f"[## Refer:{ref} ##]"] = f"[## {table_name} Index(es): {indx_refs} ##]"

    # Replace all the references
    final_table_referenced = {}
    for key, table in final_combined_table_dict.items():
        tmp = copy.deepcopy(table)
        for oldref, newref in tb_references.items():
            tmp = tmp.replace(to_replace=[oldref,], value=newref)
        final_table_referenced[key] = tmp
    
    return final_table_referenced



def combine_and_group_tables(tables, metadata):
    """
    Function to group the manageble tables (dataframes). This groupping is done based on the flattened keys
    derived after compiling the nested JSON.
    After groupping, the references within the dataframes (strings to point to other tables to represent the associations)
    are also updated as per the groupping.
    This function also converts the non-listed element's dictionary to dataframe

    Args:
        tables (dict): Dictionary of dataframes (managable tables)
        metadata (_type_): Dictionary generated from the Non-listed elements in JSON

    Returns:
        dict: Final dictionary of the tables after updating the references
    """    
    # Combine the table structure by groupping based on structure
    # Assign table references
    combined_tables = {}
    final_combined_table_dict = {}

    for ix, table in tables.items():
        tmp = pd.DataFrame(table)
        tmp = tmp.transpose()
        tmp['table_ref'] = [ix for _ in range(len(tmp))]
        struct = tuple(tmp.columns)
        if struct not in combined_tables:
            combined_tables[struct] = pd.DataFrame()
        combined_tables[struct] = pd.concat((combined_tables[struct], tmp))

    # Organize the table columns and store them with proper references
    n = 1
    for ix, tab in combined_tables.items():
        tab.index = range(len(tab))
        if 'table_ref' in tab.columns:
            tmp_cols = tab.columns.to_list()
            tmp_cols.remove('table_ref')
            tmp_cols= ['table_ref'] + tmp_cols
            tab = tab[tmp_cols]
        final_combined_table_dict[f"Refer:Table:{n}"] = tab
        n += 1

    # Organize the metadata table
    metadf = pd.DataFrame([(k, v) for k, v in metadata.items()]) if len(list(metadata.items())) > 0 else None
    if metadf is not None:
        metadf = metadf.transpose()
        header = metadf.iloc[0].to_list()
        metadf = metadf[1:]
        metadf.columns = header
    
    final_table_referenced = reorganize_table_references(final_combined_table_dict)
    
    final_table_referenced['Refer:Table:0'] = metadf

    return final_table_referenced


def write_data_to_excel(final_tables, destination="."):
    fname = generate_random_filename()
    fname = os.path.join(destination, f"{fname}.xlsx")
    with pd.ExcelWriter(fname, engine='xlsxwriter') as writer:
        for sname, tab in final_tables.items():
            if tab is not None:
                tab.to_excel(writer, sheet_name=sname.replace(":", "_"), index=False)     
    return fname


def json_to_dataframe_conversion_pipeline(json_data, destination=".", save_excel=True):
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
    managable_dict, prim_df = generate_managable_dict(json_data)
    managable_tab = generate_managable_tables(managable_dict)
    final_tables = combine_and_group_tables(managable_tab, prim_df)
    if save_excel:
        target_file = write_data_to_excel(final_tables, destination=destination)
        return target_file
    return final_tables

