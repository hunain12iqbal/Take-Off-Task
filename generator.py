
class Generator():

    def number_generator(num):
        num = 0
        while True:
            yield num
            num = (num + 1) % 10  # Reset to 0 after 9

if __name__ == "__main__":
    generator_object = Generator()
    gen = generator_object.number_generator()
    for _ in range(24):
        print(next(gen))
