import pandas as pd

from datetime import datetime


def flatten(df: pd.DataFrame, fields):
    for field in fields:
        df = df.join(pd.get_dummies(df[field]), lsuffix='_left', rsuffix='_right')
    return remove(df, fields)


def remove(df: pd.DataFrame, fields):
    return df.drop(fields, axis=1)


def convert_date(dt):
    d = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
    return d.year, d.month, d.isoweekday()


def prepare_breed(df: pd.DataFrame, full_breed: set):
    df['BreedMix'] = df['Breed'].str.contains('Mix').apply(lambda x: int(x))
    df['Breed'] = df['Breed'].apply(lambda x: x.replace(' Mix', '').split('/'))
    df['BreedCount'] = df['Breed'].apply(lambda x: len(x))
    tmp = pd.DataFrame()
    for breed in full_breed:
        tmp['Breed ' + breed] = df['Breed'].apply(lambda x: int(breed in x))
    df = remove(df, ['Breed'])
    return pd.concat([df, tmp], axis=1)


def prepare_color(df: pd.DataFrame, full_color: set):
    df['Color'] = df['Color'].apply(lambda x: x.split('/'))
    df['ColorCount'] = df['Color'].apply(lambda x: len(x))
    tmp = pd.DataFrame()
    for color in full_color:
        tmp['Color ' + color] = df['Color'].apply(lambda x: int(color in x))
    df = remove(df, ['Color'])
    return pd.concat([df, tmp], axis=1)


def to_days(x):
    r = x
    if type(x) is str:
        s = x.split(' ')
        if s[1] in ('year', 'years'):
            r = int(s[0]) * 365
        elif s[1] in ('month', 'months'):
            r = int(s[0]) * 30
        elif s[1] in ('week', 'weeks'):
            r = int(s[0]) * 7
        else:
            r = int(s[0])

    return r


def prepare_age(df: pd.DataFrame):
    df['AgeuponOutcome'] = df['AgeuponOutcome'].apply(to_days)
    df['AgeuponOutcome'] = df['AgeuponOutcome'].fillna(5.0)
    #df['AgeuponOutcome'] = pd.cut(df['AgeuponOutcome'], bins=[-1, 6, 29, 59, 180, 330, 730, 1095, 3650, 10000])
    #df['AgeuponOutcome'] = df['AgeuponOutcome'].str.replace(']', ')')
    return df


def has_name(x):
    return 0 if x == 'Unknown' else 1


def prepare_name(df: pd.DataFrame):
    df['Name'].fillna('Unknown', inplace=True)
    df['Name'] = df['Name'].apply(has_name)
    return df


def prepare_date(df: pd.DataFrame):
    df["Year"], df["Month"], df["WeekDay"] = zip(*df["DateTime"].map(convert_date))
    return df
