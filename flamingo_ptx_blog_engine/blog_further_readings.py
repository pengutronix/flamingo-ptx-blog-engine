from flamingo import ContentSet, Q


class BlogFurtherReadings:
    def setup(self, context):
        self.context = context
        self.tags = {}

    def get_further_readings(self, content):
        further_readings = ContentSet()

        # user defined further readings
        if content['further_readings']:
            for path in content['further_readings']:
                c = self.context.contents.get(path=path)

                if c['lang'] != content['lang']:
                    c = c['translations'].get(lang=content['lang'])

                if c not in further_readings:
                    further_readings.add(c)

        if(further_readings.count() >=
           self.context.settings.FURTHER_READINGS_MAX):

            return further_readings

        # auto generated further readings
        _further_readings = ContentSet()

        if content['tags']:
            for tag_name in content['tags']:
                contents_with_tag = self.tags[tag_name][1].filter(
                    ~Q(id=content['id']),
                    Q(lang=content['lang']),
                )

                counter = 0

                for content_with_tag in contents_with_tag:

                    if(content_with_tag['id'] == content['id'] or
                       content_with_tag['lang'] != content['lang'] or
                       content_with_tag in further_readings or
                       content_with_tag in _further_readings):

                        continue

                    _further_readings.add(content_with_tag)
                    counter += 1

                    if(counter ==
                       self.context.settings.FURTHER_READINGS_MAX_PER_TAG):

                        break

                    if(len(_further_readings) + len(further_readings) >=
                       self.context.settings.FURTHER_READINGS_MAX):

                        break

                if(len(_further_readings) + len(further_readings) >=
                   self.context.settings.FURTHER_READINGS_MAX):

                    break

        return further_readings + _further_readings.order_by('-date')

    def templating_engine_setup(self, context, templating_engine):
        templating_engine.env.globals['get_further_readings'] = \
            self.get_further_readings

    def contents_parsed(self, context):
        content_ids = {}

        for content in context.contents:
            if content['type'] != 'blog':
                continue

            if not content['tags']:
                continue

            if content['id'] and content['id'] not in content_ids:
                content_ids[content['id']] = []

            for tag in content['tags']:
                if tag not in self.tags:
                    self.tags[tag] = [0, ContentSet()]

                if tag in content_ids[content['id']]:
                    self.tags[tag][0] += 1

                self.tags[tag][1].add(content)
                content_ids[content['id']].append(tag)

        for name, values in self.tags.items():
            values[1] = values[1].order_by('-date')
