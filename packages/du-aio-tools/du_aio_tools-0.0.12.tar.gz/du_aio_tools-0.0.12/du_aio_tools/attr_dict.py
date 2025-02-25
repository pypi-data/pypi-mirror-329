from pathlib import Path

from dotenv import load_dotenv


class AttrDict(dict):

    def __init__(self, d=None, **kwargs):
        super().__init__()
        if d is None:
            d = {}
        else:
            d = dict(d)
        if kwargs:
            d.update(**kwargs)
        for k, v in d.items():
            setattr(self, k, v)
        # Class attributes
        for k in self.__class__.__dict__.keys():
            if (not (k.startswith('__') and k.endswith('__')) and
                    k not in ('update', 'pop','from_env', 'from_yaml', 'from_nacos')):
                setattr(self, k, getattr(self, k))

    def __setattr__(self, name, value):
        if isinstance(value, (list, tuple)):
            value = type(value)(self.__class__(x)
                                if isinstance(x, dict) else x for x in value)
        elif isinstance(value, dict) and not isinstance(value, AttrDict):
            value = AttrDict(value)
        super(AttrDict, self).__setattr__(name, value)
        super(AttrDict, self).__setitem__(name, value)

    # 将 __setitem__ 方法直接指向 __setattr__ 方法
    __setitem__ = __setattr__

    def update(self, e=None, **f):
        d = e or dict()
        d.update(f)
        for k in d:
            setattr(self, k, d[k])

    def pop(self, k, *args):
        if hasattr(self, k):
            delattr(self, k)
        return super(AttrDict, self).pop(k, *args)

    @classmethod
    def from_yaml(cls, file_path=None, text=None):
        import yaml
        if file_path:
            file_path = Path(file_path)
            if file_path.exists():
                with open(file_path, 'r') as file:
                    data = yaml.safe_load(file) or {}
        elif text:
            data = yaml.load(text, yaml.FullLoader)
        return cls(data)

    @classmethod
    def from_env(cls, file_path=None):
        load_dotenv(file_path)

    @classmethod
    def from_nacos(cls, env=True, **kwargs):
        """获取NaCos配置
        env: 默认优先加载环境变量
        NACOS_SERVER_ADDRESSES = "localhost:8848"
        NACOS_DATAID = "example-config"
        NACOS_GROUP = "DEFAULT_GROUP"
        """
        import os
        import requests
        if env:
            cls.from_env()
            # 优先加载环境变量
            server_addresses = os.getenv('NACOS_SERVER_ADDRESSES') or kwargs.get('NACOS_SERVER_ADDRESSES')
            data_id = os.getenv('NACOS_DATAID') or kwargs.get('NACOS_DATAID')
            group = os.getenv('NACOS_GROUP') or kwargs.get('NACOS_GROUP')
        else:
            server_addresses = kwargs.get('NACOS_SERVER_ADDRESSES')
            data_id = kwargs.get('NACOS_DATAID')
            group = kwargs.get('NACOS_GROUP')
        if not server_addresses:
            raise ValueError('NACOS_SERVER 不存在!')
        config_response = requests.get(
            server_addresses,
            params={"dataId": data_id,
                    "group": group}
        )
        return cls.from_yaml(text=config_response.text)

if __name__ == '__main__':
    # 读取环境变量
    import os
    import requests
    os.environ['NACOS_SERVER_ADDRESSES'] = 'http://10.168.2.83:8848/nacos/v1/cs/configs'
    os.environ['NACOS_DATAID'] = 'py-achievement.yaml'
    os.environ['NACOS_GROUP'] = 'DEFAULT_GROUP'
    config = AttrDict.from_nacos()
    print(config.db)
    print(config.db.host)  # 输出: localhost