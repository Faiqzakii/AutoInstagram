from InstagramAPI import InstagramAPI
import time, random, os

username = input("Username: ")
password = input("Password: ")
user = InstagramAPI(username, password)
login = user.login()

if login['status'] == 'success':
    os.system('cls')

    menu = """Created By Faiqzakii
1.) Auto like timeline
2.) Auto view story timeline
3.) Auto like & views timeline
"""

    print("Logged in as {} \n".format(username))
    print(menu)

    choice = int(input("Choice: "))
    delay = int(input("Delay (Seconds): "))

    if choice == 1:
        while(True):
            try:
                timeline_id = user.getHome()
                for like in timeline_id:
                    likee = user.likePost(like)
                    if likee == False:
                        user.logIn()
                    time.sleep(random.randint(4, 7))
            except Exception as E:
                print(E)
                print("Error!")
            print("Sleeping for %s seconds"%(delay))
            time.sleep(delay)
    elif choice == 2:
        while(True):
            try:
                story_id = user.getStory()
                for story in story_id:
                    print("Viewing story @%s"%(story["username"]))
                    seen = user.seeStory(story["reelid"], story["user_id"], story["taken_at"])
                    if seen == False:
                        user.logIn()
                    time.sleep(random.randint(4, 7))
            except:
                print("Error!")
            print("Sleeping for %s seconds"%(delay))
            time.sleep(delay)
    elif choice == 3:
        while(True):
            try:
                print("="*10 + " [STORY VIEWS] " + "="*10)
                story_id = user.getStory()
                for story in story_id:
                    print("Viewing story @%s"%(story["username"]))
                    seen = user.seeStory(story["reelid"], story["user_id"], story["taken_at"])
                    if seen == False:
                        user.logIn()
                    time.sleep(random.randint(5, 10))
                print("Sleeping for %s seconds"%(delay))
                time.sleep(delay)
                #################################################
                print("="*10 + " [TIMELINE LIKE] " + "="*10)
                timeline_id = user.getHome()
                for like in timeline_id:
                    likee = user.likePost(like)
                    if likee == False:
                        user.logIn()
                    time.sleep(random.randint(5, 10))
                print("Sleeping for %s seconds"%(delay))
                time.sleep(delay)
            except Exception as E:
                print(E)
                print("Error!")
    else:
        print("Error no option!")
else:
    print(login)
