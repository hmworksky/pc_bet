# coding:UTF-8
import sys,os
class MetaImporter(object):
    def find_on_path(self,fullname):
        fls = ["%s__init__.py","%s.hy"]
        dirpath = "/".join(fullname.split("."))
        for pth in sys.path:
            pth = os.path.abspath(pth)
            for fp in fls :
                composed_path = fp %("%s/%s"%(pth,dirpath))
                if os.path.exists(composed_path):
                    return composed_path
    def find_moudle(self,fullname , path = None):
        path = self.find_on_path(fullname)
        if path:
            return MetaImporter(path)
    if __name__ == '__main__':
        sys.meta_path.append(MetaImporter())