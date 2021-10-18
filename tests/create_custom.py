from keepit import keepit

ORIGIN = None


@keepit('myfunction')
def custom_function():
    return ORIGIN


if __name__ == '__main__':
    ORIGIN = 'main'
    custom_function()
