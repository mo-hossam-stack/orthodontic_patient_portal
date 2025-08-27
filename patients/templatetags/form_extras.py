from django import template

register = template.Library()


@register.filter
def add_class(field, css):
	attrs = field.field.widget.attrs
	current = attrs.get('class', '')
	attrs['class'] = (current + ' ' + css).strip()
	return field



