class A:
    def __init__(self, arg):
        self.a = 2

    def __call__(self, arg):
        print(arg, self.a)


a = A(2)
print(a(1))
