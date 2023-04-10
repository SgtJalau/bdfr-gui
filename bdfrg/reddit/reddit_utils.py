# Enum of Reddit URL Types
from enum import Enum

from bdfrg import string_utils


class RedditUrlType(Enum):
    USER = 'user'
    SUBREDDIT = 'subreddit'
    MULTIREDDIT = 'multireddit'
    POST = 'post'
    COMMENT = 'comment'


def get_reddit_type_from_url(url: str) -> RedditUrlType:
    """
    Get the type of a Reddit URL. E.g. a subreddit, a user, a post, a comment, etc.
    :param url: The URL to get the type of e.g. https://www.reddit.com/r/AskReddit/comments/9x9q0p/what_is_the_most_underrated_movie_of_all_time/
    :return: The type of the URL
    """
    if url.startswith('https://reddit.com'):
        # add www. to the url
        url = url.replace('https://reddit.com', 'https://www.reddit.com')

    if not url.startswith('https://www.reddit.com'):
        raise Exception(f'Not a Reddit URL: {url}')

    url = url.lower()
    if url.startswith('https://www.reddit.com/user/') and '/m/' in url:
        return RedditUrlType.MULTIREDDIT
    elif url.startswith('https://www.reddit.com/user/'):
        return RedditUrlType.USER
    elif url.startswith('https://www.reddit.com/r/'):
        if '/comments/' in url:
            if '/comment/' in url:
                return RedditUrlType.COMMENT
            return RedditUrlType.POST
        return RedditUrlType.SUBREDDIT

    raise Exception(f'Could not determine Reddit URL type from {url}. Unsupported URL type.')


def get_identifying_part_of_reddit_url(url: str, url_type: RedditUrlType) -> str:
    """
    Get the identifying part of a Reddit URL for the given type. E.g. the subreddit name, the user name, the post ID, the comment ID, etc.
    For example, the subreddit name of https://www.reddit.com/r/AskReddit/comments/9x9q0p/what_is_the_most_underrated_movie_of_all_time/ is AskReddit.
    :param url: The URL to get the identifying part of e.g. https://www.reddit.com/r/AskReddit/comments/9x9q0p/what_is_the_most_underrated_movie_of_all_time/
    :param url_type: The type of the URL e.g. RedditUrlType.SUBREDDIT
    :return: The identifying part of the URL e.g. AskReddit
    """
    if url_type == RedditUrlType.SUBREDDIT:
        # Go from https://www.reddit.com/r/ till the end or next / to get the subreddit
        return string_utils.get_substring_from_string(url, 'https://www.reddit.com/r/', '/')
    elif url_type == RedditUrlType.USER:
        # Go from https://www.reddit.com/user/ till the end or next / to get the user
        return string_utils.get_substring_from_string(url, 'https://www.reddit.com/user/', '/')
    elif url_type == RedditUrlType.MULTIREDDIT:
        # Go from https://www.reddit.com/user/user/m/ till the end or next / to get the multireddit
        return string_utils.get_substring_from_string(url, '/m/', '/')
    elif url_type == RedditUrlType.POST:
        # Go from https://www.reddit.com/r/subreddit/comments/ till the end or next / to get the post
        return string_utils.get_substring_from_string(url, '/comments/', '/')
    elif url_type == RedditUrlType.COMMENT:
        # Go from https://www.reddit.com/r/xxxx/comments/id/comment/ till the end or next / to get the comment
        return string_utils.get_substring_from_string(url, '/comment/', '/')

    raise Exception(f'Could not get identifying part of Reddit URL {url} of type {url_type}')
