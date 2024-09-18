"""
the job might split up to different nodes, but the main process (with the launcher), needs to be aware of it.
For this we need a synchronizer that can keep track of the job and the runs
and notify the main process when the job is done.
"""


class Synchronizer:
    pass


class ApacheZookeeperSynchronizer(Synchronizer):
    pass


class FileSystemSynchronizer(Synchronizer):
    pass


class SocketSynchronizer(Synchronizer):
    pass


class RedisSynchronizer(Synchronizer):
    pass


class NetworkSynchronizer(Synchronizer):
    # uses ip or tcp packets
    pass
