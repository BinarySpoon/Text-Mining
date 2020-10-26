def date_extractor():
    # imports -->
    import pandas as pd
    import re
    from calendar import month_name
    import dateutil.parser
    from datetime import datetime
    
    # import medical notes -->
    doc = []
    with open('dates.txt') as file:
        for line in file:
            doc.append(line)
    
    # create dataframe -->
    df = pd.DataFrame(doc, columns=['text'])
    
    # strip at \n --> 
    df['text'] = df['text'].apply(lambda x: x.strip('\n'))

    # capturing all date variants -->    
    pattern_dates = r'\d{1,2}\/\d{1,2}\/\d{2,4}|\d{1,2}\-\d{1,2}\-\d{2,4}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\-\d{1,2}\-\d{4}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[,.]? \d{2}[a-z]*,? \d{4}|\d{1,2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z,.]* \d{4}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]{2}[,.]* \d{4}|'+"[,.]? \d{4}|".join(month_name[1:])+"[,.]? \d{4}"+r'|\d{1,2}\/\d{4}|\d{4}'    
    df['date'] = df['text'].apply(lambda x:re.findall(pattern_dates,x))
    
    # fixing outlier 271 -->
    df['date'][271] = [df['date'][271][1]]
    
    #extract dates from dataframe -->
    df['date'] = df['date'].apply(lambda x: x[0])
    date_list = list(df['date'])
    
    # data normalization -->
    i=0
    for year in date_list:
        
        # if month is missing, it's january 1 -->
        if(re.match(r'\d{4}',year)) :
            date_list[i] = 'January 1, '+date_list[i]
            year = date_list[i]
            
        # if numeric month year format, convert to mm/01/yyyy -->
        elif (re.match(r'\d{1,2}\/\d{4}',year)) :
            date_split = year.split('/')
            date_list[i] = date_split[0] + '/1/'+date_split[1]
            year = date_list[i]
            
        # if alphabet month year format, convert to month 1 year -->
        elif(re.match(r'[A-Z][a-z]+[,.]? \d{4}',year)) :
            date_split = year.split(' ')
            date_list[i] = date_split[0] + ' 1 '+date_split[1]
            year = date_list[i]
        date_list[i] = dateutil.parser.parse(date_list[i]).strftime("%m/%d/%Y")
        i = i+1
    
    # data sorting -->
    df['date'] = date_list
    form = (lambda date: datetime.strptime(date, "%m/%d/%Y"))
    df['index'] = sorted(range(len(date_list)), key=lambda x : form(date_list[x]))
    df.drop('text', axis=1,inplace=True)
    final = list(df['index'])
    final_series = pd.Series(final)
    
    return final_series

date_extractor()
