import os

def create():
    mode = os.getenv('LASER')

    if mode == 'local':
        from LaserDisplayLocal import LaserDisplayLocal
        return LaserDisplayLocal()

    if not mode is None and mode.startswith('remote'):
        from LaserDisplayRemote import LaserDisplayRemote
        s = mode.split(':')
        if len(mode) == 2:
            return LaserDisplayRemote(mode[1])
        if len(mode) == 3:
            return LaserDisplayRemote(mode[1], mode[2])

    # default is simulator
    from LaserDisplaySimulator import LaserDisplaySimulator
    return LaserDisplaySimulator()
