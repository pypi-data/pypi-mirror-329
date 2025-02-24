def lazy(
    options_list,
    custom_input_message="Options are: \n",
    custom_success_message="Chosen option: ",
    custom_invalid_message="\nThat is not a valid option. Try again.\n",
):
    if custom_input_message == "Options are: \n":
        i = input(f"{custom_input_message}{"\n".join(options_list)}\n")
    else:
        i = input(custom_input_message)
    while True:
        if i not in options_list:
            print(custom_invalid_message)
        else:
            if custom_success_message == "Chosen option: ":
                print(f"{custom_success_message}{i}")
            else:
                print(custom_success_message)
            return i

        i = input("")
