from django.forms import ModelForm, Form


def errorDict(form: ModelForm | Form, fields_errors: dict = None):
    errors = dict()

    # 字典不为空，说明没有自定义错误，使用默认错误信息
    if fields_errors:
        for field, error in fields_errors.items():
            # form.add_error(field=field, error=error)  # 不再额外给form添加错误信息，直接生成错误信息字典返回
            errors[field] = error
        return errors

    # 字典为空，使用默认的错误信息
    for key, value in form.errors.items():
        errors[key] = value[0][:-1]  # 删去结尾句号
    return errors
