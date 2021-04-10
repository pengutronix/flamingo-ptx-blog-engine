from docutils.parsers.rst import directives
from bs4 import BeautifulSoup

from flamingo.plugins.rst.directives import NestedDirective


def _summary(context):
    class BlogSummary(NestedDirective):
        def run(self):
            html = super().parse_content(context)

            context.content['has_summary'] = True
            context.content['summary'] = html

            return []

    return BlogSummary


def strip_html_tags(html):
    soup = BeautifulSoup(str(html), 'html.parser')
    text = soup.get_text()
    text = text.replace('"', '').replace("'", '')

    return text


class Summary:
    def _extract_summary(self, content):
        if not content['content_body']:
            return ''

        soup = BeautifulSoup(content['content_body'], 'html.parser')

        non_summary_divs = soup.find(
            'div', {'class': ['ptx-image', 'ptx-sidebar']}
        )

        if non_summary_divs:
            non_summary_divs.decompose()

        return soup.find('p', recursive=False)

    def settings_setup(self, context):
        context.settings.EXTRA_CONTEXT['strip_html_tags'] = strip_html_tags

    def contents_parsed(self, context):
        # find summaries
        for content in context.contents.filter(has_summary=True):
            if content['summary']:
                continue

            content['summary'] = self._extract_summary(content)

    def parser_setup(self, context):
        directives.register_directive('summary', _summary(context))
