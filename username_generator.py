from config import os, string
from config import Fore
from config import TiktokUsernameChecker
from itertools import product

def username_generator():
    """
    Generate every possible 3-character username combination.
    """

    characters = string.ascii_lowercase + string.digits + "_."
    output_file = os.path.join(
        TiktokUsernameChecker.directory,
        "output",
        "usernames.txt"
    )

    generated = 0

    with open(output_file, "a") as f:
        for chars in product(characters, repeat=3):
            username = "".join(chars)

            # TikTok does not allow a username ending in '.'
            if username.endswith("."):
                continue

            f.write(username + "\n")
            generated += 1

    print(
        Fore.GREEN +
        f"\nSuccessfully generated {generated} unique 3-character usernames."
    )
    print(f"Saved to: {output_file}")
