def risk_per_contact(dataset):
    dataset['RiskPerContact'] = dataset['contact_duration'] * \
        dataset['contact_distance'] * 45
    return dataset


def daily_risk(dataset):
    dataset = dataset.groupby(['datetime', 'user_a']).agg(
        dailyrisk=('RiskPerContact', 'sum'))
    return dataset
