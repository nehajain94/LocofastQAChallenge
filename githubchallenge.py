
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import config


class GithubLocoFastChallenge:

    def __init__(self):
        self.driver = webdriver.Chrome(config.chrome_path)

    def login(self):
        """
        connecting to Github
        :return: True/False
        """

        try:
            print("Connecting to Chrome")
            time.sleep(3)
            self.driver.get("https://github.com/login")
            self.driver.find_element_by_name("login").send_keys(config.username)
            self.driver.find_element_by_name("password").send_keys(config.password)
            time.sleep(3)
            self.driver.find_element_by_name("commit").send_keys(Keys.ENTER)
            self.driver.maximize_window()
            time.sleep(3)
            # Checking whether we have reached home page or not ...
            is_home = False
            while not is_home:
                if self.driver.current_url == 'https://github.com/':
                    is_home = True
            print('Logged in successfully...')
            return True
        except Exception as e:
            print(e)
            return False

    def create_repository(self, repos_name):
        """
        Creating a Repository
        :param repos_name: name of the repository
        :return: None
        """

        print('-' * 50)
        print('Creating a repository ....')
        print('-' * 50)
        try:
            self.driver.find_element_by_link_text("New").click()
            print('Entering Repository name.')
            self.driver.find_element_by_id("repository_name").send_keys(repos_name)
            print('Adding Description for the repository.')
            self.driver.find_element_by_id("repository_description").send_keys(":smiley:")
            time.sleep(3)
            print('Choosing the type of repository (Public/ Private). ')
            self.driver.find_element_by_id("repository_visibility_public").click()
            time.sleep(3)
            self.driver.find_element_by_xpath("/html/body/div[4]/main/div/form/div[4]/button").click()
            print('Repository created successfully!!')
            time.sleep(3)
        except Exception as e:
            print(e)

    def create_issue(self, title=None, description=None):
        """
        Creates a new issue given title and description
        :param title: Title of issue
        :param description: Description of issue
        :return: Issue Id
        """

        print('-' * 50)
        print('Creating an issue ....')
        try:
            self.driver.find_element_by_xpath("/html/body/div[4]/div/main/div[1]/nav/ul/li[2]/a").click()
            self.driver.find_element_by_xpath("/html/body/div[4]/div/main/div[2]/div/div/div[2]/div[2]/a").click()
            if title:
                self.driver.find_element_by_id("issue_title").send_keys(title)
            else:
                self.driver.find_element_by_id("issue_title").send_keys('New Issue')
            if description:
                self.driver.find_element_by_id("issue_body").send_keys(description)
            else:
                self.driver.find_element_by_id("issue_body").send_keys('Github testing')
            self.driver.find_element_by_xpath("/html/body/div[4]/div/main/div[2]/div/div/form/div/div/div[1]/"
                                              "div/div[1]/div[2]/button").click()
            last_issue_ids = self.driver.find_elements_by_xpath("/html/body/div[4]/div/main/div[2]/div/div/"
                                                                "div/div[1]/div[1]/div/h1/span[2]")
            time.sleep(3)
            for id in last_issue_ids:
                print('Issue {} created successfully..'.format(id.text))
            return last_issue_ids[0].text.replace('#', '')
        except Exception as e:
            print(e)
            return False

    def navigate_to_issue_from_comment(self, issue_id):
        """
        Navigation function
        :param issue_id: # of issue
        :return: None
        """

        print('-' * 50)
        print('Navigating to issue from comment...')
        print('-' * 50)
        try:
            print('Opening all issues')
            self.driver.find_element_by_xpath("/html/body/div[4]/div/main/div[1]/nav/ul/li[2]/a").click()
            time.sleep(2)
            self.driver.find_element_by_id("issue_{}_link".format(issue_id)).click()

            self.driver.find_element_by_xpath(
                '/html/body/div[4]/div/main/div[2]/div/div/div/div[2]/div/div[1]/div/div[1]/'
                'div[2]/div[4]/div/div[2]/div/div[2]/task-lists/table/tbody/tr/td/p/a').click()
            time.sleep(2)
        except Exception as e:
            print(e)

    def comment_on_issue(self, message, issue_id):
        """
        To create a comment on issue
        :param message: message of the comment
        :param issue_id: # of issue
        :return: None
        """

        print('-' * 50)
        print('Commenting on issue: {}'.format(issue_id))
        try:
            print('-' * 50)
            print('Commenting on issue : {}'.format(issue_id))
            print('-' * 50)
            print('Clicking on Issues button..')
            self.driver.find_element_by_xpath("/html/body/div[4]/div/main/div[1]/nav/ul/li[2]/a").click()

            self.driver.find_element_by_id("issue_{}_link".format(issue_id)).click()
            self.driver.find_element_by_id("new_comment_field").send_keys(message)
            self.driver.find_element_by_xpath("/html/body/div[4]/div/main/div[2]/div/div/div/div[2]"
                                              "/div/div[1]/div/div[2]/div/form/div/div/div/div/div[2]/button").click()
        except Exception as e:
            print(e)

    def delete_repository(self, repo):
        """
        Deletes a repository
        :param repo: name of the repository
        :return: None
        """

        print('-' * 40)
        print('Deleting a Repository')
        print('-' * 40)
        try:
            print('Clicking on Settings Button')
            self.driver.find_element_by_xpath("/html/body/div[4]/div/main/div[1]/nav/ul/li[9]/a").click()
            time.sleep(3)

            print('Scrolling down to bottom of page..')
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            print('Clicking on delete repository button')
            self.driver.find_element_by_xpath("/html/body/div[4]/div/main/div[2]/div/div/"
                                              "div[2]/div/div[9]/ul/li[4]/details/summary").click()
            time.sleep(1)

            print('Entering repo name: {}'.format(repo))
            self.driver.find_element_by_xpath("/html/body/div[4]/div/main/div[2]/div/div/div[2]/div/div[9]/ul/"
                                              "li[4]/details/details-dialog/div[3]/form/p/input").send_keys(repo)
            time.sleep(1)

            self.driver.find_element_by_xpath("/html/body/div[4]/div/main/div[2]/div/div/div[2]/div/"
                                              "div[9]/ul/li[4]/details/details-dialog/div[3]/form/button").click()

            print('Deleted Repository successfully...')
        except Exception as e:
            print(e)


if __name__ == '__main__':
    github = GithubLocoFastChallenge()
    github.login()

    repo_name = 'LocofastQAChallenge'
    # Challenge -1 : Creating repository
    github.create_repository(repo_name)
    # Challenge -2: Creating issue - (a)
    issue1_id = github.create_issue(title='Issue1')
    # Challenge -2: Creating issue - (b)
    issue2_id = github.create_issue(title='Issue-2..#{}'.format(issue1_id),
                                    description='Issue - 2..  reference to Issue #{}'.format(issue1_id))
    # Challenge -3: Adding comment in issue1 : (a)
    github.comment_on_issue(message='New comment added!!', issue_id=issue1_id)
    # Challenge -3: Adding emoji in repository : (b)
    # Done as a part of challenge #1
    # Challenge -4: Adding comment in issue1 : (a)
    github.comment_on_issue(message='New comment added with mention Issue :#{} '.format(issue2_id), issue_id=issue1_id)
    # Challenge -4: Navigate to the issue from the comment : (b)
    github.navigate_to_issue_from_comment(issue1_id)
    # Challenge -5: Delete repository
    github.delete_repository(repo='{}/{}'.format(config.username, repo_name))

    # Closing the browser
    github.driver.close()


