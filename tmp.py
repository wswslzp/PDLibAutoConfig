class tmp(object):
    def __init__(self) -> None:
        super().__init__()
        self.config = {
            'age': 10,
            'name': 'shit'
        }

class tmpContainer(object):
    def __init__(self) -> None:
        super().__init__()
        self.tmp = tmp()

    @property
    def getTmpConfig(self):
        return self.tmp.config

if __name__ == "__main__":
    a = tmpContainer()
    print(
        a.getTmpConfig['age']
    )
    a.getTmpConfig['age'] = 15
    print(
        a.getTmpConfig['age']
    )