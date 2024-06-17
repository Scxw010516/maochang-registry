def get_err(form):
    """
        获取form错误文本
    """
    errors = form.errors.get_json_data()
    new_errors = {}
    for key,message_dicts in errors.items():
        messages = []
        for message in message_dicts:
            messages.append(message['message'])
            new_errors[key] = messages
    return new_errors
    # error_list = []
    # for item in form.errors.get_json_data().values():
    #     error_list.append(item[0].get('message'))
    # err_str = ';'.join(error_list)
    # return err_str
