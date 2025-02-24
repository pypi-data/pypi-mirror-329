# DNSupdater

![PyPI - Version](https://img.shields.io/pypi/v/dnsupdater) ![PyPI - Downloads](https://img.shields.io/pypi/dm/dnsupdater)

Update an Amazon Route53 or Cloudflare record with your current public IP address.

## Credentials configuration

### AWS

Easiest way is to install AWS CLI from [here](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) and then configure the credentials executing `aws configure` and provide access key and secret key for an IAM user with enough permissions to update the Route53 hosted zone.

### Cloudflare

Set a Cloudflare token in `CLOUDFLARE_API_TOKEN` environment variable or create a proper configuration file `~/.cloudflare/cloudflare.cf`

Full documentation [here](https://github.com/cloudflare/python-cloudflare?tab=readme-ov-file#providing-cloudflare-username-and-api-key)

## How to run

### From git

```
$ pwd
/home/user 
$ git clone git@github.com:diegofd/dnsupdater.git
$ cd dnsupdater
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
$ cd src

# For AWS
$ python3 -m dnsupdater.dnsupdater --name RECORD_NAME route53 --hosted-zone-id HOSTED_ZONE_ID

# For Cloudflare
$ python3 -m dnsupdater.dnsupdater --name RECORD_NAME cloudflare --domain DOMAIN
```

### From package

Using virtualenv is recommended to not polute your system.

```
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install dnsupdater

# For AWS
$ dnsupdater --name RECORD_NAME route53 --hosted-zone-id HOSTED_ZONE_ID

# For Cloudflare
$ dnsupdater --name RECORD_NAME cloudflare --domain DOMAIN
```

## How to schedule it with cron

Follow the steps above to install and configure a cron job to run every hour:
```
0 *     * * *   user   cd /home/user/dnsupdater && .venv/bin/python3 -m dnsupdater.dnsupdater --name sub.example.com route53 --hosted-zone-id ZXXXXXXXXXXX 
```

## Cost

### AWS

Estimated cost is $0.5 per hosted zone per month plus additional cost per DNS requests (none or tiny for a personal setup). [Complete Route53 pricing information](https://aws.amazon.com/es/route53/pricing/). 

### Cloudflare

Free.

## Development

Feel free to open issues or send PRs.

* Packaging documentation: https://packaging.python.org/en/latest/tutorials/packaging-projects/
