'''Some basic formatting based on the shape of the data.


'''
import random
import yamtable

# utilities for displaying data

def trunc(d, n=50):
    return f'{d[:n]} ...' if len(d) > n else d

def run(data, wait=False, **kw):
    print("Do you really want to look at this ???")
    # print(trunc(str(data), 200))
    print(str(data))
    input()

    print("Ah much better :)")
    print(yamtable.dump(data, **kw))
    wait and input()

# 

def basic_data(n=5):
    return [
        {"asdf": i, "jkl;": 10-i, "uiop": 2*i - 5}
        for i in range(n)
    ]

def sensor_data(n=8):
    return [
        {
            'is_up': random.choice([False, True]), 
            'value_A': random.random(), 
            'value_B': random.random() + 100,
            'id': random.randint(1000, 5000)
        } 
        for i in range(n)
    ]


class Asdf:
    def __str__(self) -> str:
        return "[Asdf: This is my __str__() method]"

def main(**kw):
    yamtable.yam.config(**kw)

    run(basic_data(), wait=True)

    run(sensor_data(), wait=True)

    run({
        f'blah{i}': {
            "something": sensor_data(2),
            "other thing": sensor_data(1),
            "third thing": [1, 2, 3],
            "custom_class": Asdf(),
        }
        for i in range(2)
    })

if __name__ == '__main__':
    import fire
    fire.Fire(main)