from random import randrange
from datetime import timedelta, datetime

def random_date(start, end):
    """
    This function will return a random datetime between two datetime 
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


if __name__ == "__main__":
    early = datetime(1950,1,1)
    late = datetime(1999,12,31)
    for x in range(20):
        print(random_date(early,late).date())

