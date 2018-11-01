

__author__ = "KousekiMiyo <miyo@icrr.u-tokyo.ac.jp>"


def coupling(target, suspect):
    ''' Calc counling ratio

    Return a ratio target/suspect.


    Parameters
    ----------
    target : gwpy.freqencyseries
        asd of the target channel

    suspect : gwpy.freqencyseries
        asd of the suspect channel

    target_ref : gwpy.freqencyseries
        asd of a reference signal of the target channel

    
    Returns
    -------
    ratio : gwpy.frequencyseries
        frequency series
    
    '''

    if isinstance(target,gwpy.frequencyseries):
        pass
    
    if isinstance(suspect,gwpy.frequencyseries):
        pass

    if target.fs != suspect.fs:
        raise ValueError('Two sampling frequencies are not same each other.')
        
    ratio = target/suspect
   
    return ratio
