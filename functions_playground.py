def unlimited_args(*args, **kwargs):
    print("Positional arguments:", args)
    print("Keyword arguments:", kwargs)


unlimited_args(1, 2, 3, 4, name="Alice", age=30)
