from dataclasses import dataclass, field

@dataclass
class SchoolPreference:
    name: str
    capacity: int
    preferences: list[set[str]]
    pupils: set[str] = field(default_factory=set)


    def get_pupil_level(self, pupil: str) -> int:
        for i, pref in enumerate(self.preferences):
            if pupil in pref:
                return i
        return -1

    def accept_pupil(self, pupil: str) -> bool:
        if len(self.pupils) < self.capacity:
            self.pupils.add(pupil)
            return True
        else:
            pupil_level = self.get_pupil_level(pupil)
            worst_pupil = None
            worst_pupil_level = -1
            for p in self.pupils:
                p_level = self.get_pupil_level(p)
                if p_level > worst_pupil_level:
                    worst_pupil = p
                    worst_pupil_level = p_level
            if pupil_level < worst_pupil_level:
                self.pupils.remove(worst_pupil)
                self.pupils.add(pupil)
                return True
        return False
    

@dataclass
class PupilPreference:
    name: str
    preferences: list[str]
    school: str = None


def getFreePupils(preferences: dict[str, PupilPreference]) -> list[str]:
    free = []
    for pupil, preference in preferences.items():
        if preference.school == None:
            free.append(pupil)
    return free

def getFreeSchools(preferences: dict[str, SchoolPreference]) -> list[str]:
    free = []
    for school, preference in preferences.items():
        if len(preference.pupils) < preference.capacity:
            free.append(school)
    return free



def stable_match(pupils: dict[str, PupilPreference], schools: dict[str, SchoolPreference]) -> tuple[dict[str, PupilPreference], dict[str, SchoolPreference]]:
    while (freePupils := getFreePupils(pupils)) and (freeSchool := getFreeSchools(schools)):
        for pupil in freePupils:
            prefSchool =  pupils[pupil].preferences.pop(0)
            if schools[prefSchool].accept_pupil(pupil):
                pupils[pupil].school = prefSchool
    return pupils, schools


def main(pupils, schools):
    pupil_result, school_result = stable_match(pupils, schools)

    for pupil, preference in pupil_result.items():
        print(f"{pupil} is assigned to {preference.school}")

if __name__ == "__main__":
    s1 = SchoolPreference("s1", 2, [{"p1", "p2"}, {"p3", "p4"}])
    s2 = SchoolPreference("s2", 1, [{"p1", "p3"}, {"p2", "p4"}])
    s3 = SchoolPreference("s3", 1, [{"p1", "p4"}, {"p2", "p3"}])
    p1 = PupilPreference("p1", ["s1", "s2", "s3"])
    p2 = PupilPreference("p2", ["s1", "s2", "s3"])
    p3 = PupilPreference("p3", ["s1", "s2", "s3"])
    p4 = PupilPreference("p4", ["s1", "s2", "s3"])
    schools = {"s1": s1, "s2": s2, "s3": s3}
    pupils = {"p1": p1, "p2": p2, "p3": p3, "p4": p4}
    main(pupils, schools)