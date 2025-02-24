def lazy(
    options_list,
    custom_input_message="Options are: ",
    custom_success_message="Chosen option: ",
    custom_invalid_message="\nThat is not a valid option. Try again.\n",
):
    if custom_input_message == "Options are: ":
        i = input(f"{custom_input_message} {"\n".join(options_list)}\n")
    else:
        i = input(custom_input_message)
    while True:
        if i not in options_list:
            print(custom_invalid_message)
            continue

        if i in options_list:
            print(custom_success_message)
            return i
