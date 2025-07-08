pipeline {
    agent any

    environment {
        FUNCTION_NAME = 'iit_order_service'
        REGION = 'us-east-1'
        ZIP_FILE = 'python.zip'
    }

    stages {
        stage('Setup Virtual Environment') {
            steps {
                sh '''
                echo "✅ Creating Python virtual environment..."
                python3 -m venv venv
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                echo "✅ Activating virtual environment and installing dependencies..."
                source venv/bin/activate
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Integration Tests') {
            steps {
                sh '''
                echo "✅ Running integration tests..."
                source venv/bin/activate
                uvicorn app.main:app --host 127.0.0.1 --port 8000 &
                SERVER_PID=$!
                sleep 20
                pytest app/tests/integration

                TEST_RESULT=$?

                # Stop the FastAPI server
                kill $SERVER_PID

                # Fail the Jenkins job if tests failed
                if [ $TEST_RESULT -ne 0 ]; then
                  echo "❌ Integration tests failed!"
                  exit 1
                else
                  echo "✅ Integration tests passed!"
                fi
                '''
            }
        }

        stage('Package Lambda Function') {
            steps {
                sh '''
                echo "✅ Packaging application into zip file for AWS Lambda..."
                zip -r ${ZIP_FILE} app/
                ls -lh
                '''
            }
        }

        stage('Deploy to AWS Lambda') {
            steps {
                // Use AWS Lambda deployment plugin with stored credentials
                awsLambdaDeploy(
                    functionName: "${FUNCTION_NAME}",
                    region: "${REGION}",
                    updateMode: 'code',
                    zipFilePath: "${ZIP_FILE}",
                    awsAccessKeyId: credentials('aws-access-key-id'),
                    awsSecretKey: credentials('aws-access-key-id')
                )
            }
        }
    }

    post {
        always {
            echo '🧹 Cleaning up...'
            sh 'rm -rf venv'
        }
    }
}

