import praw
import random
import markov_text_gen
import time


def get_topic_comments(submission):
    """(submission)-> list
takes a submission object and returns a lit of comment objects within the submission.
Include comments at all levels.
"""
    submission.comments.replace_more(limit=None)  #gets comments from reddit
    
    return submission.comments.list()
        
    
            
def filter_comments_from_authors(comments, authors):
    """(list,list)->list
takes a list of Comment objects "comments" and list of
author names (strings) "authors. returns a list of comment
objects written by all given authors. 
"""
    filtered_comments = []  
    
    for author in authors:   
        for comment in comments:
            if comment.author == author:   #adds comment to list if written by inputted author
                filtered_comments.append(comment)
    
    return filtered_comments
            
def filter_out_comments_replied_to_by_authors(comments, authors):
    """takes a list of comment objects "comments" and a list of
list of authors (strings) "authors" and returns the same list
except for without comments by or that have been responded to
by the given authors
"""
    
    filtered_comments=comments[:]#create duplicate list to avoid deleting iterable
        
    for comment in comments:
        for reply in comment.replies:
            
            if reply.author in authors:
                
                if comment in filtered_comments: 
                    filtered_comments.remove(comment)  #remove parent comment
                
                if reply in filtered_comments:
                    filtered_comments.remove(reply) #removed reply to comment
        
    for comment in filtered_comments:
       
       if comment.author in authors:
           filtered_comments.remove(comment)
           
    return filtered_comments
    

def get_authors_from_topic(submission):
    """(submission) -> dictionary
Takes a submission object as inout and returns a dictionary
where the keys are authors of comments in the submission
and the keys are the number of comments the author has
posted (as an integer). Includes all comments except for
comments with a deleted author.
"""
    authors_and_comments = {}
    comments = get_topic_comments(submission)
    
    for comment in comments:
        
        if comment.author != None:  #makes sure user is not deleted
            redditor = comment.author
            name= redditor.name
            
            if name not in authors_and_comments.keys():#makes new key value pair
                authors_and_comments[name]=1
            
            else:
                num_comments = authors_and_comments[name]
                authors_and_comments[name] = num_comments+1#adds to exisiting pair
    
    return authors_and_comments


def select_random_submission_url(reddit,url,subreddit_name,replace_lim):
    """(reddit,str,str,int)-> submission
takes a Reddit object, a topic URL (string), a subreddit name (string)
and a replace limit (integer). Roll a six-sided die. If the result is
1 or 2, returns the Submission object for the given topic URL, after
first loading the given number of extra comments. Otherwise, returns
a Submission object corresponding to a random submission from the top
submissions of the given subreddit name.
"""
    die_roll = random.randint(1,6)
    
    if die_roll == 1 or die_roll ==2:
        submission = reddit.submission(url=url) #retrieves submission object
        submission.comments.replace_more(limit=replace_lim) #retrieves comments
        
        return submission
    
    else:
        list_of_subs=[]
        top_submissions = reddit.subreddit(subreddit_name).top("all") 
         #gets list of top submissions from subreddit
        for post in top_submissions:
            list_of_subs.append(post)
        
        random_post = random.choice(list_of_subs)
        
        return random_post
            
            
def post_reply(submission,username):
    """(submission,str)-> None
 takes as input a Submission object and a string corresponding to
 Reddit username. If user has not made any replies in the given submission,
 creates a new top-level comment with text given by your generate_comment
 function. Otherwise, chooses a random comment from all comments
 that you have not already replied to, and reply to it with text given
 by your generate_comment function.
"""
    comment = madlibs.generate_comment() #generates comment using madlib module
    authors_and_coms = get_authors_from_topic(submission)
    
    if username not in authors_and_coms.keys(): 
        submission.reply(comment)
    
    else:
        comments = get_topic_comments(submission)
        authors=[]
        authors.append(username)
        filtered_comments = filter_out_comments_replied_to_by_authors(comments, authors)
        choose_comment = random.choice(filtered_comments)
        choose_comment.reply(comment)

def bot_daemon(reddit,url,replace_lim,subreddit_name,username):
    """(reddit,str,int,str,str)
In an infinite loop, calls the following three functions:
select_random_submission_url to get a Submission object,
then post_reply to reply to that submission, and finally time.sleep(60),
so a comment is posted every minnute.
"""

    while True: #this body of text loops infinitely
        submission = select_random_submission_url(reddit,url,subreddit_name,replace_lim)
        url = submission.url
        post_reply(submission,username)
        time.sleep(60)
        

if __name__ == '__main__':
    reddit = praw.Reddit('bot', config_interpolation="basic")
    
    

    
