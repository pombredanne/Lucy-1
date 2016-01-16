#!/usr/bin/env python

import re
import sys
from datetime import datetime

import click
import requests

API_URL = 'https://api.github.com/licenses'
HEADERS = {
	"Accept" : "application/vnd.github.drax-preview+json",
}

def build_license_content(content, name):
	"""Creates the license by replacing year and name in the original text."""
	year = datetime.now().year
	content = re.sub('\[year\]', str(year), content)
	content = re.sub('\[fullname\]', name, content)
	return content

@click.group()
def main():
	"""It generates a license for your project."""
	pass

@main.command()
def list():
	"""Lists all available licenses."""
	call_url = API_URL
	response = requests.get(call_url, headers=HEADERS)
	if response.status_code == requests.codes.ok:
		license_list = [x['key'] for x in response.json()]
		click.echo(license_list)
	else:
		click.echo("Service not working at the moment.")

@main.command()
@click.argument('license_name')
@click.option('--name', prompt="Author's name please")
def create(license_name, name):
	"""Fetches the content of the requested license."""
	call_url = API_URL + '/' + license_name
	response = requests.get(call_url, headers=HEADERS)
	if response.status_code == requests.codes.ok:
		content = response.json()['body']
		license_content = build_license_content(content, name)
		click.echo(license_content)
	else:
		click.echo("Please check the license name you provided.")
	
if __name__ == '__main__':
	main()
	sys.exit(0)