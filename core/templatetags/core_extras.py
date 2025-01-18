from django import template

register = template.Library()


@register.filter
def get_post_text_substring(querySet, key):
    post_text = querySet.get(key)
    if post_text is not None:
        final_post_text = post_text[0:297]
        final_post_text_caracter = post_text[297]
        if (
            final_post_text_caracter == "."
            or final_post_text_caracter == "?"
            or final_post_text_caracter == "!"
        ):
            return final_post_text[0:296]
        else:
            return final_post_text_caracter
