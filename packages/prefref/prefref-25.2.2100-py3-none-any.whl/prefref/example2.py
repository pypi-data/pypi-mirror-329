from prefref import *

@dataclass
class MyOptions(Config_Options):
    do_thing = Config_Option('do_thing', 'test')

config = Config(MyOptions(), 'Application Name', 'Does things!')
args: MyOptions = config.options
