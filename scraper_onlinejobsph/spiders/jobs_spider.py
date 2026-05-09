import scrapy
import re
from datetime import datetime


class JobsSpider(scrapy.Spider):
    name = "jobs"
    base_url = "https://www.onlinejobs.ph"
    search_page = "/jobseekers/jobsearch"

    search_terms = [
        'n8n', 'zapier', 'make.com', 'automation engineer',
        'automation specialist', 'workflow automation', 'rpa',
        'power automate', 'no-code', 'webhook',
        'python automation', 'api integration',
        'web scraping', 'discord bot', 'chatbot developer',
    ]

    exclusions = [
        'senior', 'lead', 'magento', 'female',
        'video editor', 'graphic designer', 'content creator',
        'podcast', 'animator', 'social media', 'sales',
        'accountant', 'bookkeeper', 'customer service'
    ]
    search_exclusions = '|'.join(re.escape(e) for e in exclusions)

    list_posts = "div.jobpost-cat-box"
    job_title  = "h4::text"
    job_link   = "a::attr(href)"
    job_salary = "p.salary-value::text"
    job_desc   = "div.desc::text"

    max_pages = 3

    custom_settings = {
        'DOWNLOAD_DELAY': 0.3,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'CONCURRENT_REQUESTS': 2,
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.RFPDupeFilter',
    }

    def start_requests(self):
        for term in self.search_terms:
            url = f"{self.base_url}{self.search_page}?jobkeyword={term}"
            yield scrapy.Request(url=url, callback=self.parse, meta={'term': term, 'page': 1})

    def parse(self, response):
        term = response.meta.get('term')
        page = response.meta.get('page', 1)
        posts = response.css(self.list_posts)

        for post in posts:
            title  = post.css(self.job_title).get(default='').strip()
            link   = post.css(self.job_link).get()
            salary = post.css(self.job_salary).get(default='Negotiable').strip()
            desc   = post.css(self.job_desc).get(default='').strip()

            if not title or not link:
                continue
            if re.search(self.search_exclusions, title, re.IGNORECASE):
                continue

            full_link = self.base_url + link if link.startswith('/') else link
            yield {
                'role':        title,
                'title':       title,
                'link':        full_link,
                'salary':      salary,
                'description': desc,
                'scraped_at':  datetime.now().strftime("%Y-%m-%d")
            }

        if posts and page < self.max_pages:
            next_url = f"{self.base_url}{self.search_page}?jobkeyword={term}&page={page + 1}"
            yield scrapy.Request(url=next_url, callback=self.parse, meta={'term': term, 'page': page + 1})
