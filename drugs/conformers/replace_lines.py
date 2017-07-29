import os


def replace_lines(file_path, idx=(0, 1), new_lines=['Hello!\n'], dest=None):
    """ 
    Replace lines between given indices with new given lines 
    Indexing:
     - to change line 5, use -> idx=(4, 5) 
     - to change line 2 and 3 use -> idx=(1, 3)
    """
    with open(file_path, 'r') as f:
        lines = f.readlines()

    if (idx[1] - idx[0]) == len(new_lines):
        lines[idx[0]:idx[1]] = new_lines

        if dest is None:
            dest = os.path.split(file_path)[0]
            os.remove(file_path)

        new_file = os.path.join(dest, os.path.basename(file_path))
        with open(new_file ,'w') as nf:
            for line in lines:
                nf.write(line)
    else:
        print('Requested indices do not match given number of lines!!!')   
