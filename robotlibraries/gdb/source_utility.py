import os

class TagNotFoundError(Exception):
    pass

class TagError(Exception):
    pass

def line_of_test_tag(test_tag,file):
        match_in_line=[]
        with open(file) as SourceFile:
            for num, line in enumerate(SourceFile, 1):
                if test_tag in line:
                    match_in_line.append(num)
        if(len(match_in_line)==0):
            raise TagNotFoundError("Tag "+test_tag+" not found in file "+file)
        elif(len(match_in_line)==1):
             return match_in_line[0]
        else:
             raise TagError("Tag "+test_tag+" more than once in file "+file)



def src_name_from_path(src_path):
    return str(os.path.basename(src_path).split('/')[-1])
