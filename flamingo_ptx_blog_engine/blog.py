from flamingo.core.utils.pagination import paginate
from flamingo.core.plugins.media import add_media


class Blog:
    def contents_parsed(self, context):
        I18N_CONTENT_KEY = getattr(context.settings, 'I18N_CONTENT_KEY', 'id')

        I18N_LANGUAGES = getattr(context.settings, 'I18N_LANGUAGES',
                                 ['en', 'de'])

        for content in context.contents.filter(path__startswith='blog/'):
            content['type'] = 'blog'
            content['template'] = 'blog_post.html'

            content['output'] = 'blog/{}.html'.format(content['slug'])
            content['url'] = '/' + content['output']

            media_content = add_media(context, content, content['image'],
                                      width='260px', type='media/image')

            content['image'] = media_content

        # gen pages
        all_slugs = context.contents.filter(
            type='blog',
        ).order_by(
            '-date',
        ).values(
            I18N_CONTENT_KEY,
        )

        for lang in I18N_LANGUAGES:
            for slugs, page, total_pages in paginate(all_slugs, context):
                context.contents.add(**{
                    I18N_CONTENT_KEY: '_blog/{}'.format(page),
                    'lang': lang,
                    'output': 'blog/{}.html'.format(page),
                    'url': '/blog/{}.html'.format(page),
                    'slugs': slugs,
                    'template': 'blog.html',
                    'pagination': {
                        'page': page,
                        'total_pages': total_pages,
                    }
                })
