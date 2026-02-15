def test_main(dev_container):
    # 1. Package the Lambda
    pkg_result = dev_container("deploy/utils/package_lambda.py")
    assert pkg_result.returncode == 0
    assert "Created" in pkg_result.stdout

    # 2. Deploy with Boto3
    deploy_result = dev_container("deploy/boto3_deploy.py", ttl=5)
    assert deploy_result.returncode == 0
    assert "Deployment completed successfully" in deploy_result.stdout

    # 3. Execute Main Logic with TTL/Retries
    main_result = dev_container("main.py", ttl=5)
    assert main_result.returncode == 0
    assert "✓ Lambda response" in main_result.stdout
    assert "✓ Content: Hello from Lambda!" in main_result.stdout
