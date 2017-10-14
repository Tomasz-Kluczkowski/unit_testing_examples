def outer():

    def inner(test_arg):
        print(test_arg)

        return outer()

    return inner()


