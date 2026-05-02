import argparse
import getpass
import sys

import boto3
from botocore.exceptions import ClientError

DEFAULT_REGION = "eu-west-1"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Authenticate against Cognito and retrieve an access token."
    )

    parser.add_argument("--client-id", help="Cognito App Client ID")
    parser.add_argument("--username", help="Cognito username")
    parser.add_argument("--region", default=DEFAULT_REGION)

    return parser.parse_args()


def prompt_if_missing(value, prompt_text, secret=False):
    if value:
        return value
    return getpass.getpass(prompt_text) if secret else input(prompt_text)


def authenticate(cognito, client_id, username, password):
    response = cognito.initiate_auth(
        ClientId=client_id,
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={
            "USERNAME": username,
            "PASSWORD": password,
        },
    )
    return response["AuthenticationResult"]["AccessToken"]


def main():
    args = parse_args()

    client_id = prompt_if_missing(
        args.client_id, "Enter Cognito App Client ID (no secret): "
    )
    username = prompt_if_missing(args.username, "Enter your Cognito username: ")
    password = prompt_if_missing(None, "Enter your Cognito password: ", secret=True)

    cognito = boto3.client("cognito-idp", region_name=args.region)

    try:
        token = authenticate(cognito, client_id, username, password)

    except ClientError as error:
        code = error.response["Error"]["Code"]

        if code == "NotAuthorizedException":
            print("❌ Invalid username or password.", file=sys.stderr)
        elif code == "UserNotConfirmedException":
            print("❌ User is not confirmed.", file=sys.stderr)
        elif code == "UserNotFoundException":
            print("❌ User not found.", file=sys.stderr)
        else:
            print(f"❌ AWS error: {error}", file=sys.stderr)

        sys.exit(1)

    print("\n✅ Authentication successful")
    print(f"Bearer Token (AccessToken):\n{token}")


if __name__ == "__main__":
    main()
