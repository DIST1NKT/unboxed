
import requests
import json
import optparse


class GitApiUrl(object):
    """
        This class is the formula for constructing a repository url for the
         GitHub API, based on its documentation. It's __init__ takes 
         3 arguments: the subdomain, folder, and path. In this class, 
         both subdomain and folder must be provided, and path can be left
         as '' but should be provided ideally. 

         Attributes:
         Domain - str, base of the url: www.example.com
         subdomain - str, e.g users, gists
         path - str, repos in this case, but could be any resource e.g. languages
    """

    domain = 'https://api.github.com'
    tolerance = 3

    def __init__(self, subdomain, folder, path):
        self.subdomain = subdomain
        self.folder = folder
        self.path = path
        self.url = '%s/%s/%s/%s' % (self.domain, subdomain, folder, path)

    def make_request(self):
        """ 
            This function makes a HTTP request using the requests library. 
            The self.url attribute is used to make a request that is allowed 
            to fail a certain amount of times, determined by the tolerance attribute.

            Reasons for failure - 
            Request failed - Request url is incorrect, or server is down
            JSON Load failed - Response is not loadable (not of type dict),
             or Library is not imported or deprecated
        """
        tries = 0
        while tries < self.tolerance:
            try:
                r = requests.get(self.url)
                assert(r.ok)
                response = json.loads(r.content or r.text)
            except AssertionError as e:
                response = json.loads(r.content or r.text)
                print "Request to %s didn't work. %s" % (self.url, response['message'])
                tries = 3
            except Exception as e:
                print "Loading %s (JSON or URL) returned an error, %s" % (self.url, e)
                tries = tries + 1
            else:
                tries = 3
                return response
        return None

class GitUser(object):
    """
        This object class represents a user's github account and is 
        used to save the state of the user's repositories with his/her
        username, and url. 

        Attributes:
        username - str, entered from command line
        repositories - dict, fetched from url and programmatically inserted
        repo_url - GitApiUrl instance that is the url to the repository 
        of this user
    """
    
    def __init__(self, username, repo_url, repositories):
        self.username = username
        self.repositories = repositories
        self.repo_url = repo_url

    def add_repositories(self, new_repos):
        assert(type(new_repos) is dict)
        self.repositories = dict(self.repositories, **new_repos)

    def get_repos(self):
        return self.repositories.keys()

    def get_languages(self):
        return self.repositories.values()

    def unique_languages(self):
        return [language for language in set(self.get_languages()) if language is not None]

    def favourite_language(self):
        return max(self.get_languages())

    def favourite_language_detail(self):
        favourite = max(self.get_languages())
        if not favourite: return "\nThe favourite language for the %s account cannot be determined at this time"%(self.username)
        return "\nIn the %s account, %s is used in most repositories, implying that it is the favourite language\n\n"%(self.username, favourite)



def main():
    p = optparse.OptionParser(description="This command line tool prints \
out a GitHub user's favourite programming language, given his/her \
username. It performs this amazing feat based on the GitHub API's \
language field",
                                prog='foprograms',
                                version='foprograms 0.1',
                                usage= 'python exercise1.py [options] [username]')
    p.add_option('-v', '--verbose', action ='store_true', help='returns verbose output')
    options, args = p.parse_args()
    
    try:
        username = args[0]
    except Exception:
        print "Please enter a username as your 1st argument, or -h or --help"
        return

    subdomain = 'users'
    resource = 'repos'

    if options.verbose:
        print "Constructing URL to repository..."
    repo_url = GitApiUrl(
        subdomain=subdomain, folder=username, path=resource)
    
    user = GitUser(username, repo_url, {})
    if options.verbose:
        print "Making request to %s"%(user.repo_url.url)
    response = user.repo_url.make_request()

    if options.verbose:
        if not response:
            print "That could be an empty repository"
            return
        print "Calculating favourite language ...\n"
    
    for repo in response:
        user.add_repositories({repo['name']: repo['language']})   
        if options.verbose:
            print "Added repository: %s"%(repo['name'])
    if options.verbose: 
        print user.favourite_language_detail()
    else:
        print user.favourite_language()
    return


if __name__ == '__main__':
    main()
    
