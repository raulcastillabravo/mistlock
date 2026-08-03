DEFINITION_PATH = "step_function.asl.json"


def render_definition(arns: dict) -> str:
    """Replaces the ${LambdaArn} placeholders of the ASL definition."""
    with open(DEFINITION_PATH) as definition_file:
        definition = definition_file.read()

    for key, arn in arns.items():
        definition = definition.replace(f"${{{key}}}", arn)
    return definition
