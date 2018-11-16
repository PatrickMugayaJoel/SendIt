
def serialize(objt):
    return objt.__dict__

def serialize_list(mylist):
    listtwo = []
    for item in mylist:
        listtwo.append(serialize(item))
    return listtwo
