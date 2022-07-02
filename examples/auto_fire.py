'''Automatically use yamtable to format fire outputs.

This is a temporary patch until fire officially adds support for custom serializers.
It overrides an internal fire function _PrintResult in order to do its job.
'''
import yamtable
# patches fire so that it will use our serializer
yamtable.fire_serializer()
# # or with your custom serializer
# yamtable.fire_serializer(myyam.dump)
# NOTE: this will not always be necessary. Awaiting PR to be publicly released...
# PR: https://github.com/google/python-fire/pull/345


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

if __name__ == '__main__':
    import fire
    fire.Fire(sensor_data)
    # # once the PR is released then you can delete the fire_serializer line and just do
    # fire.Fire(sensor_data, serialize=yamtable.dump)