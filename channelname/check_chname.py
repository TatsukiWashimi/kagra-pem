import re
import ConfigParser
import pandas as pd


def read_definition(fname='definition.ini'):
    ''' Read channel name definition from init file

        
    
    Parameters
    ----------
    fname: `str`, optional
        Name of the init file.


    Returns
    -------
    sensors: `set`
        List of the sensor name
    areas: `set`
        List of the area name
    locations: `set`
        List of the location name
    dofs:
        List of the dof name
    '''
    conf = ConfigParser.ConfigParser()
    conf.read(fname)
    sections = conf.sections()

    sensors = []
    areas = [] 
    locations = []
    dofs = []
    for section in sections:
        items = conf.items(section)[0][1].split(' ')
        if 'LOCATION' in section:
            try:
                loc_option = section.split('-')[1]                
                locations += [loc_option+'_'+item for item in items]
            except IndexError as e:
                locations += items                
        elif 'AREA' == section:
            areas = items
        elif 'SENSOR' == section:
            sensors = items
        elif 'DOF' == section:
            dofs = items
        else:            
            raise ValueError('{0} is valid name'.format(section))

    return set(sensors),set(areas),set(locations),set(dofs)


def read_chname(fname='test_chname.txt',loc_option=['CHAMBER','BOOTH','TABLE','RACK','PERI']):    
    ''' Read channel name from list.

    Parameters
    ----------
    fname : 
    

    Returns
    -------
    sensors:
    areas:
    locations:
    dofs:

    '''
    text = pd.read_csv(fname,header=None,dtype=str)
    hoge = '|'.join(['{0}_[^_]+'.format(loc) for loc in loc_option])
    pattern = 'K1:PEM-([^_]+)_([^_]+)_({hoge}|[^_]+)_([^_]+).*'.format(hoge=hoge)
    data = text[0].str.extract(pattern,expand=True)
    sensors = data[0].unique()
    areas = data[1].unique()
    locations = data[2].unique()
    dofs = data[3].unique()
    return set(sensors),set(areas),set(locations),set(dofs)


def search_chname(words,item=0,fname='test_chname.txt',loc_option=['CHAMBER','BOOTH','TABLE','RACK','PERI']):
    text = pd.read_csv(fname,header=None,dtype=str)
    hoge = '|'.join(['{0}_[^_]+'.format(loc) for loc in loc_option])
    pattern = 'K1:PEM-([^_]+)_([^_]+)_({hoge}|[^_]+)_([^_]+).+'.format(hoge=hoge)
    data = text[0].str.extract(pattern,expand=True)
    try:
        words = map(re.escape,words)
    except TypeError:
        print text[data[0].isnull()] 
        #exit()
        
    if len(words)!=1:
        pattern = r'.*('+'|'.join(['({0})'.format(word) for word in words])+').*'
    else:
        pattern = r'.*{0}.*'.format(list(words)[0])
    print text[data[item].str.match(pattern)]    


    
def main(fname_chname='chname_.txt'):
    sensors1,areas1,locations1,dofs1 = read_definition()
    sensors2,areas2,locations2,dofs2 = read_chname(fname_chname)

    
    bad_sensor = sensors2-sensors1
    bad_area = areas2-areas1
    bad_location = locations2-locations1
    bad_dofs = dofs2-dofs1
    if bad_sensor:
        print 'Bad "SENSOR" name!\n ',list(bad_sensor)
        #search_chname(bad_sensor,item=0,fname=fname_chname) 
    if bad_area:
        print 'Bad "AREA" name!\n ',list(bad_area)
        #search_chname(bad_area,item=1,fname=fname_chname)                
    if bad_location:
        print 'Bad "LOCATION" name!\n ',list(bad_location)
        #search_chname(bad_location,item=2,fname=fname_chname)     
    if bad_dofs:
        print 'Bad "DOF" name!\n ',list(bad_dofs)
        #search_chname(bad_dofs,item=3,fname=fname_chname)                    
        #if not len(bad_sensor)+len(bad_area)+len(bad_location)*len(bad_dofs):
    if not bad_sensor and not bad_area and not bad_location and not bad_dofs:        
        print('Good!')

if __name__=='__main__':
    import argparse
    parser = argparse.ArgumentParser(description='PEM channel checker')
    parser.add_argument('chlist', help='channel list') 
    args = parser.parse_args()
    main(args.chlist)
