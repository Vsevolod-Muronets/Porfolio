#!/usr/bin/env python3

def env_name():
    import os
    print("Your current virtual env is", os.environ.get('VIRTUAL_ENV'))

if __name__ == '__main__':
    env_name()
