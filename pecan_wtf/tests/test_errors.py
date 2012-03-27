from unittest import TestCase


class TestErrorWidget(TestCase):

    def make_form(self, values={}, config={}):
        import pecan_wtf

        class SmartField(pecan_wtf.fields.TextField):
            widget = pecan_wtf.errors.ErrorMarkupWidget(
                pecan_wtf.fields.TextField.widget,
                **config
            )

        class SimpleForm(pecan_wtf.Form):
            name = SmartField(
                "Name",
                [pecan_wtf.validators.Required()]
            )

        f = SimpleForm(csrf_enabled=False, **values)
        f.validate()
        return f

    def test_errorless_field(self):
        f = self.make_form({'name': 'Ryan'})
        assert f.errors == {}
        assert str(f.name) == ('<input id="name" name="name" type="text" '
                               'value="Ryan">')

    def test_error_prepend(self):
        f = self.make_form()
        assert f.errors == {'name': ['This field is required.']}
        assert str(f.name).startswith(
            '<span class="error-message">This field is required.</span><br />'
        )

    def test_error_append(self):
        f = self.make_form(config={'prepend_errors': False})
        assert f.errors == {'name': ['This field is required.']}
        assert str(f.name).strip().endswith(
            '<span class="error-message">This field is required.</span><br />'
        )

    def test_custom_formatter(self):
        f = self.make_form(config={
            'error_formatter': lambda msg: 'OMG! %s' % msg
        })
        assert f.errors == {'name': ['This field is required.']}
        assert str(f.name).startswith(
            'OMG! This field is required.'
        )

    def test_format_multiple_errors(self):
        from pecan_wtf.errors import ErrorMarkupWidget
        markup = ErrorMarkupWidget(None).format_errors(['Error 1', 'Error 2'])
        assert markup == ''.join([
            '<span class="error-message">Error 1</span><br />\n',
            '<span class="error-message">Error 2</span><br />\n'
        ])
