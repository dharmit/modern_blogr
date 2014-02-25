from wtforms import (
    Form,
    TextField,
    TextAreaField,
    HiddenField,
    fields,
    widgets,
    validators,
    )

from .models import Tag

strip_filter = lambda x: x.strip() if x else None


class TagListField(fields.Field):
    widget = widgets.TextInput()

    def _value(self):
        if self.data:
            return ', '.join([tag.name for tag in self.data])
        else:
            return ''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = Tag.create_tags(valuelist[0])
        else:
            self.data = []


class BlogCreateForm(Form):
    title = TextField('Entry title', [validators.Length(min=1, max=255)],
                      filters=[strip_filter])
    body = TextAreaField('Entry body', [validators.Length(min=1)],
                         filters=[strip_filter])
    tags = TagListField('Tags', [validators.Length(min=1, max=50)],)


class BlogUpdateForm(BlogCreateForm):
    id = HiddenField()
