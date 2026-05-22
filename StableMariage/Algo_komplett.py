
def check_free(preferences):
    free = []
    for person in preferences.keys():
        if preferences[person][1] == 0:
            free.append(person)
    return free


def pair_format(preferences):
    # return list of pairs from preferences dict
    pairs = []
    for person in preferences.keys():
        pairs.append((person, preferences[person][1]))
    return pairs


def verify_result(menPreferences, womanPreferences):
    # check if sets of pairs from men and women match
    menPairs = pair_format(menPreferences)
    womanPairs = pair_format(womanPreferences)
    if set(menPairs) != set([(b, a) for (a, b) in womanPairs]):
        return False
    return True


def stable_match(menPreferences, womenPreferences):
    # count number of proposals
    count = 0
    # do as long as there are free men and woman
    while check_free(menPreferences) != [] and check_free(womenPreferences) != []:
        freeMen = check_free(menPreferences)

        # You could remove this loop and just pick the first (as presented in the original algorithm, but with this it is more obvious what is happening)
        for man in freeMen:
            count += 1
            # find preferred woman
            prefWoman =  menPreferences[man][0][0]

            # check if woman is free
            if womenPreferences[prefWoman][1] == 0:
                # Mark both partners as a pair
                womenPreferences[prefWoman][1] = man
                menPreferences[man][1] = prefWoman

                # Remove option to couple again
                menPreferences[man][0].remove(prefWoman)

            else:
                # find current man
                currentMan = womanPreferences[prefWoman][1]

                #check if new man is preferred
                if womenPreferences[prefWoman][0].index(man) < womenPreferences[prefWoman][0].index(currentMan):

                    # Mark both partners as a pair
                    womenPreferences[prefWoman][1] = man
                    menPreferences[man][1] = prefWoman

                    # Free the dumped man
                    menPreferences[currentMan][1] = 0

                    # Remove option to couple again
                    menPreferences[man][0].remove(prefWoman)

                else:
                    # Remove option to couple again
                    menPreferences[man][0].remove(prefWoman)

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


@dataclass
class Preference:
    name: str
    preferences: list[str]
    partner: str = None



if __name__=="__main__":
    menPreferences = {
        'A': [['Z', 'Y', 'W', 'X'], 0],
        'B': [['X', 'Z', 'W', 'Y'], 0],
        'C': [['Z', 'W', 'X', 'Y'], 0],
        'D': [['Y', 'X', 'W', 'Z'], 0],
    }

    womanPreferences = {
        'W': [['A', 'B', 'C', 'D'], 0],
        'X': [['A', 'D', 'C', 'B'], 0],
        'Y': [['B', 'A', 'C', 'D'], 0],
        'Z': [['D', 'B', 'C', 'A'], 0],
    }

    main(menPreferences, womanPreferences)

