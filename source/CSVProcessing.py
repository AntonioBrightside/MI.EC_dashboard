import pandas as pd


def makeDF():
    """
    Load *CSV file from /data directory.
    :return: DataFrame
    """
    df = pd.read_csv("data/jetstat.csv", delimiter=",", low_memory=False)
    pd.set_option('display.max_columns', None)

    return df


def preProcessingDF(df):
    """
    Drop all n/a rows and convert all columns into right type
    :param df: DataFrame
    :return: DataFrame
    """

    df['Дата'] = pd.to_datetime(df['Дата'], format='%Y-%m-%d')  # .dt.date

    columnNamesString = ['UID', 'Название кампании', 'Название группы', 'Устройство', 'Регион местонахождения']
    columnNamesInt = ['ID кампании', 'ID группы', 'Показы', 'Клики',
                      '87710253 Login CDN Клик по кнопке Создать аккаунт goal315669827users',
                      '87710253 Login CDN Клик по кнопкам Социальных сетей Google Yandex Git goal315670097users',
                      '87710253 CDN Форма Успешно отправлена goal312083043user',
                      '87710253 Cloud Форма Успешно отправлена goal312083368users',
                      '87710253 Cloud BMS Форма Успешно отправлена goal315659059users',
                      '87710253 Cloud CR Форма Успешно отправлена goal315658601users',
                      '87710253 Cloud LB Форма Успешно отправлена goal315659176users',
                      '87710253 Cloud PC Форма Успешно отправлена goal315659239users',
                      '87710253 Cloud MK Форма Успешно отправлена goal315659354users',
                      '87710253 Cloud MP Форма Успешно отправлена goal315659530users',
                      '87710253 Security Форма Успешно отправлена goal315659631users',
                      '87710253 Security ST Форма Успешно отправлена goal315660033users',
                      '87710253 Security Bots Форма Успешно отправлена goal315659852users',
                      '87710253 Security WAF Форма Успешно отправлена goal315659938users',
                      '87710253 Security Servers Форма Успешно отправлена goal315659697users',
                      '87710253 Security WA Форма Успешно отправлена goal315659808users',
                      '87710253 Login DNS Клик по кнопке Создать аккаунт goal315669987users',
                      '87710253 Login DNS Клик по кнопкам Социальных сетей Google Yandex Git goal315670190users',
                      '87710253 DNS Форма Успешно отправлена goal312087674users',
                      '87710253 Login Клик по кнопкам Социальных сетей Google Yandex Git goal312622532users',
                      '87710253 Login Страница подтверждения телефона после входа по кнопке Google Yandex Git goal312513686users',
                      '87710253 Login Клик по кнопке Создать аккаунт goal312620685users',
                      '87710253 Login Посещение страницы подтверждения кода из СМС goal312627270users',
                      '87710253 Login Подтверждение почты после подтверждения СМС при регистрации goal312629269users',
                      '87710253 Переход на платформу goal315658792users',
                      '87710253 Клик на кнопку Подключиться в шапке goal312072403users',
                      '87710253 EdgeЦентр Клик на кнопку Написать менеджеру goal312073397users',
                      '87710253 Форма Написать менеджеру Успешно отправлена goal318579190users',
                      '87710253 EdgeHosting Клик на кнопку Создать аккаунт goal312075226users',
                      '87710253 EdgeHosting Клик Зарегистрироваться goal312661052users',
                      '87710253 Переход на страницу хостинга goal316187849users',
                      ]

    # Drop N/A
    df = df.drop('UID', axis='columns')
    df.dropna(inplace=True)

    for column in df.columns:
        if column in columnNamesString:
            df[column] = df[column].astype('string')
        elif column in columnNamesInt:
            df[column] = df[column].astype('int')

    return df


def createNewColumns(df):
    """
    Add new techical columns: UID, PRODUCT, SOURCE, TYPE, KW_GROUP, WEEK_NUMBER
    :param df: DataFrame
    :return: DataFrame
    """
    # Add UID, PRODUCT, SOURCE, TYPE columns
    columnsToAdd = ['UID', 'PRODUCT', 'SOURCE', 'TYPE', 'KW_GROUP', 'WEEK_NUMBER']
    sourceMap = {'NETWORK': ['epc', 'rsy'],
                 'SEARCH': ['mc', 'srch']}

    # TODO: Почему-то при переносе в DEF не перевело колонки в нужный тип. Остался Object
    for num, column in enumerate(columnsToAdd, start=1):
        df.insert(num, column, 'str')
        df[column] = df[column].astype('str')

    for num, cell in enumerate(df['Название кампании'], start=0):
        campaignName = cell.lower().split(sep='_')
        df['UID'].loc[num] = campaignName[-1].replace(' ', '').upper()
        df['PRODUCT'].loc[num] = campaignName[0].replace(' ', '').upper()

        if sourceMap.get('NETWORK')[0] or sourceMap.get('NETWORK')[1] in campaignName:
            df['SOURCE'].loc[num] = 'NETWORK'
        elif sourceMap.get('SEARCH')[0] or sourceMap.get('SEARCH')[1] in campaignName:
            df['SOURCE'].loc[num] = 'SEACRH'
        else:
            raise ValueError('None of the values from the map are suitable')

        if 'epc' in campaignName:
            df['TYPE'].loc[num] = 'EPC'
        elif 'mc' in campaignName:
            df['TYPE'].loc[num] = 'MC'
        elif 'rtrgt' in campaignName:
            df['TYPE'].loc[num] = 'RETARGETING'
        else:
            df['TYPE'].loc[num] = 'HAND'

    # Add KW_GROUP, WEEK_NUMBER column
    df['WEEK_NUMBER'] = df['Дата'].dt.isocalendar().week

    for num, cell in enumerate(df['Название группы'], start=0):
        keyWordName = cell.split(sep='_')
        df['KW_GROUP'].loc[num] = keyWordName[0]

    return df

