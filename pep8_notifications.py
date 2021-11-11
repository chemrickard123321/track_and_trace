
def notifications(dataset):

    notification = []
    for i in dataset['dailyrisk']:
        if i <180:
            notification.append('no alert')
        else:
            notification.append('send alert')
    dataset['notification']=notification

    return dataset

