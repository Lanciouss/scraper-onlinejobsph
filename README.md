# OnlineJobs.ph Job Scraper

Automated job scraper built with Scrapy that searches OnlineJobs.ph for automation and AI-related roles.

## What it does
- Searches 15+ targeted keywords across multiple pages
- Filters out irrelevant listings automatically
- Outputs clean JSON ready for processing

## Stack
- Python / Scrapy
- Runs on self-hosted Arch Linux server
- Integrated with n8n workflow for automatic Google Sheets logging and Discord alerts
- Scores job listings by relevance using weighted keyword matching

## How it works
1. Spider crawls OnlineJobs.ph search results for automation-related terms
2. Filters noise (video editors, social media roles, etc)
3. n8n picks up the output, scores each listing, logs to Google Sheets
4. High-relevance jobs trigger a Discord notification instantly
