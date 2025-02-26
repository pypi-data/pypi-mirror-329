import argparse


class ParseDict(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        d = {}
        if values:
            for item in values:
                if item is None or item == '{}':
                    continue
                else:
                    [key, value] = item.split("=", 1)
                    # we remove blanks around keys, as is logical
                    d[key.strip()] = value

        setattr(namespace, self.dest, d)
