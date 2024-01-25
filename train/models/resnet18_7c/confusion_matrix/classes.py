CLASSES = {
    0: '0 - 2',
    1: '3 - 9',
    2: '10 - 20',
    3: '21 - 27',
    4: '28 - 45',
    5: '46 - 65',
    6: '> 65'
}

def class_labels_reassign(age):
    if 0 <= age <= 2:
        return 0
    elif 3 <= age <= 9:
        return 1
    elif 10 <= age <= 20:
        return 2
    elif 21 <= age <= 27:
        return 3
    elif 28 <= age <= 45:
        return 4
    elif 46 <= age <= 65:
        return 5
    else:
        return 6