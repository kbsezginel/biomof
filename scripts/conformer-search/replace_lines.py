import os


def replace_lines(file_path, idx=[0], new_lines=['Hello!\n'], dest=None):
    """
    Replace lines in given indices with new given lines
    Indexing:
     - to change line 5, use -> idx=[4]
     - to change line 2 and 3 use -> idx=(1, 3)
    """
    with open(file_path, 'r') as f:
        lines = f.readlines()

    if len(idx) == len(new_lines):
        for i, nl in zip(idx, new_lines):
            lines[i] = nl

        if dest is None:
            dest = os.path.split(file_path)[0]
            os.remove(file_path)

        new_file = os.path.join(dest, os.path.basename(file_path))
        with open(new_file ,'w') as nf:
            for line in lines:
                nf.write(line)
    else:
        print('Requested indices do not match given number of lines!!!')
