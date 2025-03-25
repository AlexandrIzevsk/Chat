from django import template


register = template.Library()


@register.filter()
def censor(text):
    """
    text: текст, к которому нужно применить фильтр
    """

    if type(text) is not str:
        raise TypeError
    # Возвращаемое функцией значение подставится в шаблон.
    txt = text.split(' ')
    bw = ["пенек", "дурак", "бездарь"]
    str2 = []
    word1 = ''
    for j, value in enumerate(txt):
        if len(value):
            h = value[0]
            k = value.lower()
            if k in bw:
                k = k[1:]
                for x in k:
                    x = x.replace(x, "*")
                    word1 += x
                str1 = h + word1
            else:
                str1 = value
            str2.append(str1)
    str2 = ' '.join(str2)

    return str2
