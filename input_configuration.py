from dataclasses import dataclass
from enum import Enum
from typing import List


class TimeFilter(Enum):
    ALL = 'all'
    HOUR = 'hour'
    DAY = 'day'
    WEEK = 'week'
    MONTH = 'month'
    YEAR = 'year'


class SortType(Enum):
    CONTROVERSIAL = 'controversial'
    HOT = 'hot'
    NEW = 'new'
    RELEVANCE = 'relevance'
    RISING = 'rising'
    TOP = 'top'


class Format(Enum):
    JSON = 'json'
    XML = 'xml'
    YAML = 'yaml'


@dataclass
class DownloaderConfiguration:
    make_hard_links: bool = False
    max_wait_time: int = 120
    no_dupes: bool = False
    search_existing: bool = False
    file_scheme: str = '{REDDITOR}_{TITLE}_{POSTID}'
    folder_scheme: str = '{SUBREDDIT}'
    exclude_id: List[str] = None
    exclude_id_file: List[str] = None
    skip_domain: List[str] = None
    skip: List[str] = None
    skip_subreddit: List[str] = None
    min_score: int = None
    max_score: int = None
    min_score_ratio: float = None
    max_score_ratio: float = None


@dataclass
class ArchiverConfiguration:
    all_comments: bool = False
    format: Format = Format.JSON
    comment_context: bool = False


@dataclass
class InputConfiguration:
    directory: str = None
    authenticate: bool = False
    config: str = None
    opts: str = None
    disable_module: List[str] = None
    filename_restriction_scheme: str = None
    ignore_user: List[str] = None
    include_id_file: List[str] = None
    log: str = None
    saved: bool = False
    search: str = None
    submitted: bool = False
    upvoted: bool = False
    limit: int = None
    sort: SortType = SortType.HOT
    link: List[str] = None
    multireddit: List[str] = None
    subreddit: List[str] = None
    time: TimeFilter = TimeFilter.ALL
    time_format: str = None
    user: List[str] = None
    verbose: int = 0
    download_config: DownloaderConfiguration = DownloaderConfiguration()
    archiver_config: ArchiverConfiguration = ArchiverConfiguration()


def serialize_downloader_configuration(downloader_config):
    command_list = []
    if downloader_config.make_hard_links:
        command_list.append('--hard-link')
    if downloader_config.max_wait_time is not None and downloader_config.max_wait_time != 120:
        command_list.append(f'--max-wait-time {downloader_config.max_wait_time}')
    if downloader_config.no_dupes:
        command_list.append('--no-dupes')
    if downloader_config.search_existing:
        command_list.append('--search-existing')
    if downloader_config.file_scheme != '{REDDITOR}_{TITLE}_{POSTID}':
        command_list.append(f'--file-scheme {downloader_config.file_scheme}')
    if downloader_config.folder_scheme != '{SUBREDDIT}':
        command_list.append(f'--folder-scheme {downloader_config.folder_scheme}')
    if downloader_config.exclude_id is not None:
        for item in downloader_config.exclude_id:
            command_list.append(f'--exclude-id {item}')
    if downloader_config.exclude_id_file is not None:
        for item in downloader_config.exclude_id_file:
            command_list.append(f'--exclude-id-file {item}')
    if downloader_config.skip_domain is not None:
        for item in downloader_config.skip_domain:
            command_list.append(f'--skip-domain {item}')
    if downloader_config.skip is not None:
        for item in downloader_config.skip:
            command_list.append(f'--skip {item}')
    if downloader_config.skip_subreddit is not None:
        for item in downloader_config.skip_subreddit:
            command_list.append(f'--skip-subreddit {item}')
    if downloader_config.min_score is not None:
        command_list.append(f'--min-score {downloader_config.min_score}')
    if downloader_config.max_score is not None:
        command_list.append(f'--max-score {downloader_config.max_score}')
    if downloader_config.min_score_ratio is not None:
        command_list.append(f'--min-score-ratio {downloader_config.min_score_ratio}')
    if downloader_config.max_score_ratio is not None:
        command_list.append(f'--max-score-ratio {downloader_config.max_score_ratio}')

    return ' '.join(command_list)


def serialize_input_configuration(input_config):
    command_list = []
    if input_config.directory is not None:
        command_list.append(f'--directory {input_config.directory}')
    if input_config.authenticate:
        command_list.append('--authenticate')
    if input_config.config is not None:
        command_list.append(f'--config {input_config.config}')
    if input_config.opts is not None:
        command_list.append(f'--opts {input_config.opts}')
    if input_config.disable_module is not None:
        for item in input_config.disable_module:
            command_list.append(f'--disable-module {item}')
    if input_config.filename_restriction_scheme is not None:
        command_list.append(f'--filename-restriction-scheme {input_config.filename_restriction_scheme}')
    if input_config.ignore_user is not None:
        for item in input_config.ignore_user:
            command_list.append(f'--ignore-user {item}')
    if input_config.include_id_file is not None:
        for item in input_config.include_id_file:
            command_list.append(f'--include-id-file {item}')
    if input_config.log is not None:
        command_list.append(f'--log {input_config.log}')
    if input_config.saved:
        command_list.append('--saved')
    if input_config.search is not None:
        command_list.append(f'--search {input_config.search}')
    if input_config.submitted:
        command_list.append('--submitted')
    if input_config.upvoted:
        command_list.append('--upvoted')
    if input_config.limit is not None:
        command_list.append(f'--limit {input_config.limit}')
    if input_config.sort != SortType.HOT:
        command_list.append(f'--sort {input_config.sort.value}')
    if input_config.link is not None:
        for item in input_config.link:
            command_list.append(f'--link {item}')
    if input_config.multireddit is not None:
        for item in input_config.multireddit:
            command_list.append(f'--multireddit {item}')
    if input_config.subreddit is not None:
        for item in input_config.subreddit:
            command_list.append(f'--subreddit {item}')
    if input_config.time != TimeFilter.ALL:
        command_list.append(f'--time {input_config.time.value}')
    if input_config.time_format is not None:
        command_list.append(f'--time-format {input_config.time_format}')
    if input_config.user is not None:
        for item in input_config.user:
            command_list.append(f'--user {item}')
    if input_config.verbose is not None and input_config.verbose != 0:
        command_list.append(f'-{"v" * input_config.verbose}')

    downloader_command = ''

    if input_config.download_config is not None:
        downloader_command = serialize_downloader_configuration(input_config.download_config)

    archiver_command = ''

    if (input_config.archiver_config):
        archiver_command += '--all-comments ' if input_config.archiver_config.all_comments else ''

        if input_config.archiver_config.format != Format.JSON:
            archiver_command += f'-f {input_config.archiver_config.format.value}'

        archiver_command += '--comment-context ' if input_config.archiver_config.comment_context else ''

    return ' '.join(command_list) + ' ' + downloader_command + ' ' + archiver_command


def is_none_or_empty(value):
    return value is None or value == '' or value == []
