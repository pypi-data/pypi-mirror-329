def useCounter(name: str):
    tot_count = 0
    tot_correct = 0

    def increase_total(number: int = 1):
        nonlocal tot_count
        tot_count += number

    def increase_correct(number: int = 1):
        nonlocal tot_correct
        tot_correct += number

    def get_count() -> tuple[int, int]:
        return tot_count, tot_correct

    return increase_total, increase_correct, get_count
