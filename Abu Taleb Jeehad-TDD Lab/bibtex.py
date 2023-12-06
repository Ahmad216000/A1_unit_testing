
def extract_author(Aname):
    if(Aname.find(',')!=-1):
        name = Aname.split(',')
        if (len(name) > 1):
            fristName=name[0].lstrip()
            fristName=fristName.rstrip()
            surName=name[1].lstrip()
            surName= surName.rstrip()
            return fristName,surName
    else:
        name = Aname.split()
        if (len(name)>1):
            SurName = name[-1]
            if len(name) > 2:
                fristName = name[0] + " " + name[1]
            else:
                fristName = name[0]
            return SurName, fristName
        return (Aname, "")

def extract_authors(Aname):
    name = Aname.split('and')
    Aurthors=[]
    Aurthors.append(extract_author(name[0]))
    Aurthors.append(extract_author(name[1]))
    return Aurthors