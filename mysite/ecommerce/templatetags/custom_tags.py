from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def vueApp(context, app_name):
    if 'vueApp_list' not in context:
        context['vueApp_list'] = []
    context['vueApp_list'].append(app_name)
    return ''
