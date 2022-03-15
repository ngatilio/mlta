from github import Github
import os
from pprint import pprint
import csv
import requests
import json

#tokens = ['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',
#          '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',
#          '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',
#          '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',
#          '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']
#token = os.getenv('GITHUB_TOKEN','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')
#token = os.getenv('GITHUB_TOKEN','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')
#token  = os.getenv('GITHUB_TOKEN','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')
#token  = os.getenv('GITHUB_TOKEN','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')
security_pattern = 'vuln OR secur OR priva OR cve'
token  = os.getenv('GITHUB_TOKEN','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')
g      = Github(token)
#apps   = open('ml_issues_url.csv', encoding='utf-8',)
apps   = open('ml_issues_url_except.csv', encoding='utf-8',)
repos  = csv.reader(apps)
for repo in repos:
    repo_id = repo[0].replace("https://github.com/", "").replace("/issues", "")
    #repo    = g.get_repo(repo_id)
    #issues  = repo.get_issues()
    queries = 'repo:' + repo_id + ' ' + security_pattern
    issues = g.search_issues(queries)
    issues_dict = {}
    i = 1
    for issue in issues:
        issue_dict = {}
        issue_dict['url'] = issue.url
        issue_dict['title'] = issue.title
        issue_dict['comments'] = [comment.body.encode('utf-8') for comment in issue.get_comments()]
        issue_dict['state'] = issue.state
        issue_dict['created_at'] = issue.created_at
        issue_dict['closed_at'] = issue.closed_at
        issues_dict[i] = issue_dict
        i += 1

    csvfile  = '%s-issues.csv' % (repo_id.replace('/', '-'))
    csvpath  = 'issues-1/'+csvfile
    csvfileo = open(csvpath, 'w')
    csvout   = csv.writer(csvfileo)
    csvout.writerow(('url', 'title', 'comments', 'state', 'created_at', 'closed_at'))
    for issue in issues_dict.values():
        csvout.writerow([issue['url'], issue['title'].encode('utf-8'), issue['comments'], issue['state'], issue['created_at'], issue['closed_at']])

    csvfileo.close()
