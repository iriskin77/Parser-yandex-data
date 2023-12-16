import argparse


class ManageParser:

    command: str = 'service_name'

    def __init__(self, **kwargs) -> None:
        self.init_kwargs = kwargs

    @classmethod
    def manage_service(cls, argv: list[str]):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            'service',
            help='',
            choices=[service.command for service in cls.__subclasses__()]
        )

        for service in cls.__subclasses__():
            service.add_argument(parser)

        args = parser.parse_args(argv)
        service_class = cls.get_service(command=args.service)
        obj_class_service = service_class(**dict(args._get_kwargs()))

        return obj_class_service

    @classmethod
    def get_service(cls, command: str):
        filtered = filter(
            lambda service: service.command == command, cls.__subclasses__()
        )
        try:
            return next(filtered)
        except StopIteration:
            raise ValueError(f'No service with this command: {command}. ')

    @classmethod
    def add_argument(cls, parser: argparse.ArgumentParser):
        pass

    def execute(self):
        pass
