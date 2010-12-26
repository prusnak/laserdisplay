import os

def create(mode = os.getenv('LASER')):
    if mode == 'local':
        from LaserDisplayLocal import LaserDisplayLocal
        return LaserDisplayLocal()

    if not mode is None and mode.startswith('remote'):
        from LaserDisplayRemote import LaserDisplayRemote
        s = mode.split(':')
        if len(s) == 2:
            return LaserDisplayRemote(s[1])
        if len(s) == 3:
            return LaserDisplayRemote(s[1], s[2])

    # default is simulator
    from LaserDisplaySimulator import LaserDisplaySimulator
    return LaserDisplaySimulator()

def createProxy(desc):
    if not isinstance(desc, list) and not isinstance(desc, tuple):
        raise ValueError('createProxy() method accepts only list and tuples')
    from LaserDisplayProxy import LaserDisplayProxy
    return LaserDisplayProxy( map(lambda x: create(x), desc) )
