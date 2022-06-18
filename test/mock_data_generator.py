import json


outputFileName = "../data/mockSchedule.json"

courseFall   = {'code' :  'CSC225',
                'title': 'Algorithms and Data Structures I'}
courseSpring = {'code' :  'CSC320',
                'title': 'Foundations of Computer Science'}
courseSummer = {'code' :  'CSC360',
                'title': 'Operating Systems'}

courseFallSectionOne   = {'professor': '',
                          'capacity' : '0'}
courseSpringSectionOne = {'professor': '',
                          'capacity' : '0'}
courseSummerSectionOne = {'professor': '',
                          'capacity' : '0'}

courseFallSections   = [courseFallSectionOne]
courseSpringSections = [courseSpringSectionOne]
courseSummerSections = [courseSummerSectionOne]

courseOfferingFall   = {'course'  : courseFall,
                        'sections': courseFallSections}
courseOfferingSpring = {'course'  : courseSpring,
                        'sections': courseSpringSections}
courseOfferingSummer = {'course'  : courseSummer,
                        'sections': courseSummerSections}

fall   = [courseOfferingFall]
spring = [courseOfferingSpring]
summer = [courseOfferingSummer]

schedule = {'fall': fall, 'spring': spring, 'summer': summer}

with open(outputFileName, 'w') as f:
    json.dump(schedule, f)
    print(schedule)

with open(outputFileName, 'r') as f:
    obj = json.load(f)
    print(obj)
