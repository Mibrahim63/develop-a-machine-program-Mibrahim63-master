import time

from database import database


def display_welcome():
    print("\n" + "*" * 40)
    print("**        WELCOME TO VFX STUDIO!        **")
    print("*" * 40 + "\n")


def display_goodbye():
    print("\n" + "*" * 40)
    print("**    THANK YOU FOR CREATING MAGIC!    **")
    print("**         SEE YOU NEXT TIME!          **")
    print("*" * 40 + "\n")


def display_tasks(user):
    task = database[user]["task"]
    print(f"\n{'*' * 20}")
    print(f"{'**':<2} Welcome, {user}! {'**':>5}")
    print(f"{'*' * 20}\n")
    print(f"{'*' * 20}")
    print(f"{'**':<2} {task.upper():^14} {'**':>4}")
    print(f"{'*' * 20}\n")
    if database[user]["start_time"] is not None:
        print(
            f"Start Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(database[user]['start_time']))}"
        )
        print(f"{'-' * 20}\n")


def login():
    display_welcome()

    while True:
        user = input("Enter your username: ")
        password = input("Enter your password: ")

        if user in database and database[user]["password"] == password:
            log_message = (
                f"Signed in at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}."
            )
            log_to_file(user, log_message)
            return user
        else:
            print("Invalid username or password. Try again.")


def log_to_file(user, message):
    with open(f"{user}_log.txt", "a") as file:
        log_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        file.write(f"{log_time}: {message}\n")


def vfx_project(user):
    display_tasks(user)

    while True:
        try:
            action = input(
                "Press 'P' to pause, 'C' to continue, or 'F' to finish: "
            ).upper()
        except ValueError:
            print(
                "Invalid input. Please press 'P' to pause, 'C' to continue, or 'F' to finish."
            )
            continue

        if action == "F":
            end_time = time.time()
            total_time = end_time - database[user]["start_time"]
            log_message = f"Finished {database[user]['task']}! Total time taken: {total_time / 3600:.2f} hours"
            log_to_file(user, log_message)
            print(
                f"\nFinish Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}"
            )
            print(log_message)
            print("\n" + "*" * 40)
            print(f"**{'':<36}**")
            print(f"**{'':<12}GOODBYE!{'':<11}**")
            print(f"**{'':<36}**")
            print("*" * 40 + "\n")
            display_goodbye()
            break

        if action == "P":
            pause_time = time.strftime("%Y-%m-%d %H:%M:%S")
            log_message = f"Paused at {pause_time}."
            log_to_file(user, log_message)
            print(f"\nPaused at {pause_time}.\nCoffee break!")
            input(f"\nPress 'C' to continue.")
            resume_time = time.strftime("%Y-%m-%d %H:%M:%S")
            log_message = f"Resumed at {resume_time}."
            log_to_file(user, log_message)
            print(f"Resumed at {resume_time}.\nWelcome back!")

        if action == "C" and database[user]["start_time"] is None:
            database[user]["start_time"] = time.time()
            start_time = time.strftime("%Y-%m-%d %H:%M:%S")
            log_message = f"Starting {database[user]['task']} at {start_time}..."
            log_to_file(user, log_message)
            print(f"\nStarting {database[user]['task']} at {start_time}...")
            print(f"{'-' * 20}\n")


if __name__ == "__main__":
    logged_in_user = login()
    database[logged_in_user]["start_time"] = time.time()
    vfx_project(logged_in_user)
