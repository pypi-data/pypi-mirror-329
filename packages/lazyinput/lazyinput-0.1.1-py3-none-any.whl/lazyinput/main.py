def lazy(
    options_list,
    custom_input_message="Options are: \n",
    custom_success_message="Chosen option: ",
    custom_invalid_message="\nThat is not a valid option. Try again.\n",
):
    print(f"{custom_input_message}")
    for i in options_list:
        print(f"- {i}")

    print("")

    i = input()

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
