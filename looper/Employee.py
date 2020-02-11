#         "primaryPhoneNumber": "",
#         "birthday": "January 01",
#         "followingCount": 14,
#         "profileImageURL": "/documents/29158/29159/1470864091157webupload_00091669.jpg/460e5d29-d395-4664-9037-6ea54fdaefff?t=1470864091157",
#         "loopTopicAssignmentsCount": 0,
#         "classNameId": 000000,
#         "employmentTypeLabel": "Full-Time",
#         "locationName": "City, Country",
#         "type": 5,
#         "notifyingEmail": false,
#         "coverImageProfileURL": "/documents/29158/29159/1435281043437web20150626011043436PHCMFOYV/60d971fc-4f8f-49f1-8dc9-f6b9f951540f?t=1435281043445",
#         "otherPhonesJSONArray": [],
#         "inactive": false,
#         "languages": "",
#         "employmentType": 1,
#         "following": false,
#         "permissionDelete": false,
#         "description": "",
#         "name": "Name Name",
#         "age": "",
#         "displayURL": "/web/guest/home/-/loop/people/_Name.Name",
#         "descriptionMarkdownHTML": "",
#         "firstName": "Name",
#         "facebookSn": "",
#         "followingType": 0,
#         "jobTitle": "Title",
#         "lastName": "Name",
#         "skypeSn": "",
#         "preferredName": "",
#         "jobResponsibilities": "",
#         "otherEmailAddressesJSONArray": [],
#         "loopParticipantAssignmentsCount": 7,
#         "modifiedTime": 1470864091000,
#         "male": true,
#         "hireDate": "December 01, 2009",
#         "emailAddress": "email@email.com",
#         "twitterSn": "",
#         "permissionEdit": false,
#         "coverImageThumbnailURL": "/documents/29158/29159/1435281045230thumbnail20150626011045230DCKNBYER/2f0db183-47b6-44e3-9647-8cbcb01293f0?t=1435281045231",
#         "gitHubSn": "",
#         "followersCount": 96,
#         "classPK": 000000,
#         "notifying": false

class Employee(object):
    def __init__(self, id, firstName, lastName, emailAddress):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.emailAddress = emailAddress
        
        # self.jobTitle = jobTitle
        # self.hireDate = hireDate
        # self.locationName = locationName
        
        self.managers = []
        self.subordinates = []
        self.visited = False

    def setID(self, id):
        try:
            int = id
            self.id = id
        except ValueError:
            print('Must be an integer.')

    def addManager(self, employee):
        self.managers.append(employee)

    def addSubordinate(self, employee):
        self.subordinates.append(employee)

    def markVisited(self):
        self.visited = True

    def hasManager(self, employee):
        if employee not in self.managers:
            return False
        return True

    def hasSubordinate(self, employee):
        if employee not in self.subordinates:
            return False
        return True

    def isVisited(self):
        return self.visited

    def getId(self):
        return self.id

    def getName(self):
        return self.firstName + " " + self.lastName

    def getEmail(self):
        return self.emailAddress

    # def getJobTitle(self):
    #     return self.jobTitle

    # def getHireDate(self):
    #     return self.hireDate

    # def getLocationName(self):
    #     return self.locationName

    def getManagers(self):
        return self.managers

    def getSubordinates(self):
        return self.subordinates