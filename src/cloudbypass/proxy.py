import random
import re


class CloudbypassProxy:

    def __init__(self, auth, **kwargs):
        """
        :param auth: format: 12345678-res:password
        """
        self.__username, self.__password = self.check_auth(auth)
        self.__region = kwargs.get('region')
        self.__expire = kwargs.get('expire', 0)
        self.__gateway = kwargs.get('gateway', 'gw.cloudbypass.com:1288')
        self.__session_id = None

    @staticmethod
    def check_auth(auth):
        """
        :param auth:
        :return:
        """
        content = re.match(r'^(\w+-(res|dat)):(\w+)$', auth)
        if auth is None or content is None:
            raise ValueError('Invalid auth format')

        return content.group(1), content.group(3)

    def set_expire(self, expire):
        """
        :param expire: Unit: second
        :return:
        """
        self.__expire = expire
        self.__session_id = None
        return self

    def set_dynamic(self):
        """
        :return:
        """
        return self.set_expire(0)

    def set_gateway(self, gateway):
        """
        :param gateway:
        :return:
        """
        self.__gateway = gateway
        self.__session_id = None
        return self

    def set_region(self, region):
        """
        :param region:
        :return:
        """
        self.__region = region
        self.__session_id = None
        return self

    def clear_region(self):
        """
        :return:
        """
        self.__region = None
        self.__session_id = None
        return self

    @property
    def username(self):
        """
        :return:
        """
        return self.__username

    @property
    def password(self):
        """
        :return:
        """
        return self.__password

    @property
    def gateway(self):
        """
        :return:
        """
        return self.__gateway

    @property
    def expire(self):
        """
        :return:
        """
        return self.__expire

    @property
    def session_id(self):
        """
        :return:
        """
        # __session_id
        if self.__session_id is None:
            self.__session_id = "".join(
                random.choices('0123456789abcdefghijklmnopqrstuvwxyz', k=11)
            )

        return self.__session_id

    def __parse_options(self):
        options = [
            self.username,
        ]
        expire = self.expire if isinstance(self.expire, int) and 0 < self.expire <= 5184000 else None

        if self.__region is not None:
            options.append(self.__region.replace(' ', '+'))

        if expire is not None:
            for time, unit in [(60, 's'), (60, 'm'), (24, 'h'), (999, 'd')]:
                if expire < time or expire % time:
                    options.append(f'{self.session_id}-{expire}{unit}')
                    break
                expire //= time

        return '_'.join(options)

    def format(self, format_str=None):
        """
        :param format_str: {username}:{password}@{gateway}
        :return:
        """
        return (format_str or '{username}:{password}@{gateway}').format(
            username=self.__parse_options(),
            password=self.__password,
            gateway=self.__gateway
        )

    def limit(self, count, format_str=None):
        """
        :param format_str:
        :param count:
        :return:
        """
        if count <= 0:
            raise ValueError('count must be greater than 0')

        for _ in range(count):
            self.__session_id = None
            yield self.format(format_str)

    def loop(self, count, format_str=None):
        """
        :param format_str:
        :param count:
        :return:
        """
        __pool = []

        if count <= 0:
            raise ValueError('count must be greater than 0')

        for _ in self.limit(count, format_str):
            __pool.append(_)
            yield _

        while True:
            for _ in __pool:
                yield _

    def copy(self):
        """
        Copy a new proxy
        :return:
        """
        return self.__copy__()

    def __str__(self):
        """
        :return:
        """
        return self.format()

    def __repr__(self):
        """
        :return:
        """
        return self.__str__()

    def __copy__(self):
        """
        Copy a new proxy
        :return:
        """
        return CloudbypassProxy(f"{self.username}:{self.password}", **{
            'region': self.__region,
            'expire': self.__expire,
            'gateway': self.__gateway,
        })

    def __iter__(self):
        """
        :return:
        """
        return self

    def __next__(self):
        """
        :return:
        """
        self.__session_id = None
        return self.__copy__()
