# wf-email-urls
A script to submit urls seen in the message body of UCE to whiteface

## Requirements

1. [py-cgmail](https://github.com/csirtgadgets/py-cgmail)
1. [py-whitefacesdk](https://github.com/csirtgadgets/py-whitefacesdk)

## Goals

1. To demonstrate how to interact with Whiteface using the Whiteface SDK

## Requirements

1. A [Whiteface](https://whiteface.csirtgadgets.com) account
1. A Whiteface account token; within Whiteface:
  1. Select your username
  1. Select "tokens"
  1. Select "Generate Token
1. A Whiteface feed; within Whiteface
  1. Select (the plus sign)
  1. Select Feed
  1. Choose a feed name (e.g. port scanners)
  1. Choose a feed description (hosts blocked in firewall logs)
1. A Linux mail server with procmail installed
  * procmail is only one way this script could be used

## Install

1. Create a [virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/#basic-usage) for this
project.
1. Install [py-cgmail](https://github.com/csirtgadgets/py-cgmail) and [py-whitefacesdk](https://github.com/csirtgadgets/py-whitefacesdk)
within the virtual environment.
1. 