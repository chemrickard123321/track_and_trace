# this file is responsible for reducing the dataset to
# people who have been in contact with somone who is infections.


import pandas as pd
import numpy as np
np.random.seed(3)


def order_by_date(dataset):
    """ Orders pandas df by datetime, converts to date

    args:
        dataset: the dataset

    returns: dataset
    """

    dataset = dataset.sort_values(by=['datetime'])
    dataset['datetime'] = pd.to_datetime(dataset['datetime'], unit='s').dt.date

    return dataset


def randomly_infecting_people(dataset):

    # reveiw suggested this line is redundent but removing it brakes the code
    infectious_people = pd.DataFrame()
    infectious_people['users'] = dataset['user_b'].drop_duplicates()

    covid_list = np.random.choice(
        [0, 1], size=(len(infectious_people),), p=[2./3, 1./3]
    )

    infectious_people['infectious'] = covid_list
    infectious_people = infectious_people[infectious_people.infectious != 0]

    return infectious_people


def selectivley_infecting_people(dataset):

    infectious_candidates = pd.DataFrame()
    infectious_candidates['users'] = dataset['user_b'].drop_duplicates()
    infectious_candidates = infectious_candidates.reset_index(drop=True)

    print('\n', infectious_candidates, "\n")
    choice = int(input(
        '\nhow many people from the list above do you want to infect with covid\n'))

    if choice == 1:
        person_choice = int(input(
            '\nchoose which person you want to infect \n\nE.G to infect the fist person in the list input 0 \n'))
        infectious_people = infectious_candidates.iloc[person_choice]

    if choice > 1:

        choices = []
        print('\nchoose which people you want to infect \n\nE.G to infect the fist and second person enter 0 then enter 1')
        for i in range(choice):
            person_choice = int(input())
            choices.append(person_choice)
        infectious_people = infectious_candidates.iloc[choices]

    print(infectious_people)
    print(type(infectious_people))

    return infectious_people


def is_infetious(user, infectious_users):
    return user in infectious_users


def people_with_infectious_contacts(dataset):

    infectious_people = selectivley_infecting_people(dataset)

    # dropping people in list a with a positive test, if
    # we know they are infected they are alreasy isolating
    not_infected = dataset.user_a.apply(
        lambda u: u not in infectious_people["users"]
    )

    dataset = dataset[not_infected]
    # identiying people that have been in contact
    # with somone who has a positive test

    try:
        infectious_user = infectious_people.users.unique()

    except:
        infectious_user = np.asarray(infectious_people)

    dataset["infectious"] = dataset.user_b.apply(
        is_infetious, args=(infectious_user,))

    dataset = dataset[dataset.infectious != False]
    dataset = dataset.reset_index(drop=True)

    return dataset, infectious_people


def time_dist_converter(time, dist):

    if time < 5:
        t = 0.5
    elif time >= 5 and time < 15:
        t = 1
    elif time >= 15 and time < 60:
        t = 2
    else:
        t = 4

    if dist < 2:
        d = 2
    elif dist >= 2 and dist < 4:
        d = 1
    else:
        d = 0.1

    return t, d


def group_by_day_contact(dataset):

    def weighted_mean(x): return np.average(
        x, weights=dataset.loc[x.index, 'contact_duration'])

    dataset = dataset.groupby(
        ['datetime', 'user_a', 'user_b']).agg(
        contact_duration=('contact_duration', 'sum'),
        contact_distance=('contact_distance', weighted_mean))

    time = []
    dist = []

    for t, d in zip(dataset.contact_duration, dataset.contact_distance):
        t, d = time_dist_converter(t, d)
        time.append(t)
        dist.append(d)

    dataset['contact_duration'] = time
    dataset['contact_distance'] = dist
    return dataset
