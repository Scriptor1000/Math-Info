
@dataclass
class Preference:
    name: str
    preferences: list[str]
    partner: str = None

def check_free(preferences: dict[str, Preference]) -> list[str]:
    free = []
    for person, preference in preferences.items():
        if preference.partner == None:
            free.append(person)
    return free


def pair_format(preferences: dict[str, Preference]) -> list[tuple[str, str]]:
    # return list of pairs from preferences dict
    pairs = []
    for person, preference in preferences.items():
        pairs.append((person, preference.partner))
    return pairs


def verify_result(menPreferences: dict[str, Preference], womanPreferences: dict[str, Preference]) -> bool:
    # check if sets of pairs from men and women match
    menPairs = pair_format(menPreferences)
    womanPairs = pair_format(womanPreferences)
    if set(menPairs) != set([(b, a) for (a, b) in womanPairs]):
        return False
    return True


def stable_match(menPreferences: dict[str, Preference], womenPreferences: dict[str, Preference]) -> tuple[dict[str, Preference], dict[str, Preference]]:
    # count number of proposals
    count = 0
    # do as long as there are free men and woman
    while freeMen := check_free(menPreferences) and check_free(womenPreferences):
        # You could remove this loop and just pick the first (as presented in the original algorithm, but with this it is more obvious what is happening)
        for man in freeMen:
            count += 1
            # find preferred woman
            prefWoman =  menPreferences[man].preferences.pop(0)

            # check if woman is free
            if womenPreferences[prefWoman].partner == None:
                # Mark both partners as a pair
                womenPreferences[prefWoman].partner = man
                menPreferences[man].partner = prefWoman

            else:
                # find current man
                currentMan = womanPreferences[prefWoman].partner

                #check if new man is preferred
                if womenPreferences[prefWoman].preferences.index(man) < womenPreferences[prefWoman].preferences.index(currentMan):

                    # Mark both partners as a pair
                    womenPreferences[prefWoman].partner = man
                    menPreferences[man].partner = prefWoman

                    # Free the dumped man
                    menPreferences[currentMan].partner = None

    # after completion, return the pairs
    print(count)
    return menPreferences, womenPreferences


def main(menPreferences, womanPreferences):
    menResult, womanResult = stable_match(menPreferences, womanPreferences)

    if verify_result(menResult, womanResult):
        print("Stable matching found!")
        print("Pairs:")
        for i in pair_format(menResult): print(f"{i[0]} - {i[1]}")
    else:
        print("Programm error.")