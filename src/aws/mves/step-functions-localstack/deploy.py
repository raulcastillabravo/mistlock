from src.stack import OnboardingStack


def main():
    print("Deploying DynamoDB table, Lambdas and Step Function...")
    OnboardingStack().deploy()
    print("Stack deployed")


if __name__ == "__main__":
    main()
