import yamtable


import random
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


def main(**kw):
    print(yamtable.dump(sensor_data(15), **kw))

if __name__ == '__main__':
    import fire
    fire.Fire(main)