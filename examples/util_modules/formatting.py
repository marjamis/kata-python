from operator import itemgetter

def list_of_dictionaries_to_table(dataDict, excluded_headers=None, sort_key=None) -> str:
    ''' Provide a consistent, i.e. all keys are the same, dictionary and a table will be generated based off of those keys and their respective values.'''
    try:
        headers = list(dataDict[0].keys())
        if excluded_headers:
            for exclude in excluded_headers:
                headers.remove(exclude)

        data = []
        for d in range(len(dataDict)):
            tempd = []
            for header in range(len(headers)):
                tempd.append(dataDict[d][headers[header]])
            data.append(tempd)

        if sort_key:
            for pos, val in enumerate(headers):
                if val == sort_key:
                    x = pos
            data.sort(key=itemgetter(x))

        return list__to_table(headers, data)
    except Exception as e:
        print(e)
        raise e


def list__to_table(headers, data) -> str:
    ''' Provide a consistent, i.e. all keys are the same, list and a table will be generated based off of those keys and their respective values.'''
    try:
        result = ''

        # Determines the max length of each column based on the headers and the data for that header
        lengths = []
        for col in range(len(data[0])):
            maxLength = len(headers[col])
            for row in range(len(data)):
                if len(str(data[row][col])) > maxLength:
                    maxLength = len(str(data[row][col]))
            lengths.append(maxLength)

        # Outputs the headers with required padding
        result += f'| '
        for i in range(len(headers)):
            result += f'{str(headers[i]).ljust(lengths[i])} | '
        result += f'\n'

        # Outputs the delimeter between the headers and data based on the max length of padding
        result += f'| '
        for i in range(len(headers)):
            for j in range(lengths[i]):
                result += f'-'
            result += f' | '
        result += f'\n'

        # Outputs each row of data with required padding
        for row in range(len(data)):
            result += f'| '
            for col in range(len(data[row])):
                result += f'{str(data[row][col]).ljust(lengths[col])} | '
            result += f'\n'

        return result
    except Exception as e:
        print(e)
        raise e
