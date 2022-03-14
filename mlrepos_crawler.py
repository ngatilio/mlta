from github import Github
import os
from pprint import pprint
import csv
import requests
import json

'''
   Crawl something interesting :)
'''
class GitCrawler(object):
    api         = None
    repos       = []
    issues      = []
    
    '''
        Provide Github token 
    '''
    def __init__(self, token):
        token_env = os.getenv('GITHUB_TOKEN',token)
        self.api       = Github(token_env)
    
    '''
       Search all repos given a filtering query
    '''
    def search_repos(self, repo_query, order):
        api_repos  = self.api.search_repositories(query=repo_query, sort='stars', order=order)
        self.repos      = [repo.name for repo in api_repos]
    
    '''
        Search all issues given a filtering query
    '''
    def search_issues(self, repo_name, issue_query, order):
        rep_query  = ''.join(['repo:', repo_name])
        sch_query  = ' '.join([rep_query, issue_query])
        api_issues = self.api.search_issues(query=sch_query, sort='comments', order=order)
        self.issues= [ 
                      [
                          issue.title, 
                          ' '.join([
                                     comment.body.encode('utf-8') 
                                     for comment in issue.get_comments()
                                   ]),
                          issue.state,
                          issue.created_at,
                          issue.closed_at,
                          issue.url
                      ] 
                      for issue in issues
                     ]

    '''
        Getter for repos
    '''
    def get_repos(self):
        return self.repos

    ''' 
        Getter for issues
    '''
    def get_issues(self):
        return self.issues

    '''
       Output repo names in CSV 
    '''
    def to_csv(path, opt):
        csv_file = open(path, 'w')
        csv_out  = csv.writer(csv_file)
        if opt == 'r':
            csv_out.writerow('repo_name')
            for name in self.repos:
                csv_out.writerow(name)
            csv_file.close()
        else:
            csv_out.writerow(('title','comments','state','created_at','closed_at','url'))
            for issue in self.issues:
                csv_out.writeout(issue)
                csv_file.close()


'''
   Test with machine learning samples
'''
if __name__ == "__main__":
    # auth
    #MY_TOKEN_ARRAY   = [] 
    MY_TOKEN    = 'gho_aeaf40a6c53fdad37cf7706e3c5e9fc28a81d81c'
    MY_BASE_DIR = 'C:\\Users\\ngal1802\\Desktop\\Research\\P1\\Dataset'
    gc  = GitCrawler(MY_TOKEN)

    # get all repo topics containing machine-learning and most starred
    query = 'machine-learning in:topic stars:>1000'
    path  = ''.join([MY_BASE_DIR, 'repos.csv'])
    
    gc.search_repos(repo_query=query, order='desc')
    gc.to_csv(path, 'r')
    
    # get all issues containing threat patterns
    comment_queries = 'OR'.join(['cve in:comments'  , 'vuln in:comments',
                                 'secur in:comments', 'attack in:comments'])
    title_queries   = 'OR'.join(['cve in:title'  , 'vuln in:title',
                                 'secur in:title', 'attack in:title'])
    #query           = 'OR'.join([comment_queries, title_queries])
    query           = comment_queries

    for name in gc.get_repos():
        gc.search_issues(repo_name=name, issue_query=query, order='desc')
        path = ''.join([MY_BASE_DIR, name, '.csv'])
        gc.to_csv(path, 'i')

    '''
       EOF
    '''
