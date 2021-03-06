import config
import os
import re
from . import *
from interfaces.validator import Validator

class EmuInput(Validator):
    '''
    Base class for emulator inputs. Children classes only need to implement functions
    _validate_content and _validate_count to return true when the respective fields are valid,
    and may optionally define a delimiter other than '*' and a destination path other than
    project_root/game.
    '''
    delimiter = '*'
    path = config.data_dir

    def __init__(self, content, count=1):
        content = str(content)
        count = int(count)

        if not type(self)._validate_count(count):
            raise ValueError('Invalid count "{}".'.format(count))
        elif not type(self)._validate_content(content):
            raise ValueError('Invalid content "{}".'.format(content))

        self._content = content
        self._count = count

    def __eq__(self, other):
        return (isinstance(other, type(self)) and
                self.count == other.count and
                self.content == other.content)

    def __hash__(self):
        return hash((self.content, self.count))
    
    def __str__(self):
        return self.content + str(self.count)

    @abstractstaticmethod
    def _validate_content(content):
        pass

    @abstractstaticmethod
    def _validate_count(count):
        pass

    @classmethod
    def _parse_content(cls, message):
        '''
        Retrieves content portion of input.
        :param cls: Current class.
        :param message: Message to parse.
        '''
        message = message.lower()

        if cls.delimiter in message:
            result = message.split(cls.delimiter)[0]
        else:
            result = re.sub('\\d+$', '', message)

        if not cls._validate_content(result):
            raise ValueError('Invalid content "{}".'.format(result))

        return result

    @classmethod
    def _parse_count(cls, message):
        '''
        Retrieves count portion of input.
        :param cls: Current class.
        :param message: Message to parse.
        :returns: int
        '''
        if cls.delimiter in message:
            result = message.split(cls.delimiter)[1]
        else:
            match = re.search('\\d+$', message)
            result = match.group(0) if match else 1

        result = int(result)

        if not cls._validate_count(result):
            raise ValueError('Invalid count "{}".'.format(result))

        return int(result)

    @property
    def content(self):
        return self._content

    @property
    def count(self):
        return self._count

    @property
    def destination(self):
        cls = type(self)

        if not cls._filename:
            raise NotImplementedError('Class does not define a destination file in {}._filename.'.format(cls.__name__))

        return os.path.join(type(self)._location, cls._filename)

    @classmethod
    def condense(cls, inputs):
        '''
        Condenses list of inputs into equivalent list with identical consecutive inputs
        merged into one, then returns condensed list.
        :param inputs: List of inputs to condense.
        '''
        inputs = list(inputs) # in case of immutable tuple
        changed = True

        while changed:
            changed = False

            for i in range(1, len(inputs)):
                in1 = inputs[i - 1]
                in2 = inputs[i]

                if in1.content == in2.content:
                    count = in1.count + in2.count
                    button = cls(in1.content, count)

                    inputs[i - 1] = None
                    inputs[i] = button
                    changed = True

            inputs = [i for i in inputs if i]

        return inputs

    def serialize(self):
        '''
        Serializes input to send to NES.
        '''
        return self.delimiter.join((str(x) for x in [self.content, self.count]))

    @classmethod
    def deserialize(cls, serialized):
        '''
        Deserializes serialized input.
        :param cls: Current class.
        :param serialized: The serialized input.
        :returns: EmuInput object
        '''
        content = cls._parse_content(serialized)
        count = cls._parse_count(serialized)
        return cls(content, count)