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


print(yamtable.dump({
    "wow": {
        f'blah{i}': {
            "something": sensor_data(2),
            "other thing": sensor_data(1),
            "third thing": [1, 2, 3],
            "oooh": [
                {
                    "aaa": {
                        "okay": "wow"*i or 'hm', 
                        "hmm": "interesting",
                        "more?": (
                            {"wow": "srsly?"} 
                            if i < 2 else 
                            {"is it too much": "umm", "maybe": "..."}
                        )
                    }, 
                    "bbb": [1, 2], 
                    "ccc": 5
                }
                for i in range(3)
            ],
        }
        for i in range(2)
    }
}, table_format='grid'))