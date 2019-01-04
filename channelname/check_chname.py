import re
import ConfigParser
import pandas as pd

def read_definition(fname='definition.ini'):
    '''
    
    Returns
    -------
    sensors:
    areas:
    locations:
    dofs:
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
            print section,items            
    #LOC_OPTION = [section.split('-')[1] for section in sections if 'LOCATION-' in section]
    return set(sensors),set(areas),set(locations),set(dofs)#,LOC_OPTION


#def read_chname(fname='test_chname.txt',LOC_OPTION=['CHAMBER','BOOTH','TABLE','RACK']):
def read_chname(fname='test_chname.txt',LOC_OPTION=['CHAMBER','BOOTH','TABLE','RACK']):    
    '''
    Returns
    -------
    sensors:
    areas:
    locations:
    dofs:

    '''
    text = pd.read_csv(fname,header=None,dtype=str)
    hoge = '|'.join(['{0}_[^_]+'.format(loc) for loc in LOC_OPTION])
    pattern = 'K1:PEM-([^_]+)_([^_]+)_({hoge}|[^_]+)_([^_]+).*'.format(hoge=hoge)
    data = text[0].str.extract(pattern,expand=True)
    sensors = data[0].unique()
    areas = data[1].unique()
    locations = data[2].unique()
    dofs = data[3].unique()
    return set(sensors),set(areas),set(locations),set(dofs)


def search_chname(words,item=0,fname='test_chname.txt',LOC_OPTION=['CHAMBER','BOOTH','TABLE','RACK']):
    text = pd.read_csv(fname,header=None,dtype=str)
    hoge = '|'.join(['{0}_[^_]+'.format(loc) for loc in LOC_OPTION])
    pattern = 'K1:PEM-([^_]+)_([^_]+)_({hoge}|[^_]+)_([^_]+).+'.format(hoge=hoge)
    data = text[0].str.extract(pattern,expand=True)
    try:
        words = map(re.escape,words)
    except TypeError:      
        print text[data[0].isnull()] 
        exit()
        
    if len(words)!=1:
        pattern = r'.*('+'|'.join(['({0})'.format(word) for word in words])+').*'
    else:
        pattern = r'.*{0}.*'.format(list(words)[0])
    print text[data[item].str.match(pattern)]    
    #exit()

def main():
    sensors1,areas1,locations1,dofs1 = read_definition()
    sensors2,areas2,locations2,dofs2 = read_chname('test_chname2.txt')    
    bad_sensor = sensors2-sensors1
    bad_area = areas2-areas1
    bad_location = locations2-locations1
    bad_dofs = dofs2-dofs1
    if bad_sensor:
        print 'Bad sensor name!',bad_sensor
        print search_chname(bad_sensor,item=0,fname='test_chname2.txt')                    
    if bad_area:
        print 'Bad area name!',bad_area
        print search_chname(bad_area,item=1,fname='test_chname2.txt')                    
    if bad_location:
        print 'Bad location name!',bad_location
        print search_chname(bad_location,item=2,fname='test_chname2.txt')                    
    if bad_dofs:
        print 'Bad dof name!',bad_dofs           
        print search_chname(bad_dofs,item=3,fname='test_chname2.txt')                    


if __name__=='__main__':
    main()        
