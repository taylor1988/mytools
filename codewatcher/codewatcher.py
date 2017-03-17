#-*- coding:utf-8 -*-
#监控代码 并自动重启进程

import sys
import abc

E_CHANGE_FILENAME = 0X1     #包括文件创建 删除 重命名事件
E_CHANGE_DIRNAME = 0X2      #包括文件夹创建 删除 重命名事件
E_WRITE = 0X3               #文件写入事件

class ProcessManager():
    pass

class EventWatcher(metaclass=abc.ABCMeta):

    def __init__(self, path, ):
        self.watchPath = path

    @abc.abstractmethod
    def registEvent(self, event):
        pass

    def setManager(self, manager):
        self.manager = manager

    @abc.abstractmethod
    def startWatch(self):
        pass

def genWinWatcher():
    import win32file
    import win32event
    import win32con
    class WinWatcher(EventWatcher):

        def registEvent(self, event):
            event2watch = 0x0
            if E_CHANGE_FILENAME & event:
                event2watch = event2watch | win32con.FILE_NOTIFY_CHANGE_FILE_NAME
            if E_CHANGE_DIRNAME & event:
                event2watch = event2watch | win32con.FILE_NOTIFY_CHANGE_DIR_NAME
            if E_WRITE & event:
                event2watch = event2watch | win32con.FILE_NOTIFY_CHANGE_LAST_WRITE
            self.event2watch = event2watch


        def makeHandle(self):
            FILE_LIST_DIRECTORY = 0x0001
            hDir = win32file.CreateFile(
                self.watchPath,
                FILE_LIST_DIRECTORY,
                win32con.FILE_SHARE_READ |
                win32con.FILE_SHARE_WRITE |
                win32con.FILE_SHARE_DELETE,
                None,
                win32con.OPEN_EXISTING,
                win32con.FILE_FLAG_BACKUP_SEMANTICS,
                None
            )
            return hDir

        def startWatch(self):
            while True:
                results = win32file.ReadDirectoryChangesW(
                    self.makeHandle(),
                    1024,
                    True,
                    self.event2watch,
                    None,
                    None
                )
                for action, file in results:
                    if file.endwith()

def genLinuxWatcher():
    pass

def genWatcher():
    """
    根据不同平台创建不同的watcher
    """
    platformStr = sys.platform
    if 'win32' in platformStr:
        return genWinWatcher()
    elif 'linux' in platformStr:
        return genLinuxWatcher()
    else:
        return None
