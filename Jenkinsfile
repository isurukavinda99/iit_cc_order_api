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
                . venv/bin/activate
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Integration Tests') {

            environment {
                DB_HOST='iit-cc-assignment.cg7k80goqzon.us-east-1.rds.amazonaws.com'
                DB_NAME='test_iit_game_service'
                DB_USER='root'
                DB_PASSWORD='iitCCAsign1'
                DB_PORT='3306'
                COGNITO_USER_POOL_ID='us-east-1_SGSijIBP0'
                COGNITO_CLIENT_ID='79kvjkpkt94sksjel3f0720834'
                AWS_REGION='us-east-1'
                OIDC_TOKEN='eyJraWQiOiJ1Z1N2T1lOUWY3TUVQWlJFMkNcL3pkMDBGOGMyemZCSW5ITE9OSldDZENBMD0iLCJhbGciOiJSUzI1NiJ9.eyJhdF9oYXNoIjoiZ0FjT0Y5MkU0TkM5cllkaE05R2RxdyIsInN1YiI6IjI0NjhjNDk4LWQwYjEtNzAzMy1iYTk3LWIzMTVlNGRjMWZlZCIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV9TR1NpaklCUDAiLCJjb2duaXRvOnVzZXJuYW1lIjoiMjQ2OGM0OTgtZDBiMS03MDMzLWJhOTctYjMxNWU0ZGMxZmVkIiwib3JpZ2luX2p0aSI6ImFhODMyMWI0LTNiYjYtNDA5OC05MzRhLTAwNmUzNDFhZDY5MCIsImF1ZCI6Ijc5a3Zqa3BrdDk0c2tzamVsM2YwNzIwODM0IiwiZXZlbnRfaWQiOiI3YThjOTZkYS1hOTlmLTRjMDItYjViMC1mNmUzYTcyZDk2OGYiLCJ0b2tlbl91c2UiOiJpZCIsImF1dGhfdGltZSI6MTc1MDU3MzcwMCwiZXhwIjoxNzUwNTc3MzAwLCJpYXQiOjE3NTA1NzM3MDAsImp0aSI6IjE3MzA2YWQ2LTQ3ZmQtNDU2Ny05ZWM0LWUzNDk1NmI1YjA4OCIsImVtYWlsIjoiYmx1ZXBob2VuaXg3ODNAZ21haWwuY29tIn0.ioM-Cd0c9z-tt603p8otOu5oGlUjzxUBIeezVs2NKWUXcgeXOWcABHeNP1S4nXkKz1kvXheoXscym9igOQCsDrRTLulbcuubLnJrRi_ddP69mVqM4f3M22DRZQXGA6Qm25BK_0Jx7a9Obo0KPc0T1lEbSH6wZXieVksjy4yJtr196cwrxHq988QzUm6GlHl_0V4Ub_zKCHrYvHYPmruxyY_H1OQ-rfza-OOK2aV1Pr0VSv7oE85rHQY1NVF_7O_roC1b9P4HADDIstKJktRpiHQ6_ZPifxIbrYXKxP3dpcBi3VH0QKEfiWIzKYRcjrB57bTvsK0bQJO1CuVq8LOE7w'
            }

            steps {
                sh '''
                echo "✅ Running integration tests..."
                . venv/bin/activate
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
                withCredentials([
                    usernamePassword(credentialsId: 'aws-access-key-id', usernameVariable: 'AWS_ACCESS_KEY_ID', passwordVariable: 'AWS_SECRET_ACCESS_KEY')
                ]) {
                    sh '''
                    echo "✅ Deploying to AWS Lambda..."

                    aws lambda update-function-code \
                      --function-name ${FUNCTION_NAME} \
                      --region us-east-1 \
                      --zip-file fileb://${ZIP_FILE}
                    '''
                }
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

