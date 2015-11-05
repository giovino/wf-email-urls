# -*- encoding: utf-8 -*-

import sys
import cgmail
import logging
import textwrap
import json

from whitefacesdk.client import Client
from whitefacesdk.observable import Observable
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

LOG_FORMAT = '%(asctime)s - %(levelname)s - %(name)s[%(lineno)s] - %(message)s'

logger = logging.getLogger(__name__)

WHITEFACE_USER = ''
WHITEFACE_TOKEN = ''
WHITEFACE_FEED = ''


def main():
    """
    A script to extract URLs in the body of spam email messages and submitting the following to
    whiteface:

    * Date
    * From
    * Subject
    * Description
    * URL
    """

    p = ArgumentParser(
        description=textwrap.dedent('''\
        example usage:
            $ cat test.eml | cgmail -v
            $ cgmail --file test.eml
        '''),
        formatter_class=RawDescriptionHelpFormatter,
        prog='cgmail'
    )

    p.add_argument('-d', '--debug', dest='debug', action="store_true")
    p.add_argument("-f", "--file", dest="file", help="specify email file")
    p.add_argument('--urls', action='store_true')

    args = p.parse_args()

    loglevel = logging.INFO
    if args.debug:
        loglevel = logging.DEBUG

    console = logging.StreamHandler()
    logging.getLogger('').setLevel(loglevel)
    console.setFormatter(logging.Formatter(LOG_FORMAT))
    logging.getLogger('').addHandler(console)

    options = vars(args)

    # get email from file or stdin
    if options.get("file"):
        with open(options["file"]) as f:
            email = f.read()
    else:
        email = sys.stdin.read()
        logger.info("processing email")

    # parse email message
    results = cgmail.parse_email_from_string(email)

    for result in results:
        adata = {}
        if result['urls']:
            for url in result['urls']:

                if 'date' in result['headers']:
                    adata['date'] = result['headers']['date'][0]
                if 'from' in result['headers']:
                    adata['from'] = result['headers']['from'][0]
                if 'subject' in result['headers']:
                    adata['subject'] = result['headers']['subject'][0]

                adata['description'] = 'urls parsed out of the message body sourced from unsolicited commercial ' \
                                       'email (spam)'

                comment = json.dumps(adata)
                c = Client(token=WHITEFACE_TOKEN)
                o = Observable(c, url, tags='uce', comment=comment)
                ret = o.new(user=WHITEFACE_USER, feed=WHITEFACE_FEED)
                logger.info('logged to whiteface %s ' % ret['observable']['location'])

if __name__ == "__main__":
    main()
