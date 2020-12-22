#!/usr/local/CyberCP/bin/python3
import logging
import argparse
from time import time

from Backup import Backup
from Utils import Utils

log_format = "%(asctime)s::%(levelname)s::%(name)s::" \
             "%(lineno)d::%(message)s"
logging.basicConfig(level=logging.DEBUG, format=log_format)
log = logging.getLogger("b2_backup")
# [website_id, website_name, database_name]
website_list = Utils.get_websites_list()

parser = argparse.ArgumentParser()
parser.add_argument('--nocheck', action='store_true', help='doesnt run policies and checks')
parser.add_argument('--debug', action='store_true', help='runs only first vhost')
parser.add_argument('--unlock', action='store_true', help='runs unlock on all hosts first')
parser.add_argument('--cacheCleanup', action='store_true', help='runs unlock on all hosts first')
args = parser.parse_args()

debug = False
if args.debug:
    log.info("!!DEBUG MODE!!")
    debug = True

nocheck = False
if args.nocheck:
    log.info("!!NOCHECK MODE!!")
    nocheck = True

unlock = False
if args.unlock:
    log.info("!!UNLOCK MODE!!")
    unlock = True

cacheCleanup = False
if args.cacheCleanup:
    log.info("!!CACHE_CLEANUP MODE!!")
    cacheCleanup = True

if debug:
    website_list = [website_list[0]]
    # single = []
    # for website in website_list:
    #     vhost = website[1]
    #     if "example.com" in vhost:
    #         print("found it!")
    #         website_list = [website]


def start_backups():
    for website in website_list:
        # website_id = website[0]
        vhost = website[1]
        db_name = website[2]
        log.info("Starting backup of: %s ..." % vhost)
        backup = Backup(vhost, db_name)
        backup.start()
        log.info("Completed Backup of: %s ..." % vhost)
        print("~~~~~~~~~~")
    print()
    print("########### BACKUPS COMPLETE")
    print()


def run_policies():
    log.info("Running Policies and Checks...")
    for website in website_list:
        vhost = website[1]
        job = Backup(vhost, skip_init=True)
        job.policies()


def run_checks():
    log.info("Running Checks...")
    for website in website_list:
        vhost = website[1]
        job = Backup(vhost, skip_init=True)
        job.check()


def run_cache_cleanup():
    log.info("Running Cache Cleanup...")
    for website in website_list:
        vhost = website[1]
        job = Backup(vhost, skip_init=True)
        job.cache_cleanup()


def run_unlock():
    log.info("Running Unlock...")
    for website in website_list:
        vhost = website[1]
        job = Backup(vhost, skip_init=True)
        job.unlock()


if __name__ == '__main__':
    t0 = time()

    if unlock:
        run_unlock()
    if cacheCleanup:
        run_cache_cleanup()

    start_backups()
    if not nocheck:
        run_policies()
        # run_checks()
    # run_cache_cleanup()

    total = time() - t0
    log.info("~~Script Completed in %s" % total)
