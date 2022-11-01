from redminelib import Redmine
import os

def RedmineNewIssue(TelegramID, Subject, Description):
    ProjectID = os.environ['PROJECT_ID']
    RedmineURL = os.environ['REDMINE_URL']
    RedmineKey = os.environ['REDMINE_KEY']
    redmine = Redmine(RedmineURL, key=RedmineKey)

    # Get user by Telegram ID
    users = redmine.user.filter(status=1)
    userlist = list(users)
    userfoundlist = [x for x in userlist if x.custom_fields[1].value == TelegramID]

    if len(userfoundlist) == 1:
        # Check uses membership
        user = userfoundlist[0]
        memberships = redmine.project_membership.filter(project_id=ProjectID)
        membershipslist = list(memberships)
        member = [x for x in membershipslist if x.user.id  == user.id]

        if len(member) == 1:
            redmine2 = Redmine(RedmineURL, key=RedmineKey, impersonate=user.login)
            issue = redmine2.issue.create(project_id=ProjectID, subject=Subject, description=Description)

            return issue.id
    
    return 0