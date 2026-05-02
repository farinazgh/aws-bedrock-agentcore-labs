import argparse
import getpass
import sys

import boto3
from botocore.exceptions import ClientError

DEFAULT_REGION = "eu-west-1"
TEMPORARY_PASSWORD = "TempPass123@#!"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Create a Cognito User Pool, App Client, user, and access token."
    )

    parser.add_argument("--user-pool-name", required=True)
    parser.add_argument("--client-name", required=True)
    parser.add_argument("--username", required=True)
    parser.add_argument("--region", default=DEFAULT_REGION)

    return parser.parse_args()


def create_user_pool(cognito, user_pool_name):
    response = cognito.create_user_pool(
        PoolName=user_pool_name,
        Policies={
            "PasswordPolicy": {
                "MinimumLength": 8,
            }
        },
    )
    return response["UserPool"]["Id"]


def create_app_client(cognito, pool_id, client_name):
    response = cognito.create_user_pool_client(
        UserPoolId=pool_id,
        ClientName=client_name,
        GenerateSecret=False,
        ExplicitAuthFlows=[
            "ALLOW_USER_PASSWORD_AUTH",
            "ALLOW_REFRESH_TOKEN_AUTH",
        ],
    )
    return response["UserPoolClient"]["ClientId"]


def create_user(cognito, pool_id, username):
    cognito.admin_create_user(
        UserPoolId=pool_id,
        Username=username,
        TemporaryPassword=TEMPORARY_PASSWORD,
        MessageAction="SUPPRESS",
    )


def set_permanent_password(cognito, pool_id, username, password):
    cognito.admin_set_user_password(
        UserPoolId=pool_id,
        Username=username,
        Password=password,
        Permanent=True,
    )


def authenticate_user(cognito, client_id, username, password):
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

    permanent_password = getpass.getpass("Enter Permanent Password (will be hidden): ")

    cognito = boto3.client("cognito-idp", region_name=args.region)

    try:
        print("Creating user pool...")
        pool_id = create_user_pool(cognito, args.user_pool_name)

        print("Creating app client...")
        client_id = create_app_client(cognito, pool_id, args.client_name)

        print("Creating user...")
        create_user(cognito, pool_id, args.username)

        print("Setting permanent password...")
        set_permanent_password(
            cognito,
            pool_id,
            args.username,
            permanent_password,
        )

        print("Authenticating user...")
        access_token = authenticate_user(
            cognito,
            client_id,
            args.username,
            permanent_password,
        )

    except ClientError as error:
        print(f"AWS error: {error.response['Error']['Message']}", file=sys.stderr)
        sys.exit(1)

    print("\n✅ Setup Complete")
    print(f"Pool ID: {pool_id}")
    print(
        f"Discovery URL: https://cognito-idp.{args.region}.amazonaws.com/"
        f"{pool_id}/.well-known/openid-configuration"
    )
    print(f"Client ID: {client_id}")
    print(f"Bearer Token: {access_token}")


if __name__ == "__main__":
    main()
